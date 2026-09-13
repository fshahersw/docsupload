"""Import a licensed settlement snapshot as attributed, unverified source records.

Standard library only. No network, claim submission, model use or input deletion.
"""
from pathlib import Path
from datetime import date,datetime,timezone
from urllib.parse import urlsplit,urlunsplit
import json,hashlib,argparse,collections,re,shutil

class InputError(ValueError):pass
def digest(b):return hashlib.sha256(b).hexdigest()
def row_hash(row):return digest(json.dumps(row,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
def read(path):
 def pairs(values):
  d={}
  for k,v in values:
   if k in d:raise InputError('Duplicate JSON key: '+k)
   d[k]=v
  return d
 try:return json.loads(Path(path).read_text(encoding='utf-8-sig'),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError('Invalid JSON constant')))
 except (UnicodeError,json.JSONDecodeError) as e:raise InputError('Invalid UTF-8 JSON') from e
def iso(v):
 if v is None:return None
 if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v):raise InputError('Expected ISO date or null')
 try:date.fromisoformat(v)
 except ValueError as e:raise InputError('Invalid calendar date') from e
 return v
def canonical_url(value):
 if not isinstance(value,str) or value!=value.strip() or re.search(r'[^\S ]|[\x00-\x1f\x7f\\]',value) or not re.match(r'^https?://[^\s/?#]+(?:[/?#]|$)',value,re.I):raise InputError('Invalid URL text')
 try:
  p=urlsplit(value);port=p.port
 except ValueError as e:raise InputError('Invalid URL authority') from e
 if p.scheme not in ('http','https') or not p.hostname or p.username is not None or p.password is not None or port:raise InputError('Expected credential-free public web URL')
 if '.' not in p.hostname or ':' in p.hostname or re.fullmatch(r'\d+(\.\d+){3}',p.hostname) or p.hostname.endswith(('.local','.localhost')):raise InputError('Expected public domain')
 return urlunsplit((p.scheme,p.hostname.lower(),p.path.rstrip('/') or '/',p.query,p.fragment)).replace(' ','%20')
def validate(row):
 if not isinstance(row,dict):raise InputError('Every settlement must be an object')
 for k in ['title','url','@id','settlement_type','status','proof_required','verification_status']:
  if not isinstance(row.get(k),str) or not row[k].strip():raise InputError('Missing/non-text '+k)
 canonical_url(row['url']);canonical_url(row['@id'])
 for k in ['claim_deadline','last_verified']:iso(row.get(k))
 for k in ['category','estimated_payout','official_claim_url','official_settlement_url']:
  if row.get(k) is not None and not isinstance(row[k],str):raise InputError('Expected text or null: '+k)
 states=row.get('applicable_states')
 if not isinstance(states,list) or any(not isinstance(s,str) or not re.fullmatch('[A-Z]{2}',s) for s in states):raise InputError('Expected two-letter state codes')
 if type(row.get('accepted_official_evidence')) is not bool:raise InputError('Evidence flag must be boolean')
