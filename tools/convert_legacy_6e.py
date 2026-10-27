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
                elif t in ('modifiers','links','rules','profiles'):
                    if len(ch): warnings['unconverted_'+t]+=len(ch)
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
                elif len(ch): warnings['unconverted_group_section:'+t]+=len(ch)
    box=sub(target,'selectionEntries')
    for e in children(source,'entries'): walk(e,box,True)
    shared=sub(target,'sharedSelectionEntries')
    for e in children(source,'sharedEntries'): walk(e,shared)
    sharedgroups=sub(target,'sharedSelectionEntryGroups')
    for e in children(source,'sharedEntryGroups'): walk(e,sharedgroups)
    for section in ('links','rules','sharedRules','sharedProfiles','modifiers'):
        count=len(children(source,section))
        if count: warnings['unconverted_catalogue_section:'+section]+=count
    ET.register_namespace('',NS)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(target).write(args.output,encoding='utf-8',xml_declaration=True)
    result={'status':'EXPERIMENTAL_NOT_PUBLISHABLE','source':source.get('name'),
            'rootUnits':len(box),'sharedEntries':len(shared),
            'sharedGroups':len(sharedgroups),'legacyTypes':dict(old_types),
            'unsupported':dict(warnings),
            'warning':'Do not publish: legacy profiles, links, rules, modifiers and conditional restrictions still require semantic conversion.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
