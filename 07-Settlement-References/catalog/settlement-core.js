(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.SettlementCore = api;
})(globalThis, function () {
  'use strict';
  const DAY=86400000;
  const TYPES={financial_fee_settlement:'Financial fees',class_action_settlement:'Class action',privacy_settlement:'Privacy',consumer_product_settlement:'Consumer product',data_breach_settlement:'Data breach',other_consumer_compensation:'Consumer compensation',state_ag_refund:'State refund',government_refund:'Government refund',regulatory_compensation_program:'Regulatory compensation'};
  function isoDay(value){if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))return null;const n=Date.parse(value+'T00:00:00Z');return Number.isFinite(n)&&new Date(n).toISOString().slice(0,10)===value?n:null;}
  function localToday(){const d=new Date();return [d.getFullYear(),String(d.getMonth()+1).padStart(2,'0'),String(d.getDate()).padStart(2,'0')].join('-');}
  function daysUntil(date,asOf){const a=isoDay(date),b=isoDay(asOf);return a===null||b===null?null:Math.round((a-b)/DAY);}
  function prettyDate(date){return isoDay(date)===null?'Not stated':new Date(date+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric',timeZone:'UTC'});}
  function normalize(value){return String(value??'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase();}
  function safeURL(value){try{if(typeof value!=='string'||value!==value.trim()||/[^\S ]|[\u0000-\u001f\u007f\\]/.test(value)||!/^https?:\/\/[^\s/?#]+(?:[/?#]|$)/i.test(value))return null;const u=new URL(value);if(!['http:','https:'].includes(u.protocol)||u.username||u.password||u.port)return null;const host=u.hostname.toLowerCase();if(!host.includes('.')||host==='localhost'||host.endsWith('.local')||host.endsWith('.localhost')||host.includes(':')||/^\d+(?:\.\d+){3}$/.test(host))return null;return u.href;}catch{return null;}}
  function localDocument(path){if(typeof path!=='string'||!path.startsWith('documents/')||/[\u0000-\u001f\u007f\\]/.test(path))return null;const parts=path.split('/');if(parts.some(p=>!p||p==='.'||p==='..'))return null;return '07-Settlement-References/'+parts.map(encodeURIComponent).join('/');}
  function typeLabel(type){return TYPES[type]||String(type||'Not stated').replaceAll('_',' ');}
  function reportedGeography(record){return record.publisher.applicable_states.length?record.publisher.applicable_states.join(', '):'Nationwide (feed)';}
  function claimDate(record){return record.publisher.claim_deadline;}
  function flags(record,asOf){const r=record.publisher,out=[...(record.quality_notes||[])];const d=daysUntil(r.claim_deadline,asOf);if(d!==null&&d<0&&r.status==='Open for claims')out.push('The reported claim date has passed; the feed status has not been updated.');if(d===0)out.push('The reported claim date is today. The feed does not provide a cutoff time or time zone.');if(d!==null&&d>=0&&r.status==='Claim window closed')out.push('The feed says the claim window is closed despite a current or future reported date.');if(record.review?.discrepancies?.length)out.push('The attached source review qualifies or corrects '+record.review.discrepancies.length+' reported field(s).');return out;}
  function filterRecords(records,f={},saved=new Set()){
    const terms=normalize(f.query).trim().split(/\s+/).filter(Boolean),asOf=f.asOf||localToday();
    return records.filter(r=>{
      const p=r.publisher,days=daysUntil(p.claim_deadline,asOf);
      if(f.category && (p.category||'Uncategorized')!==f.category)return false;
      if(f.proof && p.proof_required!==f.proof)return false;
      if(f.status && p.status!==f.status)return false;
      if(f.evidence && p.verification_status!==f.evidence)return false;
      if(f.state==='nationwide' && p.applicable_states.length)return false;
      if(f.state && f.state!=='nationwide' && !p.applicable_states.includes(f.state) && !(f.includeNationwide!==false&&!p.applicable_states.length))return false;
      if(f.collection==='reviewed'&&!r.review)return false;
      if(f.collection==='saved'&&!saved.has(r.id))return false;
      if(f.collection==='upcoming'&&(days===null||days<0||days>30))return false;
      if(f.deadline==='missing'&&p.claim_deadline)return false;
      if(f.deadline==='past'&&(days===null||days>=0))return false;
      if(['7','30','90'].includes(f.deadline)&&(days===null||days<0||days>Number(f.deadline)))return false;
      if(f.localOnly&&!r.review?.documents?.some(d=>d.status==='downloaded'&&localDocument(d.path)))return false;
      const text=normalize([p.title,p.category,p.settlement_type,p.estimated_payout,p.applicable_states.join(' '),p.status,r.review?.title,r.review?.court,r.review?.case_number,r.review?.jurisdiction,r.review?.eligibility_scope,r.review?.summary].filter(Boolean).join(' '));
      return terms.every(t=>text.includes(t));
    });
  }
  function sortRecords(records,sort='upcoming',asOf=localToday()){
    return [...records].sort((a,b)=>{
      if(sort==='title')return a.publisher.title.localeCompare(b.publisher.title)||a.id.localeCompare(b.id);
      if(sort==='reviewed'&&!!a.review!==!!b.review)return a.review?-1:1;
      if(sort==='verified'){const v=String(b.publisher.last_verified||'').localeCompare(String(a.publisher.last_verified||''));if(v)return v;}
      const ad=daysUntil(claimDate(a),asOf),bd=daysUntil(claimDate(b),asOf),rank=d=>d===null?2:d<0?1:0;
      const group=rank(ad)-rank(bd);if(group)return group;
      if(ad!==bd){if(ad===null)return 1;if(bd===null)return -1;return ad<0&&bd<0?bd-ad:ad-bd;}
      return a.publisher.title.localeCompare(b.publisher.title)||a.id.localeCompare(b.id);
    });
  }
  function exportRecord(r){return {id:r.id,source_positions:r.source_positions,publisher:{...r.publisher},publisher_record_sha256:r.publisher_record_sha256,source_snapshot_sha256:r.source_snapshot_sha256,source_review:r.review||null,quality_notes:r.quality_notes||[],source_review_attached:!!r.review,independent_review_scope:r.review?.independent_review||null};}
  function csvCell(value){if(value===null||value===undefined)return '""';let s=String(value);if(/^[\s\u0000-\u001f]*[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}
  function csv(records,meta){const fields=['Record ID','Title (feed)','Category (feed)','Type (feed)','Claim date (feed)','Status (feed)','Proof (feed)','Geography (feed)','Benefits as reported (not normalized)','Publisher verification tier','Publisher last check','Publisher evidence flag','Claim link (feed)','Settlement site (feed)','Source review available','Reviewed process','Reviewed claim date','Review assessment date','Source review limitations','Review discrepancies','Publisher record URL','Attribution'];
    const out=[fields.map(csvCell).join(',')];for(const r of records){const p=r.publisher,v=r.review;out.push([r.id,p.title,p.category||'Uncategorized',typeLabel(p.settlement_type),p.claim_deadline,p.status,p.proof_required,reportedGeography(r),p.estimated_payout,p.verification_status,p.last_verified,p.accepted_official_evidence,p.official_claim_url,p.official_settlement_url,!!v,v?.status,v?.claim_deadline,v?.assessment_date,v?.independent_review?.limitations,v?.discrepancies?.map(x=>[x.field,x.official_observation,x.note].filter(Boolean).join(': ')).join(' | '),p.url,meta.attribution].map(csvCell).join(','));}return '\uFEFF'+out.join('\r\n')+'\r\n';}
  function researchBrief(r,meta){const p=r.publisher,v=r.review;return '# Settlement research brief: '+p.title+'\n\nRecord: '+r.id+'\nSource snapshot: '+meta.generated+'\n\n## Reported facts\n\n- Claim date (feed): '+(p.claim_deadline||'Not stated')+'\n- Process (feed): '+p.status+'\n- Proof (feed): '+p.proof_required+'\n- Geography (feed): '+reportedGeography(r)+'\n- Publisher verification tier: '+p.verification_status+'\n\n## Benefits as reported\n\n'+(p.estimated_payout||'No benefit description supplied.')+'\n\nThis text may mix a total fund, maximum reimbursement, noncash benefits and an estimated per-person award. Do not treat it as a standardized settlement valuation.\n\n## Primary-source follow-up\n\n1. Establish the case, court, settlement round, class definition and operative approval/order date.\n2. Check the current notice, administrator instructions and later orders for claim, exclusion, objection and hearing dates. Keep these events separate; do not invent a cutoff time.\n3. Extract eligibility and documentation requirements, benefit elections, caps and pro rata adjustments with source locators.\n4. Distinguish fund totals, class size, actual claims, administration costs and per-person benefits before comparing cases.\n5. Preserve unavailable sources, contradictions, date uncertainty and review coverage. Return a cited ledger with the extraction scope.\n\n## Attached source review\n\n'+(v?'Assessed '+v.assessment_date+'. '+v.summary+'\n\nReviewed process: '+v.status+'\nReviewed claim date: '+(v.claim_deadline||'Not stated / not applicable')+'\n\n'+v.independent_review.limitations+'\n\n'+(v.discrepancies||[]).map(x=>'- '+x.field+': '+x.official_observation+' '+x.note).join('\n'):'No independent source review is attached. Provider metadata is not an independent verification result.')+'\n\n## Source links\n\n'+[p.official_settlement_url,p.official_claim_url,p.url].filter(Boolean).map(u=>'- '+u).join('\n')+'\n\n'+meta.attribution+'\n'+meta.license+'\n\nPrepared locally as a research assignment. No eligibility determination, claim filing or calendar action has been made.\n';}
  return {isoDay,localToday,daysUntil,prettyDate,normalize,safeURL,localDocument,typeLabel,reportedGeography,claimDate,flags,filterRecords,sortRecords,exportRecord,csvCell,csv,researchBrief};
});
