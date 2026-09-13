(function () {
  'use strict';
  const data = globalThis.SW_PLATFORM_CORPUS;
  const root = document.querySelector('#platform-corpus');
  if (!root || !data) return;
  const base = root.dataset.libraryBase || '';
  const asset = base + '11-Platform-Corpus/';
  const state = { tab: 'sources', query: '', category: '' };
  const el = (tag, text, cls) => { const e = document.createElement(tag); if (text != null) e.textContent = text; if (cls) e.className = cls; return e; };
  const button = (text, fn, cls) => { const b = el('button', text, cls); b.type = 'button'; b.addEventListener('click', fn); return b; };
  const link = (text, path) => { const a = el('a', text); a.href = base + path; return a; };
  const external = (text, url) => { const a = el('a', text); try { const u = new URL(url); if (!['http:', 'https:'].includes(u.protocol) || u.username || u.password) throw new Error(); a.href = u.href; a.target = '_blank'; a.rel = 'noopener noreferrer'; } catch { return el('span', text); } return a; };
  const list = (items) => { const u = el('ul'); for (const item of items || []) u.append(el('li', item)); return u; };
  const disclosure = (title) => { const d = el('details'); d.append(el('summary', title)); return d; };
  const header = el('header', null, 'pc-header');
  header.append(el('div', 'SEEGER WEISS / PRACTICE INTELLIGENCE', 'pc-eyebrow'));
  const title = el('div', null, 'pc-title');
  title.append(el('h1', 'Platform resources'), link('Explore agent skills →', 'SKILLS.html'));
  header.append(title, el('p', 'Useful source material, integration references, and practical tools for the firm’s AI workspace.', 'pc-intro'));
  const nav = el('nav'); nav.setAttribute('aria-label', 'Library navigation');
  for (const [label, path] of [['Documents','index.html'],['Court coverage','COVERAGE.html'],['Rules & sources','RULES.html'],['Primary law','LAW.html'],['Additional sources','EXTENDED-LAW.html'],['Workflow toolkit','TOOLKIT.html'],['Agent skills','SKILLS.html']]) nav.append(link(label,path));
  const current = el('span','Platform resources'); current.setAttribute('aria-current','page'); nav.append(current); header.append(nav); root.append(header);
  const main = el('main');
  const metrics = el('div',null,'pc-metrics');
  for (const [n, label, desc] of [[150,'Capabilities','Firm instructions and role specifications'],[14,'Enriched agents','Contracts, mini-app forms, and review scenarios'],[20,'Source references','Purpose and limitations checked against primary sources'],[5,'Local utilities','Deterministic checks with 54 passing tests']]) {
    const item=el('div'); item.append(el('strong',String(n)),el('span',label),el('p',desc)); metrics.append(item);
  }
  main.append(metrics);
  const tabBar=el('div',null,'pc-tabs');tabBar.setAttribute('role','tablist');tabBar.setAttribute('aria-label','Resource views');
  const tabs=[['sources','Source library'],['tools','Local tools']];
  for(const [id,label]of tabs){const b=button(label,()=>setTab(id));b.id='pc-tab-'+id;b.setAttribute('role','tab');b.setAttribute('aria-controls','pc-content');b.addEventListener('keydown',e=>{const i=tabs.findIndex(t=>t[0]===id);if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length;setTab(tabs[next][0]);tabBar.children[next].focus();}});tabBar.append(b);}
  main.append(tabBar);
  const toolbar=el('div',null,'pc-toolbar');const searchLabel=el('label','Search resources');const search=el('input');search.type='search';search.placeholder='Retrieval, court data, documents, citations…';search.setAttribute('aria-label','Search resources');searchLabel.append(search);
  const categoryLabel=el('label','Category');const category=el('select');category.setAttribute('aria-label','Resource category');categoryLabel.append(category);toolbar.append(searchLabel,categoryLabel,button('Reset',()=>{search.value='';state.query='';category.value='';state.category='';render();}));
  search.addEventListener('input',()=>{state.query=search.value;render();});category.addEventListener('change',()=>{state.category=category.value;render();});main.append(toolbar);
  const status=el('p',null,'pc-status');status.setAttribute('role','status');main.append(status);
  const content=el('section',null,'pc-content');content.id='pc-content';content.setAttribute('role','tabpanel');content.tabIndex=0;main.append(content);
  const footer=el('footer',null,'pc-footer');footer.append(el('span','Public reference package · Source-specific review dates'),link('Full analysis','11-Platform-Corpus/ANALYSIS.md'),link('Integration guide','11-Platform-Corpus/integration/INTEGRATION.md'),link('Data boundaries','11-Platform-Corpus/INGESTION-POLICY.json'));main.append(footer);root.append(main);
  function setTab(tab){state.tab=tab;state.category='';state.query='';search.value='';category.replaceChildren();const all=el('option','All categories');all.value='';category.append(all);const values=tab==='sources'?[...new Set(data.sources.map(r=>r.category))].sort():[];for(const v of values){const o=el('option',v);o.value=v;category.append(o);}categoryLabel.hidden=tab!=='sources';toolbar.hidden=tab==='tools';for(const [i,[id]]of tabs.entries()){const b=tabBar.children[i];b.setAttribute('aria-selected',String(id===tab));b.tabIndex=id===tab?0:-1;}content.setAttribute('aria-labelledby','pc-tab-'+tab);render();}
  function matches(r){return(!state.category||r.category===state.category)&&state.query.toLowerCase().trim().split(/\s+/).filter(Boolean).every(t=>JSON.stringify([r.title,r.category,r.use_case,r.useful_for,r.behavior,r.limits]).toLowerCase().includes(t));}
  function render(){content.replaceChildren();if(state.tab==='sources')renderSources();else renderTools();}
  function renderSources(){const rows=data.sources.filter(matches);status.textContent=rows.length+' source references · Documentation reviewed; datasets and integrations are not installed by this package.';const grid=el('div',null,'pc-grid');for(const r of rows){const card=el('article',null,'pc-card');card.append(el('div',r.category,'pc-eyebrow'),el('h2',r.title),el('p',r.use_case));const tags=el('div',null,'pc-tags');for(const value of r.useful_for||[])tags.append(el('span',value.replaceAll('_',' ').replaceAll('.',' / ')));card.append(tags);const detail=disclosure('Use, limits & next step');detail.append(el('strong',r.qualification),list(r.limits),el('p',r.next_step));card.append(detail);const source=disclosure('Source & license record');source.append(external(r.provider||'Primary source',r.canonical_url),el('p',r.acquisition_status),el('p','Code: '+(r.licensing.code||'See source-specific record')),el('p','Data: '+(r.licensing.data||'See source-specific record')),link('Complete evidence record','11-Platform-Corpus/SOURCE-REGISTRY.json'));card.append(source);grid.append(card);}if(!rows.length)grid.append(el('p','No matching resources. Try a broader search.','pc-empty'));content.append(grid);}
  function renderTools(){status.textContent='Five working local utilities · Python standard library · No network or model calls';const intro=el('div',null,'pc-note');intro.append(el('strong','Make missing coverage visible before relying on an answer.'),el('p','These tools operate on explicit source manifests, extracted text and result ledgers. They verify structure and literal evidence; they do not certify extraction quality or legal reasoning.'),link('Read usage and input formats','11-Platform-Corpus/tools/README.md'));content.append(intro);const grid=el('div',null,'pc-grid');for(const t of data.tools){const c=el('article',null,'pc-card');c.append(el('div',t.tag,'pc-eyebrow'),el('h2',t.title),el('p',t.description),el('pre',t.command),el('p',t.limit,'pc-secondary'));grid.append(c);}content.append(grid);const resources=el('div',null,'pc-downloads');for(const [label,path]of[['Python utilities','tools/corpus_tools.py'],['54-test suite','tools/test_corpus_tools.py'],['Synthetic examples','tools/examples/README.md'],['Utility guide','tools/README.md'],['Ingestion policy','INGESTION-POLICY.json']])resources.append(link(label,'11-Platform-Corpus/'+path));content.append(resources);}
  setTab('sources');
})();