def normalize_dataset(data,references,source_sha):
 if not isinstance(data,dict) or not isinstance(data.get('settlements'),list):raise InputError('Expected dataset.settlements array')
 rows=data['settlements']
 if type(data.get('count')) is not int or data['count']!=len(rows):raise InputError('Declared count differs from source row count')
 if not isinstance(references,list):raise InputError('Expected reference array')
 refs={}
 for r in references:
  if not isinstance(r,dict) or not r.get('publisher_url'):raise InputError('Reference has no exact publisher URL')
  key=canonical_url(r['publisher_url'])
  if key in refs:raise InputError('Ambiguous reference join')
  refs[key]=r
 by_hash={};groups=collections.defaultdict(list);out=[]
 for i,row in enumerate(rows,1):
  validate(row);key=canonical_url(row['url']);h=row_hash(row)
  if h in by_hash:by_hash[h]['source_positions'].append(i);continue
  notes=[]
  for field in ['official_claim_url','official_settlement_url']:
   if row.get(field):
    try:canonical_url(row[field])
    except InputError:notes.append(field+' is retained as source text but cannot be opened as a public web link.')
  if canonical_url(row['@id'])!=key:notes.append('The publisher @id and record URL differ.')
  if row['verification_status']=='needs_recheck':notes.append('The publisher marks this record for rechecking.')
  if row['verification_status']=='third_party_only':notes.append('The publisher identifies third-party-only verification.')
  ref=refs.get(key)
  if ref and isinstance(ref.get('publisher_snapshot'),dict):
   changed=[k for k,v in ref['publisher_snapshot'].items() if row.get(k)!=v]
   if changed:notes.append('Publisher fields changed since the attached review: '+', '.join(sorted(changed))+'. The dated review has not been refreshed.')
  record={'id':'settlement-'+digest(key.encode())[:20],'publisher':row,'publisher_record_sha256':h,'source_positions':[i],'source_snapshot_sha256':source_sha,'review':ref,'quality_notes':notes}
  out.append(record);by_hash[h]=record;groups[key].append(record)
 # A shared source URL with different payloads is not silently overwritten.
 for group in groups.values():
  if len(group)>1:
   for r in group:r['id']+='-'+r['publisher_record_sha256'][:10];r['quality_notes'].append('Conflicting payloads share a publisher URL; retained as separate source versions.')
 ids={r['id'] for r in out}
 if len(ids)!=len(out):raise InputError('Stable ID collision')
 used={canonical_url(r['publisher']['url']) for r in out if r['review']};unmatched=[r['id'] for k,r in refs.items() if k not in used]
 if unmatched:raise InputError('Reviewed reference(s) missing from source: '+', '.join(unmatched))
 metadata={k:data.get(k) for k in ['name','description','source','url','generated','dateModified','license','attribution','creator','publisher','variableMeasured']}
 metadata.update(schema_version='1.0.0',record_count=len(out),source_row_count=len(rows),source_sha256=source_sha,provider='SettleSignal',attribution='Data: SettleSignal (settlesignal.com) — https://settlesignal.com/',records_are_independently_verified=False,reviewed_reference_count=len(used),status_policy='Publisher status and evidence fields are assertions. Source reviews are bounded, dated overlays; neither is a present eligibility or payment guarantee.',geography_policy='An empty applicable_states array means nationwide according to this feed. It is not a complete class definition or court jurisdiction.',benefit_policy='estimated_payout is preserved as source text. It may mix fund totals, maximum reimbursements, pro rata estimates and noncash benefits; no dollar value is normalized or aggregated.',date_policy='Claim dates have no assumed cutoff time or time zone. UI date comparisons use the visible as-of date; feed and review snapshots keep their own dates.')
 return {'schema_version':'1.0.0','metadata':metadata,'records':out}
def write(path,data):Path(path).write_bytes((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',required=True);p.add_argument('--references',required=True);p.add_argument('--output',required=True);a=p.parse_args()
 source=Path(a.input).resolve();refs=Path(a.references).resolve();output=Path(a.output).resolve()
 for name in ['catalog.json','catalog-data.js','publisher-feed.json','IMPORT-RECEIPT.json']:
  if output/name in [source,refs]:raise InputError('Output would overwrite an input')
 raw=source.read_bytes();result=normalize_dataset(read(source),read(refs),digest(raw));output.mkdir(parents=True,exist_ok=True)
 write(output/'catalog.json',result);(output/'catalog-data.js').write_bytes(('globalThis.SETTLEMENT_CATALOG = '+json.dumps(result,ensure_ascii=False).replace('\u2028','\\u2028').replace('\u2029','\\u2029')+';\n').encode())
 (output/'publisher-feed.json').write_bytes(raw)
 receipt={'imported_at':datetime.now(timezone.utc).isoformat(),'source_sha256':digest(raw),'references_sha256':digest(refs.read_bytes()),'raw_input_rows':len(read(source)['settlements']),'canonical_records':len(result['records']),'exact_duplicate_rows':sum(len(r['source_positions'])-1 for r in result['records']),'review_joins':result['metadata']['reviewed_reference_count'],'all_source_fields_retained':True,'network_requests':0,'new_independent_reviews':0,'source_original_unchanged':digest(source.read_bytes())==digest(raw)}
 write(output/'IMPORT-RECEIPT.json',receipt);print(json.dumps(receipt))
if __name__=='__main__':
 try:main()
 except InputError as e:raise SystemExit('Input error: '+str(e))
