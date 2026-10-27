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
print('PASS: source-era units, FOC references, counts, and resolved links.')
print('NOT A PLAYABILITY CERTIFICATION: conditional modifiers and roster legality remain unvalidated.')
