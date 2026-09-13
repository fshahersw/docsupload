/* Original bounded citation lookup. No network, fuzzy substitution, or legal-effect inference. */
(function(root){
 'use strict';
 const pin='((?:\\s*\\([A-Za-z0-9]+\\))*)';
 const number='([0-9]+[A-Za-z]?(?:\\.[0-9]+)?|[A-G])';
 const rulePatterns=[
  ['FRCP','(?:FRCP|Fed\\.?\\s*R\\.?\\s*Civ\\.?\\s*P\\.?)'],
  ['FRAP','(?:FRAP|Fed\\.?\\s*R\\.?\\s*App\\.?\\s*P\\.?)'],
  ['FRE','(?:FRE|Fed\\.?\\s*R\\.?\\s*Evid\\.?)'],
  ['SUPP-ADM','(?:Supplemental Admiralty Rule|SUPP-ADM)'],
  ['SUPP-SSA','(?:Supplemental Social Security Rule|SUPP-SSA)']
 ].map(([f,p])=>[f,new RegExp('^'+p+'\\s*(?:Rule\\s*)?'+number+pin+'$','i')]);
 function parse(value){
  const input=String(value||'').trim().replace(/\u00a0/g,' ');
  let m=input.match(new RegExp('^([0-9]+)\\s+U\\.?\\s*S\\.?\\s*C\\.?\\s*(?:§|sec(?:tion)?\\.?)?\\s*([0-9]+[A-Za-z]?)'+pin+'$','i'));
  if(m)return {key:'USC:'+Number(m[1])+':'+m[2],pin:[...m[3].matchAll(/\(([^)]+)\)/g)].map(x=>x[1]),input};
  for(const [family,re] of rulePatterns){m=input.match(re);if(m)return {key:family+':'+m[1].toUpperCase(),pin:[...m[2].matchAll(/\(([^)]+)\)/g)].map(x=>x[1]),input};}
  return null;
 }
 function resolve(input,records){
  const p=parse(input);
  if(!p)return {status:'unsupported',message:'Enter one supported U.S. Code or federal rule citation. Bare rule numbers and citation ranges are not resolved.'};
  const matches=records.filter(r=>r.citation_key.toLowerCase()===p.key.toLowerCase());
  if(!matches.length)return {status:'not_found',parsed:p,matches:[],message:'This citation is outside the loaded snapshot or is not present. No substitute was selected.'};
  if(matches.length>1)return {status:'ambiguous',parsed:p,matches,message:'The publisher contains multiple provisions with this citation. Choose the intended title below.'};
  const record=matches[0];
  if(p.pin.length){
   const subs=record.subsections.filter(s=>s.path.join('/')===p.pin.join('/'));
   if(subs.length!==1)return {status:subs.length?'ambiguous_subsection':'subsection_not_found',parsed:p,matches:[record],message:'The requested subsection could not be resolved uniquely. The parent provision is available below.'};
   if(record.source_structure_issues?.length)return {status:'source_structure_uncertain',parsed:p,matches:[record],message:'The publisher XML has numbering or nesting issues in this provision. Read the complete provision and original PDF; an exact pinpoint has not been asserted.'};
   return {status:'resolved',parsed:p,matches:[record],record,subsection:subs[0]};
  }
  return {status:'resolved',parsed:p,matches:[record],record};
 }
 const api={parse,resolve};root.CourtCitation=api;
 if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
