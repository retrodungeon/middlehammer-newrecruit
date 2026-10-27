#!/usr/bin/env python3
"""Experimental BattleScribe 1.14b -> 2.03 Space Marines catalogue conversion.

Does not publish automatically. Records unsupported legacy constructs instead
of silently treating the output as a complete, rules-correct codex.
"""
import argparse
import collections
import json
import xml.etree.ElementTree as ET
from pathlib import Path

NS = 'http://www.battlescribe.net/schema/catalogueSchema'
N = '{' + NS + '}'
FOC = {
    'HQ': 'ac8d-efba-1884-d3ad',
    'Troops': 'default-category',
    'Elites': '978c-e18f-8aeb-f4c1',
    'Fast Attack': '74fe-37c3-fbbf-849e',
    'Heavy Support': '9260-7d57-be5c-bd52',
    'Dedicated Transport': '168b-a772-94f7-83f5',
}
def local(e): return e.tag.rsplit('}',1)[-1]
def group(e, name): return next((x for x in e if local(x)==name), None)
def children(e,name): 
    x=group(e,name)
    return list(x) if x is not None else []
def sub(parent,tag_name,**attrs):
    return ET.SubElement(parent,N+tag_name,{k:str(v) for k,v in attrs.items() if v is not None})
def constraints(old,new):
    for legacy,scope,kind in [('minSelections','parent','min'),('maxSelections','parent','max'),
                              ('minInForce','force','min'),('maxInForce','force','max'),
                              ('minInRoster','roster','min'),('maxInRoster','roster','max')]:
        val=old.get(legacy)
        if val is not None and float(val)>=0 and not (kind=='min' and float(val)==0):
            box=group(new,'constraints')
            if box is None: box=sub(new,'constraints')
            sub(box,'constraint',id=old.get('id')+'-'+legacy,type=kind,value=val,
                field='selections',scope=scope,shared='true')
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source',type=Path)
    ap.add_argument('target_gst',type=Path)
    ap.add_argument('output',type=Path)
    ap.add_argument('--report',type=Path,required=True)
    ap.add_argument('--source-gst',type=Path)
    ap.add_argument('--experimental-gst',type=Path)
    args=ap.parse_args()
    source=ET.parse(args.source).getroot()
    gst=ET.parse(args.target_gst).getroot()
    target=ET.Element(N+'catalogue',{
        'name':'Space Marines (6th Edition, 2013)',
        'id':source.get('id'),'revision':'1','battleScribeVersion':'2.03',
        'gameSystemId':gst.get('id'),'gameSystemRevision':gst.get('revision'),
        'library':'false'})
    warnings=collections.Counter()
    old_types=collections.Counter()

    if args.source_gst and args.experimental_gst:
        source_gst=ET.parse(args.source_gst).getroot()
        gst_ns='{http://www.battlescribe.net/schema/gameSystemSchema}'
        profile_types=group(gst,'profileTypes')
        if profile_types is None: profile_types=ET.SubElement(gst,gst_ns+'profileTypes')
        known={x.get('id') for x in gst.iter() if x.get('id')}
        count=0
        for old_type in source_gst.iter():
            if local(old_type)!='profileType' or old_type.get('id') in known: continue
            new_type=ET.SubElement(profile_types,gst_ns+'profileType',
                                   {'id':old_type.get('id'),'name':'6e '+old_type.get('name','Profile')})
            characteristic_types=ET.SubElement(new_type,gst_ns+'characteristicTypes')
            for ch in old_type.iter():
                if local(ch)=='characteristic':
                    ET.SubElement(characteristic_types,gst_ns+'characteristicType',
                                  {'id':ch.get('id'),'name':ch.get('name','')})
            count+=1
        args.experimental_gst.parent.mkdir(parents=True,exist_ok=True)
        ET.ElementTree(gst).write(args.experimental_gst,encoding='utf-8',xml_declaration=True)
        print('Legacy profile types added to isolated experimental GST:',count)
    else:
        warnings['missing_experimental_gst_profile_types']=1


    def convert_profile(old,dest):
        box=group(dest,'profiles')
        if box is None: box=sub(dest,'profiles')
        p=sub(box,'profile',id=old.get('id'),name=old.get('name'),typeId=old.get('profileTypeId'),hidden=old.get('hidden','false'))
        chars=sub(p,'characteristics')
        for ch in children(old,'characteristics'):
            sub(chars,'characteristic',name=ch.get('name'),typeId=ch.get('characteristicId')).text=ch.get('value','')
        if children(old,'modifiers'): warnings['unconverted_profile_modifiers']+=len(children(old,'modifiers'))
    def convert_rule(old,dest):
        box=group(dest,'rules')
        if box is None: box=sub(dest,'rules')
        r=sub(box,'rule',id=old.get('id'),name=old.get('name'),hidden=old.get('hidden','false'))
        desc=group(old,'description')
        sub(r,'description').text=(desc.text if desc is not None else old.get('description','')) or ''
        if children(old,'modifiers'): warnings['unconverted_rule_modifiers']+=len(children(old,'modifiers'))
    def convert_link(old,dest):
        kind=old.get('linkType')
        if kind not in ('entry','profile','rule','entry group'):
            warnings['unsupported_link_type:'+str(kind)]+=1
            return
        boxname='entryLinks' if kind in ('entry','entry group') else 'infoLinks'
        box=group(dest,boxname)
        if box is None: box=sub(dest,boxname)
        attrs={'id':old.get('id'),'targetId':old.get('targetId'),'type':'selectionEntryGroup' if kind=='entry group' else ('selectionEntry' if kind=='entry' else kind)}
        sub(box,'entryLink' if kind in ('entry','entry group') else 'infoLink',**attrs)
        if children(old,'modifiers'): warnings['unconverted_link_modifiers']+=len(children(old,'modifiers'))
    def convert_section(old,dest):
        kind=local(old)
        for item in old:
            if kind=='profiles': convert_profile(item,dest)
            elif kind=='rules': convert_rule(item,dest)
            elif kind=='links': convert_link(item,dest)

    def walk(old, dest, root=False):
        name=local(old)
        if name in ('entry','sharedEntry'):
            if root and old.get('name','').lower().startswith('allied detachment'):
                warnings['excluded_allied_detachment']+=1
                return
            e=sub(dest,'selectionEntry',id=old.get('id'),name=old.get('name'),
                  type='unit' if root and old.get('categoryId') not in (None,'(No Category)') else 'upgrade',
                  hidden=old.get('hidden','false'),defaultAmount=old.get('minSelections','0'))
            old_types[old.get('type','')]+=1
            constraints(old,e)
            if float(old.get('points','0'))!=0:
                costs=sub(e,'costs')
                sub(costs,'cost',name='Points',typeId='6f18-a8fc-2c5b-9517',value=old.get('points'))
            if root:
                cat=old.get('categoryId','')
                try:
                    label=bytes.fromhex(cat).decode('utf-8').split('###')[0]
                except (ValueError,UnicodeError):
                    label=''
                if label in FOC:
                    cl=sub(e,'categoryLinks')
                    sub(cl,'categoryLink',id=old.get('id')+'-foc',name=label,
                        targetId=FOC[label],primary='true')
                else: warnings['unmapped_root_category:'+label]+=1
            for ch in old:
                t=local(ch)
                if t=='entries':
                    box=sub(e,'selectionEntries')
                    for item in ch: walk(item,box)
                elif t=='entryGroups':
                    box=sub(e,'selectionEntryGroups')
                    for item in ch: walk(item,box)
                elif t in ('links','rules','profiles'):
                    convert_section(ch,e)
                elif t=='modifiers':
                    if len(ch): warnings['unconverted_modifiers']+=len(ch)
                elif len(ch): warnings['unconverted_entry_section:'+t]+=len(ch)
            return
        if name in ('entryGroup','sharedEntryGroup'):
            e=sub(dest,'selectionEntryGroup',id=old.get('id'),name=old.get('name'),
                  hidden=old.get('hidden','false'),defaultSelectionEntryId=old.get('defaultSelectionEntryId'))
            constraints(old,e)
            for ch in old:
                t=local(ch)
                if t=='entries':
                    box=sub(e,'selectionEntries')
                    for item in ch: walk(item,box)
                elif t=='entryGroups':
                    box=sub(e,'selectionEntryGroups')
                    for item in ch: walk(item,box)
                elif t=='links': convert_section(ch,e)
                elif len(ch): warnings['unconverted_group_section:'+t]+=len(ch)
    box=sub(target,'selectionEntries')
    for e in children(source,'entries'): walk(e,box,True)
    shared=sub(target,'sharedSelectionEntries')
    for e in children(source,'sharedEntries'): walk(e,shared)
    sharedgroups=sub(target,'sharedSelectionEntryGroups')
    for e in children(source,'sharedEntryGroups'): walk(e,sharedgroups)
    for section in ('links','rules','sharedRules','sharedProfiles','modifiers'):
        items=children(source,section)
        if section in ('sharedRules','sharedProfiles'):
            box=sub(target,section)
            for item in items:
                if section=='sharedRules': convert_rule(item,box)
                else: convert_profile(item,box)
            nested=group(box,'rules' if section=='sharedRules' else 'profiles')
            if nested is not None:
                box.remove(nested)
                for item in list(nested): box.append(item)
        elif section in ('links','rules'):
            for item in items:
                if section=='links': convert_link(item,target)
                else: convert_rule(item,target)
        elif items: warnings['unconverted_catalogue_section:'+section]+=len(items)
    ET.register_namespace('',NS)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(target).write(args.output,encoding='utf-8',xml_declaration=True)
    result={'status':'EXPERIMENTAL_NOT_PUBLISHABLE','source':source.get('name'),
            'rootUnits':len(box),'sharedEntries':len(shared),
            'sharedGroups':len(sharedgroups),'convertedProfiles':sum(1 for x in target.iter() if local(x)=='profile'),'convertedRules':sum(1 for x in target.iter() if local(x)=='rule'),'convertedLinks':sum(1 for x in target.iter() if local(x) in ('entryLink','infoLink')),'legacyTypes':dict(old_types),
            'unsupported':dict(warnings),
            'warning':'Do not publish: legacy profiles, links, rules, modifiers and conditional restrictions still require semantic conversion.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
