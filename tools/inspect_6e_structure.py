#!/usr/bin/env python3
"""Inspect 2013 Space Marines and 6th edition GST structure before conversion."""
import io,sys,zipfile,xml.etree.ElementTree as ET
z=zipfile.ZipFile(sys.argv[1])
cat=ET.fromstring(z.read('Space Marines - Codex.cat'))
gst_name=next(n for n in z.namelist() if n.endswith('.gst'))
gst=ET.fromstring(z.read(gst_name))
def tag(e): return e.tag.rsplit('}',1)[-1]
def sections(e): return [(tag(x),len(x)) for x in e]
def ids(e): return {x.get('id') for x in e.iter() if x.get('id')}
print('SOURCE GST',gst_name,gst.attrib,sections(gst))
print('SPACE MARINES',cat.attrib,sections(cat))
for group in cat:
 if tag(group) in ('selectionEntries','entryLinks','sharedSelectionEntries','sharedSelectionEntryGroups','selectionEntryGroups','catalogueLinks','categoryEntries'):
  print('CAT SECTION',tag(group),'count',len(group),'sample',[(tag(x),x.get('name'),x.get('type')) for x in list(group)[:15]])
print('SOURCE CATEGORIES',[(x.get('name'),x.get('id')) for x in gst.iter() if tag(x)=='categoryEntry'][:35])
print('CAT CATEGORY LINKS',[(x.get('name'),x.get('targetId')) for x in cat.iter() if tag(x)=='categoryLink'][:25])
print('CAT ROOT LINKS',[(x.get('name'),x.get('targetId')) for x in cat if tag(x)=='entryLink'][:10])
print('CAT UNIT ENTRIES',[(x.get('name'),x.get('type')) for x in cat.iter() if tag(x)=='selectionEntry' and x.get('type') in ('unit','model')][:30])
missing={x.get('targetId') for x in cat.iter() if x.get('targetId')}-ids(cat)-ids(gst)
print('UNRESOLVED IN SOURCE',len(missing),sorted(missing)[:30])
print('SOURCE GST FORCES',[(x.get('name'),x.get('id')) for x in gst.iter() if tag(x)=='forceEntry'][:12])
