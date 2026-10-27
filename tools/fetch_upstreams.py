#!/usr/bin/env python3
"""Download source snapshots locally for analysis (not redistribution)."""
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'sources/upstreams.json').read_text(encoding='utf-8'))
cache = ROOT / 'upstream-cache'
cache.mkdir(exist_ok=True)
for edition, info in manifest['editions'].items():
    repo = info['repository']
    ref = info.get('branch')
    if not ref:
        print(f'{edition}e: archived release {info.get("release")} requires separate extraction')
        continue
    url = f'https://api.github.com/repos/{repo}/zipball/{ref}'
    target = cache / f'{edition}e.zip'
    request = urllib.request.Request(url, headers={'User-Agent': 'middlehammer-upstream-audit', 'Accept': 'application/vnd.github+json'})
    with urllib.request.urlopen(request, timeout=90) as response, target.open('wb') as out:
        import shutil
        shutil.copyfileobj(response, out)
    print(f'{edition}e: downloaded {repo} -> {target}')
