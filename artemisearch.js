// Copyright 2026 Cohnsoft. AGPL-3.0-or-later.
// Request-scoped lenses; no history, tracking, telemetry, or browser storage.
(()=>{
 const form=document.querySelector('#search') || document.querySelector('form[action*="search"]');
 if(!form)return;
 const taggedLens=[...(document.querySelector('#q')?.value||'').matchAll(/(?:^|\s)#(balanced|research|discovery)(?=\s|$)/gi)].pop()?.[1]?.toLowerCase();
 const current=taggedLens||new URL(location.href).searchParams.get('lens')||'balanced';
 const lenses=[['balanced','Balanced','Agreement, relevance, and variety'],['research','Research','More weight on the words you searched'],['discovery','Discovery','More variety across sites and overlapping text']];
 const bar=document.createElement('div');bar.className='artemis-lenses';bar.setAttribute('role','group');bar.setAttribute('aria-label','Search perspective');
 const hidden=document.createElement('input');hidden.type='hidden';hidden.name='lens';hidden.value=lenses.some(x=>x[0]===current)?current:'balanced';form.append(hidden);
 const label=document.createElement('span');label.textContent='Perspective';bar.append(label);
 for(const[id,name,title]of lenses){const button=document.createElement('button');button.type='button';button.textContent=name;button.title=title;button.setAttribute('aria-pressed',String(id===hidden.value));button.onclick=()=>{hidden.value=id;for(const child of bar.querySelectorAll('button'))child.setAttribute('aria-pressed',String(child===button));if(new URL(location.href).searchParams.has('q')){const page=form.querySelector('[name="pageno"]');if(page)page.value='1';form.requestSubmit();}};bar.append(button)}
 form.insertAdjacentElement('afterend',bar);
 const footer=document.createElement('p');footer.className='artemis-credit';footer.append('Cohnsoft Search · Ad-free metasearch by Cohnsoft. ');const link=document.createElement('a');link.href='https://github.com/danecohn/Artemisearch/blob/main/ATTRIBUTION.md';link.textContent='Built on SearXNG / AltStackSearch · Inspired by AT Protocol';footer.append(link);document.querySelector('footer')?.prepend(footer);
})();
(()=>{
 const form=document.querySelector('#search');if(!form)return;const input=form.querySelector('[name=q]');if(!input)return;
 const help=document.createElement('details');help.className='artemis-tags-help';const summary=document.createElement('summary');summary.textContent='Narrow it with #tags';help.append(summary);const description=document.createElement('p');description.textContent='Combine controls such as #research #docs #opensource #news #week #site:apple.com #lang:en. Any other topic tag, like #astronomy, requires those words in the title, snippet, or URL. Time and language filters depend on source-provider support. Narrowing may return fewer or no results.';help.append(description);const examples=document.createElement('div');for(const tag of ['#research','#docs','#opensource','#news','#week','#site:apple.com']){const button=document.createElement('button');button.type='button';button.textContent=tag;button.onclick=()=>{input.value=(input.value.trim()+' '+tag).trim();input.focus()};examples.append(button)}help.append(examples);const anchor=document.querySelector('.artemis-lenses')||form;anchor.insertAdjacentElement('afterend',help);
 const chips=document.createElement('div');chips.className='artemis-active-tags';chips.setAttribute('aria-label','Active hashtag controls');const tags=input.value.match(/(?:^|\s)#[\w.-]+(?::[^\s#]+)?/gu)||[];for(const match of tags){const tag=match.trim();const button=document.createElement('button');button.type='button';button.textContent=tag+' ×';button.setAttribute('aria-label','Remove '+tag);button.onclick=()=>{input.value=input.value.replace(tag,'').replace(/\s+/g,' ').trim();const page=form.querySelector('[name=pageno]');if(page)page.value='1';form.requestSubmit()};chips.append(button)}if(tags.length)help.insertAdjacentElement('afterend',chips);
})();
// Preserve explicit hashtag intent and the selected lens across result pages.
(()=>{const q=document.querySelector('#q')?.value;if(!q)return;const lens=new URL(location.href).searchParams.get('lens')||'balanced';for(const link of document.querySelectorAll('#pagination a')){const url=new URL(link.href,location.href);if(url.origin===location.origin){url.searchParams.set('q',q);url.searchParams.set('lens',lens);link.href=url.href;}}})();
