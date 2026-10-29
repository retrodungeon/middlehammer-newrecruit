#!/usr/bin/env python3
"""Produce a machine-readable 2013 Space Marines integration readiness decision.

Exit 0 for a generated experimental bundle; --strict exits nonzero until
all conversion blockers are resolved. Never labels an untested roster playable.
"""
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

def local(x): return x.tag.rsplit('}', 1)[-1]
p=argparse.ArgumentParser()
p.add_argument('catalogue',type=Path)
p.add_argument('report',type=Path)
p.add_argument('gst',type=Path)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--strict',action='store_true')
args=p.parse_args()
cat=ET.parse(args.catalogue).getroot()
gst=ET.parse(args.gst).getroot()
report=json.loads(args.report.read_text())
warnings=report.get('unsupported',{})
blocker_keys=[
 'conditional_modifiers_pending','conditional_groups_pending',
 'unconverted_profile_modifiers','unconverted_link_modifiers',
 'modifier_target_constraint_absent','modifier_target_cost_absent',
 'unresolved_link_targets',
]
blockers={k:warnings.get(k,0) for k in blocker_keys if warnings.get(k,0)}
blockers.update({k:v for k,v in warnings.items()
                 if k.startswith(('unsupported_modifier_','unconverted_'))
                 and v and k not in blockers})
root=next((x for x in cat if local(x)=='selectionEntries'),None)
root_entries=list(root) if root is not None else []
categories={x.get('name'): [y.get('targetId') for y in x.iter() if local(y)=='categoryLink']
            for x in root_entries}
special=[x.get('name') for x in root_entries if not categories[x.get('name')]]
if special: blockers['special_entries_needing_FOC_or_eligibility_review']=len(special)
if cat.get('gameSystemId')!=gst.get('id'): blockers['incorrect_game_system']=1
readiness={
 'catalogue':cat.get('name'),'status':'NOT_READY' if blockers else 'STRUCTURALLY_READY_REQUIRES_MANUAL_ROSTER_TEST',
 'root_entries':len(root_entries),'blockers':blockers,
 'special_entries':special,
 'manual_checks':['2013 codex points and squad composition','Chapter Tactics and character restrictions',
                  'legal and illegal New Recruit roster tests','Middlehammer 5e FOC integration',
                  'no regression in existing Guard/Chaos catalogues'],
 'production_published':False,
}
args.output.parent.mkdir(parents=True,exist_ok=True)
args.output.write_text(json.dumps(readiness,indent=2)+'\n')
print(json.dumps(readiness,indent=2))
if args.strict and blockers: raise SystemExit('Release gate blocked: unresolved rules or category exceptions')
