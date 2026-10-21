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
frontend = json.loads((root / 'data/frontend-experiments.json').read_text())
frontend_ids = {g['id'] for g in frontend}
if len(frontend) != len(frontend_ids):
    errors.append('Duplicate frontend experiment IDs')
frontend_cases = set()
for group in frontend:
    page = root / group['path']
    if not page.is_file() or not (root / group['setup']).is_file():
        errors.append(f'Missing frontend page or setup: {group["id"]}')
        continue
    if group['status'] != 'not_run':
        errors.append(f'Frontend design must not claim execution: {group["id"]}')
    if not group['cases']:
        errors.append(f'Empty frontend cases: {group["id"]}')
    for case_id in group['cases']:
        if case_id in frontend_cases:
            errors.append(f'Duplicate frontend case: {case_id}')
        frontend_cases.add(case_id)
        rows = [line for line in page.read_text().splitlines() if line.startswith(f'| {case_id} ')]
        if len(rows) != 1 or len(rows[0].split('|')) != 6 or not all(x.strip() for x in rows[0].split('|')[1:-1]):
            errors.append(f'Frontend case requires operation, expectation and observation: {case_id}')
    for dep in group['prerequisites']:
        if dep not in frontend_ids:
            errors.append(f'Unknown frontend prerequisite: {group["id"]} -> {dep}')
frontend_done = set()
while len(frontend_done) < len(frontend_ids):
    ready = [g['id'] for g in frontend if g['id'] not in frontend_done and set(g['prerequisites']) <= frontend_done]
    if not ready:
        errors.append('Frontend prerequisite cycle or unresolved dependency')
        break
    frontend_done.update(ready)
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
print(f'PASS: {len(frontend)} frontend groups, {len(frontend_cases)} cases, acyclic prerequisites; no RunningHub execution claimed')
