"""Validate a curated evidence graph and rebuild deterministic research outputs."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIMENSIONS = {'transparency','accountability','interoperability','human_oversight','participation'}

def load():
    return tuple(json.loads((ROOT/'data'/name).read_text()) for name in ('sources.json','claims.json','synthesis.json'))

def unique(items):
    ids=[x['id'] for x in items]
    if len(ids)!=len(set(ids)): raise ValueError('Duplicate ID')
    return set(ids)

def validate(sources, claims, synthesis):
    source_ids=unique(sources); claim_ids=unique(claims); unique(synthesis)
    for source in sources:
        if not source['url'].startswith('https://') or not source.get('version'): raise ValueError('Missing source URL/version')
    for claim in claims:
        if claim['source'] not in source_ids: raise ValueError('Unknown source')
        if not claim.get('locator','').strip(): raise ValueError('Missing locator')
        if claim['dimension'] not in DIMENSIONS: raise ValueError('Unknown dimension')
        if claim.get('kind')!='source_summary': raise ValueError('Unlabelled evidence kind')
        if claim.get('review') not in ('pending','reviewed'): raise ValueError('Missing review state')
        if claim['review']=='reviewed' and not claim.get('reviewer'): raise ValueError('Reviewer required')
    for item in synthesis:
        if not item['evidence'] or any(x not in claim_ids for x in item['evidence']): raise ValueError('Broken evidence link')
        if item.get('kind')!='analyst_inference': raise ValueError('Inference must be labelled')
        if not item.get('question'): raise ValueError('Missing unresolved question')
    return True

def build():
    sources, claims, synthesis=load(); validate(sources,claims,synthesis)
    out=ROOT/'docs';out.mkdir(exist_ok=True)
    lookup={s['id']:s for s in sources}
    lines=['# Evidence crosswalk','', 'Curated summaries; independent human review pending. Empty intersections mean not coded in this sample, not absent from the framework.','', '| ID | Dimension | Summary | Source and locator |','|---|---|---|---|']
    for c in claims:
        s=lookup[c['source']]
        lines.append(f"| {c['id']} | {c['dimension']} | {c['claim']} | [{s['id']}]({s['url']}) — {c['locator']} |")
    (out/'crosswalk.md').write_text('\n'.join(lines)+'\n')
    with (out/'crosswalk.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(claims[0]),lineterminator='\n');writer.writeheader();writer.writerows(claims)
    lines=['# Policy brief: a pilot for evidence interoperability','','Independent portfolio analysis. Scope: three selected international texts, not a global regulatory survey.','','## Decision proposed','','Pilot a common evidence record for one low-risk administrative AI use case. Keep source requirements and review decisions visible rather than assigning a single compliance score.']
    for s in synthesis:
        lines += ['', '## '+s['title'],'',s['inference'],'','Evidence: '+', '.join('['+x+'](crosswalk.md)' for x in s['evidence'])+'. Analyst inference; review pending.','','Consultation question: '+s['question']]
    lines += ['','## Practical next step','','Use the consultation protocol to test the draft record with policy, technical and affected-community perspectives. Record dissent and missing evidence. Add national and regional law before making any jurisdiction-specific recommendation. No expert workshop or consensus finding is claimed.']
    (out/'policy-brief.md').write_text('\n'.join(lines)+'\n')
    lines=['# Concept map','','```mermaid','flowchart LR']
    for c in claims: lines.append(f'  {c["source"]} --> {c["id"]}["{c["id"]}: {c["dimension"]}"]')
    for s in synthesis:
        for e in s['evidence']: lines.append(f'  {e} --> {s["id"]}["{s["id"]}: analyst inference"]')
    lines += ['```','','Edges show citation relationships, not legal equivalence or causal proof.']
    (out/'concept-map.md').write_text('\n'.join(lines)+'\n')
    print(f'Validated {len(sources)} sources, {len(claims)} claims and {len(synthesis)} labelled inferences; rebuilt four outputs.')

if __name__=='__main__': build()
