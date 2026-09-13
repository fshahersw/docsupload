"""Offline regression tests for retention, identity, review joins and malformed input."""
import copy,json,tempfile,unittest
from pathlib import Path
import import_catalog as importer

ROOT=Path(__file__).parent

class ImportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.feed=importer.read(ROOT/'publisher-feed.json')
  cls.catalog=importer.read(ROOT/'catalog.json')
  cls.refs=[r['review'] for r in cls.catalog['records'] if r['review']]
 def normalized(self,feed=None,refs=None):
  return importer.normalize_dataset(feed or self.feed,self.refs if refs is None else refs,'a'*64)
 def small(self):
  f=copy.deepcopy(self.feed);f['settlements']=f['settlements'][:1];f['count']=1;return f
 def test_all_original_fields_and_occurrences_retained(self):
  self.assertEqual(len(self.catalog['records']),848)
  positions=[]
  for record in self.catalog['records']:
   for pos in record['source_positions']:
    positions.append(pos);self.assertEqual(record['publisher'],self.feed['settlements'][pos-1]);self.assertEqual(record['publisher_record_sha256'],importer.row_hash(self.feed['settlements'][pos-1]))
  self.assertEqual(sorted(positions),list(range(1,849)))
 def test_source_byte_hash(self):
  self.assertEqual(importer.digest((ROOT/'publisher-feed.json').read_bytes()),self.catalog['metadata']['source_sha256'])
 def test_nine_exact_review_joins(self):
  out=self.normalized();self.assertEqual(sum(bool(r['review']) for r in out['records']),9)
  for r in out['records']:
   if r['review']:self.assertEqual(r['publisher']['url'],r['review']['publisher_url'])
 def test_ids_stable_under_reorder(self):
  f=copy.deepcopy(self.feed);f['settlements'].reverse()
  before={r['publisher']['url']:r['id'] for r in self.normalized()['records']}
  self.assertEqual(before,{r['publisher']['url']:r['id'] for r in self.normalized(f)['records']})
 def test_exact_duplicates_keep_source_positions(self):
  f=self.small();f['settlements'].append(copy.deepcopy(f['settlements'][0]));f['count']=2
  rows=self.normalized(f,[])['records'];self.assertEqual(len(rows),1);self.assertEqual(rows[0]['source_positions'],[1,2])
 def test_conflicting_same_url_is_preserved(self):
  f=self.small();r=copy.deepcopy(f['settlements'][0]);r['title']='A separate reported version';f['settlements'].append(r);f['count']=2
  rows=self.normalized(f,[])['records'];self.assertEqual(len(rows),2);self.assertEqual(len({r['id'] for r in rows}),2);self.assertTrue(all('Conflicting' in r['quality_notes'][-1] for r in rows))
 def test_shared_official_site_is_not_case_deduplication(self):
  f=self.small();r=copy.deepcopy(f['settlements'][0]);r['url']=r['@id']='https://settlesignal.com/different-program';f['settlements'].append(r);f['count']=2
  self.assertEqual(len(self.normalized(f,[])['records']),2)
 def test_changed_feed_preserves_dated_review(self):
  f=copy.deepcopy(self.feed);ref=self.refs[0];row=next(r for r in f['settlements'] if r['url']==ref['publisher_url']);row['status']='Changed provider status'
  record=next(r for r in self.normalized(f)['records'] if r['review'] and r['review']['id']==ref['id'])
  self.assertEqual(record['review'],ref);self.assertTrue(any('changed since' in n for n in record['quality_notes']))
 def test_missing_or_ambiguous_review_join_fails(self):
  for refs in [self.refs+[self.refs[0]],[dict(self.refs[0],publisher_url='https://settlesignal.com/missing-case')]]:
   with self.subTest(refs=len(refs)),self.assertRaises(importer.InputError):self.normalized(refs=refs)
 def test_count_mismatch_fails(self):
  f=self.small();f['count']=2
  with self.assertRaises(importer.InputError):self.normalized(f,[])
 def test_invalid_dates_fail_without_timezone_coercion(self):
  for value in ['2026-02-30','2026-2-01','2026-09-13T00:00:00Z',0,True]:
   with self.subTest(value=value),self.assertRaises(importer.InputError):importer.iso(value)
  self.assertEqual(importer.iso('2024-02-29'),'2024-02-29');self.assertIsNone(importer.iso(None))
 def test_url_policy_and_space_encoding(self):
  self.assertEqual(importer.canonical_url('https://example.com/Claim Form.pdf'),'https://example.com/Claim%20Form.pdf')
  for u in ['javascript:alert(1)','https://example.com\n/x','https://name:pass@example.com/x','https://localhost/a','https://127.0.0.1/x','https://example.com\\x','https://example.com:8080','No claim form currently available','https://exa mple.com/path']:
   with self.subTest(url=u),self.assertRaises(importer.InputError):importer.canonical_url(u)
 def test_prose_claim_link_and_long_benefits_are_not_dropped(self):
  record=self.catalog['records'][762];self.assertEqual(record['publisher']['official_claim_url'],'No claim form currently available');self.assertTrue(any('source text' in n for n in record['quality_notes']))
  source=max(self.feed['settlements'],key=lambda r:len(r['estimated_payout'] or ''));result=next(r for r in self.catalog['records'] if r['publisher']['url']==source['url']);self.assertEqual(result['publisher']['estimated_payout'],source['estimated_payout'])
 def test_state_and_boolean_types_are_not_coerced(self):
  for key,value in [('applicable_states',['New York']),('accepted_official_evidence','true'),('title',None)]:
   row=copy.deepcopy(self.feed['settlements'][0]);row[key]=value
   with self.subTest(key=key),self.assertRaises(importer.InputError):importer.validate(row)
 def test_duplicate_keys_and_nonfinite_json_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.json'
   for text in ['{"count":1,"count":2}','{"count":NaN}']:
    p.write_text(text)
    with self.assertRaises(importer.InputError):importer.read(p)
 def test_null_empty_and_unknown_fields_preserved(self):
  f=self.small();r=f['settlements'][0];r.update(estimated_payout=None,category='',applicable_states=[],future_field={'arbitrary':'retained'})
  self.assertEqual(self.normalized(f,[])['records'][0]['publisher'],r)

if __name__=='__main__':unittest.main()
