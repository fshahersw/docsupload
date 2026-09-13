"""Exact, offline lookup into the supplied OLRC release. Python standard library only.

Example: python resolve_citation.py "28 U.S.C. 1332(d)(2)"
This is not a Bluebook validator, citator, deadline calculator, or good-law service.
"""
from pathlib import Path
import argparse,json,re

def parse(value):
    value=value.strip().replace('\u00a0',' ')
    pin=r'((?:\s*\([A-Za-z0-9]+\))*)'
    m=re.fullmatch(r'(\d+)\s+U\.?\s*S\.?\s*C\.?\s*(?:§|sec(?:tion)?\.?)?\s*(\d+[A-Za-z]?)'+pin,value,re.I)
    if m:return {'key':f'USC:{int(m[1])}:{m[2]}','pin':re.findall(r'\(([^)]+)\)',m[3])}
    patterns=[('FRCP',r'(?:FRCP|Fed\.?\s*R\.?\s*Civ\.?\s*P\.?)'),('FRAP',r'(?:FRAP|Fed\.?\s*R\.?\s*App\.?\s*P\.?)'),('FRE',r'(?:FRE|Fed\.?\s*R\.?\s*Evid\.?)'),('SUPP-ADM',r'(?:Supplemental Admiralty Rule|SUPP-ADM)'),('SUPP-SSA',r'(?:Supplemental Social Security Rule|SUPP-SSA)')]
    for family,p in patterns:
        m=re.fullmatch(p+r'\s*(?:Rule\s*)?([0-9]+[A-Za-z]?(?:\.[0-9]+)?|[A-G])'+pin,value,re.I)
        if m:return {'key':family+':'+m[1].upper(),'pin':re.findall(r'\(([^)]+)\)',m[2])}
    return None

def resolve(value,records):
    p=parse(value)
    if p is None:return {'status':'unsupported','message':'One supported U.S. Code or federal rule citation required; no fuzzy or range resolution.'}
    matches=[r for r in records if r['citation_key'].lower()==p['key'].lower()]
    if not matches:return {'status':'not_found','parsed':p,'matches':[]}
    if len(matches)>1:return {'status':'ambiguous','parsed':p,'matches':matches}
    record=matches[0]
    if p['pin']:
        subs=[s for s in record['subsections'] if s['path']==p['pin']]
        if len(subs)!=1:return {'status':'ambiguous_subsection' if subs else 'subsection_not_found','parsed':p,'matches':matches}
        if record.get('source_structure_issues'):return {'status':'source_structure_uncertain','parsed':p,'matches':matches,'message':'Publisher numbering/nesting issues; use full provision and original PDF. Exact pinpoint not asserted.'}
        return {'status':'resolved','parsed':p,'record':record,'subsection':subs[0]}
    return {'status':'resolved','parsed':p,'record':record}

def load(path):
    with Path(path).open(encoding='utf-8') as f:return [json.loads(line) for line in f if line.strip()]

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('citation')
    parser.add_argument('--index',default=Path(__file__).with_name('PRIMARY-LAW.jsonl'))
    args=parser.parse_args()
    print(json.dumps(resolve(args.citation,load(args.index)),ensure_ascii=False,indent=2))
