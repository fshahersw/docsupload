"""Synthetic engineering fixtures, never legal evidence or model-quality scores."""
import copy
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from corpus_tools import (InputError, canonical_url, classify_http, normalize_registry,
                          plan_scan, plan_digest, text_hash, scan_coverage, verify_findings, csv_text, read_json)


def docs(text='The device failed on March 3. The witness did not recall a warning.'):
    return [{'document_id':'doc-1','matter_id':'test-matter','access_scope':'case-team-1',
             'source_version':'v1','sha256':'a'*64,'expected_page_count':1,
             'pages':[{'page':1,'status':'complete','text':text}]}]


def cite():
    return {'document_id':'doc-1','matter_id':'test-matter','access_scope':'case-team-1',
            'source_version':'v1','source_sha256':'a'*64,'page':1,'quote':'did not recall a warning'}


class RegistryTests(unittest.TestCase):
    def test_tracking_only_dedup(self):
        r=normalize_registry([{'url':'https://example.org/x?utm_source=x&a=1'}, {'url':'https://EXAMPLE.org:443/x?a=1'}])
        self.assertEqual((r['unique_count'],r['duplicate_count']),(1,1))
        self.assertEqual(len(r['records'][0]['variants']),2)

    def test_statute_anchor_is_not_lost(self):
        r=normalize_registry([{'url':'https://example.org/law#s1'}, {'url':'https://example.org/law#s2'}])
        self.assertEqual(r['unique_count'],2)

    def test_significant_query_order_and_case(self):
        self.assertEqual(canonical_url('HTTPS://Example.org:443/Case?q=A&q=B'), 'https://example.org/Case?q=A&q=B')

    def test_query_bytes_and_bare_flags_are_preserved(self):
        query='signature=a%2fb%20c&flag&value=%FF&value=+&x=%2F'
        self.assertEqual(canonical_url('https://example.org/x?'+query), 'https://example.org/x?'+query)
        self.assertNotEqual(canonical_url('https://example.org/x?q=a%20b'), canonical_url('https://example.org/x?q=a+b'))
        self.assertEqual(canonical_url('https://example.org/x?x=%2f&utm_source=a&flag'), 'https://example.org/x?x=%2f&flag')

    def test_zero_port_is_not_collapsed_to_default(self):
        self.assertEqual(canonical_url('https://example.org:0/x'), 'https://example.org:0/x')

    def test_empty_credentials_and_invalid_authority_rejected(self):
        for url in ['https://@example.org/x','https://example .org/x','https://example.org\\@other.org/x','https://example.org/x\x7f']:
            with self.subTest(url=url),self.assertRaises(InputError):canonical_url(url)

    def test_registry_and_http_shapes_are_explicit(self):
        for rows in [None,{},'text']:
            with self.subTest(rows=rows),self.assertRaises(InputError):normalize_registry(rows)
        for status in ['200',True,200.5,99,600]:
            with self.subTest(status=status),self.assertRaises(InputError):classify_http(status)

    def test_unsafe_urls(self):
        for value in ['javascript:alert(1)','file:///C:/secret','https://user:secret@example.org','https://example.org:\\bad','https://example.org/\nsecret']:
            with self.subTest(value=value), self.assertRaises(InputError): canonical_url(value)

    def test_http_status_is_not_waf_or_content_verification(self):
        self.assertEqual(classify_http(403),'access_denied_reason_unknown')
        self.assertEqual(classify_http(429),'rate_limited')
        self.assertEqual(classify_http(503),'service_unavailable')
        self.assertEqual(classify_http(200),'http_success_content_not_verified')
        self.assertEqual(classify_http(None,'tls'),'tls_error')
        self.assertEqual(classify_http(None,'timeout'),'timeout')


