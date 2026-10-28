#!/usr/bin/env python3
"""Regression gates for the isolated 2013 Space Marines conversion."""
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

catalogue=ET.parse(sys.argv[1]).getroot()
report=json.loads(Path(sys.argv[2]).read_text())
gst=ET.parse(sys.argv[3]).getroot()
def tag(e): return e.tag.rsplit('}',1)[-1]
def direct(e,name):
    return next((x for x in e if tag(x)==name),None)
entries=direct(catalogue,'selectionEntries')
assert entries is not None
units=list(entries)
names={e.get('name') for e in units}
for required in ('Tactical Squad','Assault Squad','Devastator Squad','Captain','Librarian'):
    assert required in names, f'Missing 2013 codex entry: {required}'
for forbidden in ('Rogal Dorn Battle Tank','Primaris Intercessors','Redemptor Dreadnought','Repulsor'):
    assert forbidden not in names, f'Anachronistic unit: {forbidden}'
assert len(units)==66, f'Expected 66 top-level entries after excluding allied detachment; got {len(units)}'
assert catalogue.get('gameSystemId')==gst.get('id')
assert report['unsupported'].get('excluded_allied_detachment')==1
assert not report['unresolvedLinks'], 'Unresolved catalogue links'
assert report['convertedProfiles']>=451
assert report['convertedRules']>=222
assert report['convertedLinks']>=277
foc={'ac8d-efba-1884-d3ad','default-category','978c-e18f-8aeb-f4c1',
     '74fe-37c3-fbbf-849e','9260-7d57-be5c-bd52','168b-a772-94f7-83f5'}
for entry in units:
    for link in entry.iter():
        if tag(link)=='categoryLink':
            assert link.get('targetId') in foc, (entry.get('name'),link.get('targetId'))
# Audit converted profiles against the companion GST, not just the baseline GST.
companion=ET.parse(sys.argv[4]).getroot() if len(sys.argv)>4 else gst
profile_types={x.get('id'):x for x in companion.iter() if tag(x)=='profileType'}
profile_errors=[]
for profile in catalogue.iter():
    if tag(profile)!='profile': continue
    ptype=profile_types.get(profile.get('typeId'))
    if ptype is None:
        profile_errors.append((profile.get('name'),'missing type',profile.get('typeId')))
        continue
    char_ids={x.get('id') for x in ptype.iter() if tag(x)=='characteristicType'}
    for characteristic in profile.iter():
        if tag(characteristic)=='characteristic' and characteristic.get('typeId') not in char_ids:
            profile_errors.append((profile.get('name'),'missing characteristic',characteristic.get('typeId')))
assert not profile_errors, f'Broken profile type references: {profile_errors[:15]} (total {len(profile_errors)})'
# Every emitted modifier must target an actual cost/constraint, and each
# condition must have a supported 2.x operator and a known selection target.
ids={e.get('id') for e in catalogue.iter() if e.get('id')}
ids.update(e.get('id') for e in companion.iter() if e.get('id'))
cost_ids={e.get('typeId') for e in catalogue.iter() if tag(e)=='cost'}
cost_ids.update(e.get('id') for e in companion.iter() if tag(e)=='costType')
modifier_errors=[]
for owner in catalogue.iter():
    modifiers=direct(owner,'modifiers')
    if modifiers is None: continue
    owner_constraints={e.get('id') for e in owner.iter() if tag(e)=='constraint'}
    for modifier in modifiers:
        field=modifier.get('field')
        if field not in owner_constraints and field not in cost_ids:
            modifier_errors.append(('target',owner.get('name'),field))
        for cond in modifier.iter():
            if tag(cond)!='condition': continue
            if cond.get('type') not in ('atLeast','atMost','equalTo','notEqualTo'):
                modifier_errors.append(('operator',owner.get('name'),cond.get('type')))
            if cond.get('childId') not in ids:
                modifier_errors.append(('condition target',owner.get('name'),cond.get('childId')))
assert not modifier_errors, f'Invalid modifiers: {modifier_errors[:15]} (total {len(modifier_errors)})'
print('PASS: source-era units, FOC references, counts, resolved links, profile types, and modifier targets.')
print('NOT A PLAYABILITY CERTIFICATION: conditional modifiers and roster legality remain unvalidated.')
