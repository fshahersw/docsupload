"""Local, deterministic corpus utilities. No network, model calls or supplied-code execution.

These checks measure extraction/scan coverage and literal citation grounding; they
do not decide whether a legal proposition is supported or law is current.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote_plus, urlsplit, urlunsplit


class InputError(ValueError):
    pass


def canonical_url(value: str) -> str:
    """Conservative URL identity; significant query parameters/anchors survive."""
    if not isinstance(value, str) or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise InputError('URL must be text without control characters')
    value = value.strip()
    if any(c.isspace() for c in value) or '\\' in value:
        raise InputError('URL contains unescaped whitespace or a backslash')
    try:
        u = urlsplit(value)
        if u.scheme.lower() not in ('http', 'https') or not u.hostname or u.username is not None or u.password is not None:
            raise ValueError()
        port = u.port
        host = u.hostname.encode('idna').decode('ascii').lower()
    except (ValueError, UnicodeError) as exc:
        raise InputError('Expected an HTTP(S) URL without credentials') from exc
    if ':' in host:
        host = '[' + host + ']'
    if port is not None and (u.scheme.lower(), port) not in (('https', 443), ('http', 80)):
        host += ':' + str(port)
    # Keep significant query bytes, bare flags and duplicate order. Parsing and
    # re-encoding would change signed values, percent-escape case and %20 to +.
    query = []
    for part in u.query.split('&'):
        key = unquote_plus(part.split('=', 1)[0]).lower()
        if not key.startswith('utm_') and key not in ('fbclid', 'gclid'):
            query.append(part)
    return urlunsplit((u.scheme.lower(), host, u.path or '/', '&'.join(query), u.fragment))


def classify_http(status: int | None, error: str | None = None) -> str:
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        raise InputError('HTTP status must be an integer from 100 to 599, or null')
    if error is not None and not isinstance(error, str):
        raise InputError('HTTP error must be text or null')
    if error:
        return {'timeout': 'timeout', 'tls': 'tls_error', 'dns': 'dns_error'}.get(error, 'network_error')
    if status is None:
        return 'not_checked'
    if 200 <= status < 300:
        return 'http_success_content_not_verified'
    if 300 <= status < 400:
        return 'redirect_not_resolved'
    return {401: 'authentication_required', 403: 'access_denied_reason_unknown',
            404: 'not_found_at_check', 410: 'gone_at_check', 429: 'rate_limited',
            503: 'service_unavailable'}.get(status, 'http_error')


def normalize_registry(rows: list[dict]) -> dict:
    if not isinstance(rows, list):
        raise InputError('Registry rows must be an array')
    groups: dict[str, list[dict]] = defaultdict(list)
    for n, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            raise InputError(f'Row {n} is not an object')
        try:
            url = canonical_url(row.get('canonical_url') or row.get('url') or '')
        except InputError as exc:
            raise InputError(f'Row {n}: {exc}') from exc
        groups[url].append({'input_row': n, 'record': row})
    records = []
    for url, members in groups.items():
        records.append({'source_id': 'src-' + hashlib.sha256(url.encode()).hexdigest()[:20],
                        'canonical_url': url, 'input_rows': [r['input_row'] for r in members],
                        'variants': [r['record'] for r in members],
                        'content_downloaded_by_this_tool': False,
                        'legal_authority_verified': False})
    return {'input_count': len(rows), 'unique_count': len(records),
            'duplicate_count': len(rows) - len(records), 'records': records}


def text_hash(value: str) -> str:
    if not isinstance(value, str):
        raise InputError('Text to hash must be a string')
    try:
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    except UnicodeError as exc:
        raise InputError('Text contains invalid Unicode') from exc


def is_hash(value) -> bool:
    return isinstance(value, str) and re.fullmatch(r'[a-f0-9]{64}', value) is not None


def plan_digest(plan: dict) -> str:
    """Consistency fingerprint, not a signature or proof of source authenticity."""
    try:
        return text_hash(json.dumps({k: v for k, v in plan.items() if k != 'plan_sha256'},
                                    sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False))
    except (TypeError, ValueError, RecursionError) as exc:
        raise InputError('Plan must contain finite JSON-compatible values') from exc


def document_index(documents: list[dict]) -> dict[str, dict]:
    if not isinstance(documents, list) or not documents:
        raise InputError('Provide at least one explicitly scoped document')
    index = {}
    for d in documents:
        if not isinstance(d, dict):
            raise InputError('Every document must be an object')
        for key in ('document_id', 'matter_id', 'access_scope', 'source_version'):
            if not isinstance(d.get(key), str) or not d[key].strip():
                raise InputError(f'Document requires {key}')
        if d['document_id'] in index:
            raise InputError('Duplicate document_id: ' + d['document_id'])
        if not is_hash(d.get('sha256')):
            raise InputError('Document sha256 must identify the source bytes')
        count = d.get('expected_page_count')
        if type(count) is not int or count < 1:
            raise InputError('expected_page_count must be a positive integer')
        pages = d.get('pages')
        if not isinstance(pages, list):
            raise InputError('pages must be a list, including unavailable pages where known')
        page_ids = set()
        for page in pages:
            if not isinstance(page, dict):
                raise InputError('Page must be an object')
            number = page.get('page')
            if type(number) is not int or number < 1 or number > count or number in page_ids:
                raise InputError('Duplicate or out-of-range page number')
            page_ids.add(number)
            if page.get('status') not in ('complete', 'partial', 'unreadable', 'pending'):
                raise InputError('Every page needs explicit extraction status')
            if not isinstance(page.get('text'), str):
                raise InputError('Page text must be a string, empty when unavailable')
        index[d['document_id']] = d
    return index


def plan_scan(documents: list[dict], chunk_chars: int = 6000, overlap: int = 400) -> dict:
    """Partition every supplied page without dropping tails or crossing sources."""
    index = document_index(documents)
    if type(chunk_chars) is not int or chunk_chars < 2 or type(overlap) is not int or not 0 <= overlap < chunk_chars:
        raise InputError('Require chunk_chars >= 2 and 0 <= overlap < chunk_chars')
    chunks, coverage, duplicates = [], [], defaultdict(list)
    for d in index.values():
        # Hash equality never merges access scopes or matter records.
        duplicates[(d['matter_id'], d['access_scope'], d['sha256'])].append(d['document_id'])
        pages = {p['page']: p for p in d['pages']}
        for number in range(1, d['expected_page_count'] + 1):
            p = pages.get(number)
            status = p['status'] if p else 'missing'
            text = p['text'] if p else ''
            coverage.append({'document_id': d['document_id'], 'page': number,
                             'extraction_status': status, 'text_characters': len(text),
                             'text_sha256': text_hash(text)})
            if status not in ('complete', 'partial'):
                continue
            start = 0
            while start < len(text):
                end = min(len(text), start + chunk_chars)
                part = text[start:end]
                identity = [d[k] for k in ('document_id', 'matter_id', 'access_scope', 'sha256', 'source_version')]
                identity += [number, start, end, text_hash(part)]
                chunks.append({'chunk_id': 'chunk-' + text_hash(json.dumps(identity))[:24],
                               'document_id': d['document_id'], 'matter_id': d['matter_id'],
                               'access_scope': d['access_scope'], 'source_version': d['source_version'],
                               'source_sha256': d['sha256'], 'page': number,
                               'start_character': start, 'end_character': end,
                               'text_sha256': text_hash(part), 'text': part})
                if end == len(text):
                    break
                start = end - overlap
    gaps = [p for p in coverage if p['extraction_status'] != 'complete']
    result = {'schema_version': '1.1.0', 'purpose': 'exhaustive_scan_plan',
            'character_unit': 'unicode_code_points',
            'document_manifest': [{k: d[k] for k in ('document_id', 'matter_id', 'access_scope', 'sha256', 'source_version', 'expected_page_count')} for d in index.values()],
            'document_count': len(index), 'expected_pages': len(coverage),
            'complete_extraction_pages': len(coverage) - len(gaps), 'extraction_gaps': gaps,
            'page_manifest': coverage, 'chunk_count': len(chunks), 'chunks': chunks,
            'duplicate_candidates': [ids for ids in duplicates.values() if len(ids) > 1],
            'dedup_policy': 'Candidates only; preserve every matter, access scope, original and source version.'}
    result['plan_sha256'] = plan_digest(result)
    return result


def scan_coverage(plan: dict, attempts: list[dict], max_attempts: int = 3,
                  *, expected_plan_sha256: str | None = None) -> dict:
    """Validate a plan and summarize one current status per numbered attempt.

    A later attempt supersedes an older pending record. Successful attempts are
    durable. Pending attempts never exhaust their budget until terminal. Store
    plan_sha256 separately and supply expected_plan_sha256 to pin intended scope;
    an unkeyed digest alone cannot authenticate caller-supplied source metadata.
    """
    if type(max_attempts) is not int or max_attempts < 1:
        raise InputError('max_attempts must be positive')
    if not isinstance(plan, dict) or not isinstance(attempts, list):
        raise InputError('Provide a plan object and an attempts array')
    if plan.get('schema_version') != '1.1.0' or plan.get('purpose') != 'exhaustive_scan_plan':
        raise InputError('Unsupported plan schema or purpose; regenerate the plan')
    if plan.get('character_unit') != 'unicode_code_points':
        raise InputError('Unsupported character unit')
    if not is_hash(plan.get('plan_sha256')) or plan_digest(plan) != plan['plan_sha256']:
        raise InputError('Plan fingerprint changed; regenerate from the intended source scope')
    if expected_plan_sha256 is not None and (not is_hash(expected_plan_sha256) or expected_plan_sha256 != plan['plan_sha256']):
        raise InputError('Plan does not match the separately recorded expected scope')
    manifest = plan.get('document_manifest')
    if not isinstance(manifest, list) or any(not isinstance(d, dict) for d in manifest):
        raise InputError('Plan requires a document scope manifest')
    documents = document_index([{**d, 'pages': []} for d in manifest])
    if type(plan.get('document_count')) is not int or plan['document_count'] != len(documents):
        raise InputError('Plan document count is inconsistent')
    chunks = plan.get('chunks')
    if not isinstance(chunks, list) or any(not isinstance(c, dict) for c in chunks):
        raise InputError('Plan chunks must be an array of objects')
    ids = [c.get('chunk_id') for c in chunks]
    if any(not isinstance(cid, str) or not cid for cid in ids):
        raise InputError('Each chunk needs a nonempty identity')
    if len(set(ids)) != len(ids) or type(plan.get('chunk_count')) is not int or plan['chunk_count'] != len(ids):
        raise InputError('Plan chunk identities/count are inconsistent')
    if not isinstance(plan.get('page_manifest'), list) or not plan['page_manifest']:
        raise InputError('Plan has no page scope; cannot certify an empty selection')
    pages = {}
    for p in plan['page_manifest']:
        if not isinstance(p, dict) or not isinstance(p.get('document_id'), str):
            raise InputError('Every page needs a scoped document identity')
        d = documents.get(p['document_id'])
        if not d or type(p.get('page')) is not int or not 1 <= p['page'] <= d['expected_page_count']:
            raise InputError('Page is outside the declared document scope')
        if p.get('extraction_status') not in ('complete', 'partial', 'unreadable', 'pending', 'missing'):
            raise InputError('Unknown extraction status')
        if type(p.get('text_characters')) is not int or p['text_characters'] < 0 or not is_hash(p.get('text_sha256')):
            raise InputError('Invalid page text length or hash')
        key = (p['document_id'], p['page'])
        if key in pages:
            raise InputError('Duplicate page in plan')
        pages[key] = p
    if type(plan.get('expected_pages')) is not int or plan['expected_pages'] != len(pages) or len(pages) != sum(d['expected_page_count'] for d in documents.values()):
        raise InputError('Plan page scope is inconsistent')
    ranges = defaultdict(list)
    for c in plan['chunks']:
        if not isinstance(c.get('document_id'), str) or type(c.get('page')) is not int:
            raise InputError('Chunk has an invalid document or page identity')
        key = (c['document_id'], c['page'])
        if key not in pages or type(c.get('start_character')) is not int or type(c.get('end_character')) is not int or c['start_character'] < 0 or c['end_character'] <= c['start_character']:
            raise InputError('Chunk points outside the page scope')
        if pages[key]['extraction_status'] not in ('complete', 'partial'):
            raise InputError('Chunk refers to a page without usable extraction')
        d = documents[c['document_id']]
        if any(c.get(k) != d[k] for k in ('matter_id', 'access_scope', 'source_version')) or c.get('source_sha256') != d['sha256']:
            raise InputError('Chunk does not match its document scope')
        if not isinstance(c.get('text'), str) or c['end_character'] > pages[key]['text_characters'] or len(c['text']) != c['end_character'] - c['start_character']:
            raise InputError('Chunk text and range are inconsistent')
        if text_hash(c['text']) != c.get('text_sha256'):
            raise InputError('Chunk text hash changed')
        identity = [c[k] for k in ('document_id', 'matter_id', 'access_scope', 'source_sha256', 'source_version')]
        identity += [c['page'], c['start_character'], c['end_character'], c['text_sha256']]
        if c['chunk_id'] != 'chunk-' + text_hash(json.dumps(identity))[:24]:
            raise InputError('Chunk identity changed')
        ranges[key].append(c)
    for key, p in pages.items():
        if p['extraction_status'] not in ('complete', 'partial'):
            continue
        reconstructed = ''
        for c in sorted(ranges[key], key=lambda c: (c['start_character'], c['end_character'])):
            start = c['start_character']
            if start > len(reconstructed):
                raise InputError('Plan drops text between chunks')
            overlap = min(len(reconstructed) - start, len(c['text']))
            if reconstructed[start:start + overlap] != c['text'][:overlap]:
                raise InputError('Overlapping chunks disagree about page text')
            reconstructed += c['text'][overlap:]
        if len(reconstructed) != p['text_characters']:
            raise InputError('Plan drops a page tail or an entire page')
        if text_hash(reconstructed) != p['text_sha256']:
            raise InputError('Reconstructed page text hash changed')
    gaps = [p for p in plan['page_manifest'] if p['extraction_status'] != 'complete']
    if plan.get('extraction_gaps') != gaps or type(plan.get('complete_extraction_pages')) is not int or plan['complete_extraction_pages'] != len(pages) - len(gaps):
        raise InputError('Extraction summary is inconsistent with the page manifest')
    known = set(ids)
    grouped, seen = defaultdict(list), set()
    for a in attempts:
        if not isinstance(a, dict):
            raise InputError('Attempt must be an object')
        key = (a.get('chunk_id'), a.get('attempt'))
        if not isinstance(key[0], str) or key[0] not in known or type(key[1]) is not int or key[1] < 1 or key in seen:
            raise InputError('Unknown chunk, duplicate attempt, or invalid attempt number')
        if a.get('status') not in ('completed', 'failed', 'timeout', 'pending'):
            raise InputError('Unknown attempt status')
        seen.add(key)
        grouped[key[0]].append(a)
    # A validated successful attempt is durable; later failed retries do not erase it.
    done = {cid for cid, runs in grouped.items() if any(a['status'] == 'completed' for a in runs)}
    missing = [cid for cid in ids if cid not in done]
    latest = {cid: max(runs, key=lambda a: a['attempt']) for cid, runs in grouped.items() if runs}
    pending = [cid for cid in missing if latest.get(cid, {}).get('status') == 'pending']
    exhausted = [cid for cid in missing if cid not in pending and latest.get(cid, {}).get('attempt', 0) >= max_attempts]
    retry = [cid for cid in missing if cid not in exhausted and cid not in pending]
    return {'complete': not gaps and not missing, 'expected_chunks': len(ids),
            'completed_chunks': len(done), 'coverage_fraction': len(done) / len(ids) if ids else None,
            'extraction_gaps': gaps, 'unfinished_chunk_ids': missing,
            'retry_chunk_ids': retry, 'exhausted_chunk_ids': exhausted,
            'pending_chunk_ids': pending, 'attempts_logged': len(attempts),
            'plan_sha256': plan['plan_sha256'],
            'matches_expected_plan': True if expected_plan_sha256 is not None else None,
            'source_bytes_verified': False,
            'interpretation': 'Processing coverage within caller-declared scope only. Source file bytes and extraction status were not independently checked; a completed model call is not an accuracy assessment.'}


def verify_findings(documents: list[dict], findings: list[dict]) -> dict:
    index = document_index(documents)
    if not isinstance(findings, list):
        raise InputError('Findings must be an array')
    ids, issues, quote_count, without_quotes = set(), [], 0, []
    for finding in findings:
        if not isinstance(finding, dict):
            raise InputError('Finding must be an object')
        fid = finding.get('finding_id')
        if not isinstance(fid, str) or not fid.strip() or fid in ids:
            raise InputError('Finding IDs must be nonempty and unique')
        ids.add(fid)
        status = finding.get('support_status')
        if status not in ('supported', 'partially_supported', 'unsupported', 'unverified'):
            raise InputError('Unknown support_status')
        citations = finding.get('citations')
        if not isinstance(citations, list):
            raise InputError('citations must be a list')
        if status in ('supported', 'partially_supported') and not citations:
            issues.append({'finding_id': fid, 'reason': 'support_claim_without_evidence'})
        finding_quotes = 0
        for c in citations:
            if not isinstance(c, dict):
                raise InputError('Citation must be an object')
            if not isinstance(c.get('document_id'), str) or not c['document_id'].strip() or type(c.get('page')) is not int or c['page'] < 1:
                raise InputError('Citation needs a document ID and positive integer page')
            reason = None
            d = index.get(c.get('document_id'))
            if not d:
                reason = 'unknown_document'
            elif c.get('source_version') != d['source_version'] or c.get('source_sha256') != d['sha256']:
                reason = 'source_version_or_hash_mismatch'
            elif c.get('matter_id') != d['matter_id'] or c.get('access_scope') != d['access_scope']:
                reason = 'scope_mismatch'
            else:
                p = next((p for p in d['pages'] if p['page'] == c.get('page')), None)
                quote = c.get('quote')
                if not p or p['status'] != 'complete':
                    reason = 'page_missing_or_extraction_incomplete'
                elif not isinstance(quote, str) or not quote.strip():
                    reason = 'empty_quote'
                elif quote not in p['text']:
                    reason = 'quote_not_literal_on_cited_page'
            if reason:
                issues.append({'finding_id': fid, 'reason': reason, 'document_id': c.get('document_id'), 'page': c.get('page')})
            else:
                quote_count += 1
                finding_quotes += 1
        if not finding_quotes:
            without_quotes.append(fid)
    return {'finding_count': len(findings), 'literal_quotes_verified': quote_count,
            'literal_grounding_passed': bool(findings) and not without_quotes and not issues,
            'findings_without_verified_quotes': without_quotes,
            'empty_ledger': not findings, 'issues': issues,
            'legal_support_evaluated': False, 'citation_treatment_evaluated': False, 'source_bytes_verified': False,
            'interpretation': 'Literal matching against supplied page text only. Source bytes and caller-declared extraction status are not independently checked. A matching quote may not support the claimed proposition.'}


def csv_text(rows: list[dict]) -> str:
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise InputError('CSV rows must be an array of objects')
    if not rows:
        return ''
    if any(not isinstance(k, str) for row in rows for k in row):
        raise InputError('CSV column names must be strings')
    fields = list(dict.fromkeys(k for r in rows for k in r))
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')

    def cell(value):
        if isinstance(value, (dict, list)):
            try:
                value = json.dumps(value, ensure_ascii=False, allow_nan=False)
            except (TypeError, ValueError, RecursionError) as exc:
                raise InputError('Nested CSV values must be finite JSON data') from exc
        elif not isinstance(value, (str, int, float, bool, type(None))):
            raise InputError('CSV values must be JSON-compatible')
        if isinstance(value, float) and not math.isfinite(value):
            raise InputError('Non-finite numbers cannot be exported')
        if isinstance(value, str) and (value.lstrip().startswith(('=', '+', '-', '@')) or value.startswith(('\t', '\r', '\n'))):
            return "'" + value
        return value

    # Column names can be hostile too. Write the header with the same safeguards.
    if len({cell(k) for k in fields}) != len(fields):
        raise InputError('CSV headers collide after spreadsheet sanitization')
    writer.writerow({k: cell(k) for k in fields})
    for row in rows:
        writer.writerow({k: cell(v) for k, v in row.items()})
    return stream.getvalue()


def read_json(path: Path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InputError('JSON objects must not contain duplicate keys')
            result[key] = value
        return result

    def invalid_constant(value):
        raise InputError('Non-finite JSON value: ' + value)

    try:
        text = path.read_text(encoding='utf-8-sig')
        def parse(value):
            return json.loads(value, object_pairs_hook=pairs, parse_constant=invalid_constant)
        if path.suffix.lower() == '.jsonl':
            return [parse(line) for line in text.split('\n') if line.strip()]
        return parse(text)
    except (UnicodeError, RecursionError) as exc:
        raise InputError('Input must be valid UTF-8 JSON with bounded nesting') from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('registry', 'plan', 'coverage', 'verify', 'csv'):
        p = sub.add_parser(name)
        p.add_argument('input', type=Path)
        p.add_argument('--output', type=Path, required=True)
        if name in ('coverage', 'verify'):
            p.add_argument('--results', type=Path, required=True)
        if name == 'plan':
            p.add_argument('--chunk-chars', type=int, default=6000)
            p.add_argument('--overlap', type=int, default=400)
        if name == 'coverage':
            p.add_argument('--expected-plan-sha256', help='Fingerprint recorded separately when the plan was created')
    args = parser.parse_args()
    try:
        inputs = [args.input] + ([args.results] if hasattr(args, 'results') else [])
        if args.output.resolve() in [p.resolve() for p in inputs]:
            raise InputError('Output must not overwrite an input')
        data = read_json(args.input)
        if args.command == 'registry': out = normalize_registry(data)
        elif args.command == 'plan': out = plan_scan(data, args.chunk_chars, args.overlap)
        elif args.command == 'coverage': out = scan_coverage(data, read_json(args.results), expected_plan_sha256=args.expected_plan_sha256)
        elif args.command == 'verify': out = verify_findings(data, read_json(args.results))
        else: out = csv_text(data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out if isinstance(out, str) else json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='')
        print('Wrote '+str(args.output))
    except (InputError, OSError, json.JSONDecodeError) as exc:
        parser.exit(2, f'Input error: {exc}\n')


if __name__ == '__main__':
    main()