class ScanTests(unittest.TestCase):
    def test_tail_and_unicode_retained(self):
        source='a'*71+'\u2028tail 😀'
        p=plan_scan(docs(source),20,4)
        coverage=set()
        for c in p['chunks']:
            self.assertEqual(c['text'],source[c['start_character']:c['end_character']])
            coverage.update(range(c['start_character'],c['end_character']))
        self.assertEqual(coverage,set(range(len(source))))

    def test_partial_and_missing_pages_remain_gaps(self):
        d=docs();d[0]['expected_page_count']=3;d[0]['pages'][0]['status']='partial'
        p=plan_scan(d)
        results=[{'chunk_id':c['chunk_id'],'attempt':1,'status':'completed'} for c in p['chunks']]
        report=scan_coverage(p,results)
        self.assertFalse(report['complete']);self.assertEqual(len(report['extraction_gaps']),3)

    def test_cross_scope_hashes_never_merge(self):
        d=docs();e=copy.deepcopy(d[0]);e['document_id']='doc-2';e['access_scope']='different-team';d.append(e)
        p=plan_scan(d)
        self.assertEqual(p['document_count'],2);self.assertEqual(p['duplicate_candidates'],[])
        self.assertNotEqual(p['chunks'][0]['chunk_id'],p['chunks'][1]['chunk_id'])

    def test_same_scope_duplicates_are_only_candidates(self):
        d=docs();e=copy.deepcopy(d[0]);e['document_id']='doc-2';d.append(e)
        p=plan_scan(d);self.assertEqual(p['duplicate_candidates'],[['doc-1','doc-2']]);self.assertEqual(len(p['chunks']),2)

    def test_changed_source_version_gets_new_chunk_ids(self):
        d=docs();a=plan_scan(d);d[0]['source_version']='v2';b=plan_scan(d)
        self.assertNotEqual(a['chunks'][0]['chunk_id'],b['chunks'][0]['chunk_id'])

    def test_blank_verified_page_is_distinct_from_missing(self):
        p=plan_scan(docs(''));r=scan_coverage(p,[])
        self.assertTrue(r['complete']);self.assertIsNone(r['coverage_fraction'])

    def test_zero_selection_cannot_pass(self):
        with self.assertRaises(InputError):plan_scan([])
        with self.assertRaises(InputError):scan_coverage({'chunks':[],'chunk_count':0,'page_manifest':[]},[])

    def test_no_silent_page_dedup(self):
        d=docs();d[0]['pages'].append(copy.deepcopy(d[0]['pages'][0]))
        with self.assertRaises(InputError):plan_scan(d)

    def test_failed_attempt_can_recover(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id']
        r=scan_coverage(p,[{'chunk_id':cid,'attempt':1,'status':'timeout'}]);self.assertEqual(r['retry_chunk_ids'],[cid]);self.assertFalse(r['complete'])
        r=scan_coverage(p,[{'chunk_id':cid,'attempt':1,'status':'timeout'},{'chunk_id':cid,'attempt':2,'status':'completed'}]);self.assertTrue(r['complete'])

    def test_pending_and_exhausted_do_not_spin(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id']
        for status,attempt in [('pending',1),('failed',3)]:
            r=scan_coverage(p,[{'chunk_id':cid,'attempt':attempt,'status':status}]);self.assertFalse(r['complete']);self.assertEqual(r['retry_chunk_ids'],[])

    def test_old_pending_does_not_block_a_newer_failed_attempt(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id']
        r=scan_coverage(p,[{'chunk_id':cid,'attempt':1,'status':'pending'},{'chunk_id':cid,'attempt':2,'status':'failed'}])
        self.assertEqual(r['pending_chunk_ids'],[]);self.assertEqual(r['retry_chunk_ids'],[cid])

    def test_last_allowed_attempt_pending_is_not_exhausted(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id']
        r=scan_coverage(p,[{'chunk_id':cid,'attempt':3,'status':'pending'}])
        self.assertEqual(r['pending_chunk_ids'],[cid]);self.assertEqual(r['exhausted_chunk_ids'],[])

    def test_success_remains_durable_and_attempt_order_is_irrelevant(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id']
        r=scan_coverage(p,[{'chunk_id':cid,'attempt':3,'status':'failed'},{'chunk_id':cid,'attempt':1,'status':'completed'}])
        self.assertTrue(r['complete']);self.assertEqual(r['retry_chunk_ids'],[])

    def test_unknown_or_duplicate_attempts_are_rejected(self):
        p=plan_scan(docs());cid=p['chunks'][0]['chunk_id'];a={'chunk_id':cid,'attempt':1,'status':'completed'}
        with self.assertRaises(InputError):scan_coverage(p,[a,a])
        with self.assertRaises(InputError):scan_coverage(p,[{**a,'chunk_id':'invented'}])

    def test_invalid_chunking(self):
        for size,overlap in [(0,0),(10,10),(20,-1),(20,0.5),(20,True)]:
            with self.assertRaises(InputError):plan_scan(docs(),size,overlap)

    def test_tampered_plan_cannot_hide_dropped_tail(self):
        p=plan_scan(docs('A'*49),20,4);p['chunks'].pop();p['chunk_count']=len(p['chunks'])
        with self.assertRaises(InputError):scan_coverage(p,[])

    def test_tampered_text_or_scope_rejected(self):
        for field,value in [('text','changed text'),('access_scope','another-team')]:
            p=plan_scan(docs());p['chunks'][0][field]=value
            with self.assertRaises(InputError):scan_coverage(p,[])

    def test_document_and_page_scope_are_bound(self):
        for mutate in [lambda p:p.update(document_count=999),
                       lambda p:p['page_manifest'][0].update(text_characters=0),
                       lambda p:p['page_manifest'][0].update(extraction_status='invented')]:
            p=plan_scan(docs());mutate(p)
            with self.assertRaises(InputError):scan_coverage(p,[])

    def test_character_units_and_plan_digest_are_explicit(self):
        p=plan_scan(docs('A😀B'),2,0)
        self.assertEqual(p['character_unit'],'unicode_code_points')
        r=scan_coverage(p,[],expected_plan_sha256=p['plan_sha256'])
        self.assertTrue(r['matches_expected_plan'])
        with self.assertRaises(InputError):scan_coverage(p,[],expected_plan_sha256='0'*64)
        p['character_unit']='utf16_code_units'
        with self.assertRaises(InputError):scan_coverage(p,[])

    def test_malformed_plan_and_attempts_return_input_errors(self):
        for plan in [None,[],{}, {'chunks':[{}],'chunk_count':1,'page_manifest':[{}]}]:
            with self.subTest(plan=plan),self.assertRaises(InputError):scan_coverage(plan,[])
        p=plan_scan(docs())
        for attempts in [None,{},[None],[{'chunk_id':[],'attempt':1,'status':'completed'}]]:
            with self.subTest(attempts=attempts),self.assertRaises(InputError):scan_coverage(p,attempts)

    def test_malformed_source_hash_returns_input_error(self):
        for invalid in [None,1,[],{}]:
            d=docs();d[0]['sha256']=invalid
            with self.subTest(invalid=invalid),self.assertRaises(InputError):plan_scan(d)

    def test_plan_digest_is_not_a_substitute_for_structural_checks(self):
        # The caller can recompute an unkeyed digest. Invalid scope must still
        # fail, even if the checksum is internally consistent.
        for mutate in [lambda p:p.update(document_count=100),
                       lambda p:p['page_manifest'][0].update(extraction_status='unknown'),
                       lambda p:p['page_manifest'][0].update(page=True),
                       lambda p:p['chunks'][0].update(start_character=0.0),
                       lambda p:p['document_manifest'][0].update(access_scope='different-team')]:
            p=plan_scan(docs());mutate(p);p['plan_sha256']=plan_digest(p)
            with self.assertRaises(InputError):scan_coverage(p,[])

    def test_complete_page_cannot_be_dropped_from_recomputed_plan(self):
        d=docs();d[0]['expected_page_count']=2;d[0]['pages'].append({'page':2,'status':'complete','text':'A different second page'})
        p=plan_scan(d);p['page_manifest']=p['page_manifest'][:1]
        p['chunks']=[c for c in p['chunks'] if c['page']==1]
        p['chunk_count']=len(p['chunks']);p['expected_pages']=1;p['complete_extraction_pages']=1;p['plan_sha256']=plan_digest(p)
        with self.assertRaises(InputError):scan_coverage(p,[])

    def test_conflicting_overlap_cannot_hide_behind_valid_chunk_hashes(self):
        p=plan_scan(docs('abcdefghijklmnop'),8,3);c=p['chunks'][1]
        c['text']='X'+c['text'][1:];c['text_sha256']=text_hash(c['text'])
        identity=[c[k] for k in ('document_id','matter_id','access_scope','source_sha256','source_version')]
        identity += [c['page'],c['start_character'],c['end_character'],c['text_sha256']]
        c['chunk_id']='chunk-'+text_hash(json.dumps(identity))[:24];p['plan_sha256']=plan_digest(p)
        with self.assertRaises(InputError):scan_coverage(p,[])

    def test_blank_page_completeness_is_caller_declared_not_source_verification(self):
        report=scan_coverage(plan_scan(docs('')),[])
        self.assertTrue(report['complete']);self.assertFalse(report['source_bytes_verified'])
        self.assertIsNone(report['matches_expected_plan'])


class EvidenceTests(unittest.TestCase):
    def check(self,citation=None,status='supported'):
        return verify_findings(docs(),[{'finding_id':'f1','support_status':status,'citations':[citation if citation is not None else cite()]}])

    def test_literal_match_does_not_claim_legal_support(self):
        r=self.check();self.assertTrue(r['literal_grounding_passed']);self.assertFalse(r['legal_support_evaluated'])

    def test_empty_ledger_never_passes(self):
        r=verify_findings(docs(),[]);self.assertFalse(r['literal_grounding_passed']);self.assertTrue(r['empty_ledger'])

    def test_missing_source_does_not_become_supported(self):
        r=verify_findings(docs(),[{'finding_id':'f1','support_status':'supported','citations':[]}]);self.assertEqual(r['issues'][0]['reason'],'support_claim_without_evidence')

    def test_wrong_quote_or_page(self):
        for delta in [{'quote':'recall a warning not given'},{'page':2},{'quote':''}]:
            with self.subTest(delta=delta):self.assertFalse(self.check({**cite(),**delta})['literal_grounding_passed'])

    def test_source_hash_and_version_checked(self):
        for delta in [{'source_version':'v2'},{'source_sha256':'b'*64}]:
            self.assertEqual(self.check({**cite(),**delta})['issues'][0]['reason'],'source_version_or_hash_mismatch')

    def test_cross_matter_reference_rejected(self):
        self.assertEqual(self.check({**cite(),'matter_id':'other'})['issues'][0]['reason'],'scope_mismatch')

    def test_unverified_is_allowed_but_not_certified(self):
        r=verify_findings(docs(),[{'finding_id':'f1','support_status':'unverified','citations':[]}]);self.assertEqual(r['issues'],[]);self.assertFalse(r['literal_grounding_passed'])

    def test_partial_extraction_cannot_certify_quote(self):
        d=docs();d[0]['pages'][0]['status']='partial'
        r=verify_findings(d,[{'finding_id':'f1','support_status':'supported','citations':[cite()]}]);self.assertFalse(r['literal_grounding_passed'])

    def test_mixed_ledger_does_not_certify_unquoted_findings(self):
        r=verify_findings(docs(),[{'finding_id':'f1','support_status':'supported','citations':[cite()]},
                                 {'finding_id':'f2','support_status':'unverified','citations':[]}])
        self.assertFalse(r['literal_grounding_passed']);self.assertEqual(r['findings_without_verified_quotes'],['f2'])

    def test_boolean_or_fractional_page_reference_is_rejected(self):
        for page in [True,1.0,'1',[],None]:
            with self.subTest(page=page),self.assertRaises(InputError):self.check({**cite(),'page':page})

    def test_malformed_citation_identifier_is_rejected(self):
        for document_id in [[],{},None]:
            with self.subTest(document_id=document_id),self.assertRaises(InputError):self.check({**cite(),'document_id':document_id})

    def test_duplicate_finding_ids_rejected(self):
        f={'finding_id':'f1','support_status':'supported','citations':[cite()]}
        with self.assertRaises(InputError):verify_findings(docs(),[f,f])


class ExportTests(unittest.TestCase):
    def test_spreadsheet_formulas_and_headers_are_inert(self):
        text=csv_text([{'=header':' =HYPERLINK("bad")','safe':'@cmd','number':-3,'tab':'\tformula'}])
        rows=list(csv.reader(io.StringIO(text)))
        self.assertTrue(rows[0][0].startswith("'"));self.assertTrue(rows[1][0].startswith("'"));self.assertEqual(rows[1][1],"'@cmd");self.assertEqual(rows[1][2],'-3');self.assertTrue(rows[1][3].startswith("'"))

    def test_csv_quotes_newlines_and_unicode_survive(self):
        value='First, "quoted"\nSecond 😀'
        result=list(csv.DictReader(io.StringIO(csv_text([{'value':value}]))))
        self.assertEqual(result[0]['value'],value)

    def test_csv_rejects_malformed_and_nested_nonfinite_data(self):
        for rows in [None,{},'rows',[None],[{1:'x'}],[{'x':{'number':float('nan')}}]]:
            with self.subTest(rows=rows),self.assertRaises(InputError):csv_text(rows)

    def test_csv_sanitized_headers_cannot_collide(self):
        with self.assertRaises(InputError):csv_text([{'=name':'first',"'=name":'second'}])

    def test_empty_csv_is_empty(self):
        self.assertEqual(csv_text([]),'')


class JsonInputTests(unittest.TestCase):
    def test_duplicate_keys_and_nonfinite_json_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'input.json'
            for value in ['{"status":"partial","status":"complete"}','[NaN]','[Infinity]']:
                p.write_text(value,encoding='utf-8')
                with self.subTest(value=value),self.assertRaises(InputError):read_json(p)

    def test_jsonl_retains_unicode_line_separators_inside_strings(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'input.jsonl'
            p.write_text(json.dumps({'text':'A\u2028B'},ensure_ascii=False)+'\n',encoding='utf-8')
            self.assertEqual(read_json(p),[{'text':'A\u2028B'}])

    def test_invalid_utf8_is_a_controlled_input_error(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'input.json';p.write_bytes(b'\xffnot json')
            with self.assertRaises(InputError):read_json(p)


if __name__=='__main__':unittest.main(verbosity=2)
