#!/usr/bin/env python3
"""Validate documentation structure; this does not execute ComfyUI."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

root = Path(__file__).resolve().parents[1]
groups = json.loads((root / 'data/experiments.json').read_text())
nodes = json.loads((root / 'data/nodes.json').read_text())
errors = []
by_id = {g['id']: g for g in groups}
node_ids = {n['class_name'] for n in nodes}
cards = json.loads((root / 'data/node-experiments.json').read_text())
schemas = json.loads((root / 'data/node-schemas.json').read_text())
if len(cards) != 639 or {n['class_name'] for n in cards} != node_ids:
    errors.append('Expected one experiment card for each of 639 nodes')
if len(schemas) != 639 or {n['class_name'] for n in schemas} != node_ids:
    errors.append('Schema coverage differs from node index')
for card in cards:
    p = root / card['path']
    if not p.is_file():
        errors.append(f'Missing node card: {card["path"]}')
        continue
    if not card['cases']:
        errors.append(f'Empty cases: {card["class_name"]}')
    for case in card['cases']:
        for field in ('change', 'expected', 'observe'):
            if not case.get(field, '').strip():
                errors.append(f'Missing concrete case field: {card["class_name"]}/{field}')
    if card['status'] != 'not_run':
        errors.append(f'Design generation must not claim execution: {card["class_name"]}')
if len(groups) != len(by_id) or len(groups) != 78:
    errors.append('Expected 78 unique experiment groups')
if len(nodes) != len(node_ids) or len(nodes) != 639:
    errors.append('Expected 639 unique nodes')
membership = {}
for group in groups:
    path = root / group['path']
    if not path.is_file():
        errors.append(f'Missing experiment page: {group["path"]}')
    for name in group['nodes']:
        if name in membership:
            errors.append(f'Duplicate node membership: {name}')
        membership[name] = group['id']
    for dep in group['prerequisites']:
        if dep not in by_id:
            errors.append(f'Unknown prerequisite: {group["id"]} -> {dep}')
if set(membership) != node_ids:
    errors.append('Node coverage differs from experiment membership')
for node in nodes:
    if membership.get(node['class_name']) != node['experiment']:
        errors.append(f'Node assignment mismatch: {node["class_name"]}')
    page = root / by_id[node['experiment']]['path']
    if page.is_file() and f'`{node["class_name"]}`' not in page.read_text():
        errors.append(f'Node missing from its page: {node["class_name"]}')
done = set()
while len(done) < len(groups):
    ready = [g['id'] for g in groups if g['id'] not in done and set(g['prerequisites']) <= done]
    if not ready:
        errors.append('Prerequisite cycle or unresolved dependency')
        break
    done.update(ready)
link_count = 0
for page in root.rglob('*.md'):
    body = re.sub(r'```[\s\S]*?```', '', page.read_text())
    for raw in re.findall(r'\[[^\]]*\]\(([^)]+)\)', body):
        url = urlsplit(raw)
        if url.scheme or not url.path:
            continue
        link_count += 1
        dest = (page.parent / unquote(url.path)).resolve()
        if not dest.is_relative_to(root) or not dest.exists():
            errors.append(f'Broken relative link: {page.relative_to(root)} -> {raw}')
if errors:
    print('\n'.join(errors), file=sys.stderr)
    sys.exit(1)
print(f'PASS: {len(groups)} groups, {len(nodes)} nodes, {len(cards)} cards, {sum(len(c["cases"]) for c in cards)} cases, acyclic prerequisites, {link_count} relative links; no ComfyUI execution claimed')
