// Copyright 2026 Artemis Softworks LLC. AGPL-3.0-or-later.
// Request-scoped lenses; no history, tracking, telemetry, or browser storage.
(()=>{
 const form=document.querySelector('#search') || document.querySelector('form[action*="search"]');
 if(!form)return;
 const current=new URL(location.href).searchParams.get('lens')||'balanced';
 const lenses=[['balanced','Balanced','Agreement, relevance, and variety'],['research','Research','More weight on the words you searched'],['discovery','Discovery','More variety across sites and overlapping text']];
 const bar=document.createElement('div');bar.className='artemis-lenses';bar.setAttribute('role','group');bar.setAttribute('aria-label','Search perspective');
 const hidden=document.createElement('input');hidden.type='hidden';hidden.name='lens';hidden.value=lenses.some(x=>x[0]===current)?current:'balanced';form.append(hidden);
 const label=document.createElement('span');label.textContent='Perspective';bar.append(label);
 for(const[id,name,title]of lenses){const button=document.createElement('button');button.type='button';button.textContent=name;button.title=title;button.setAttribute('aria-pressed',String(id===hidden.value));button.onclick=()=>{hidden.value=id;for(const child of bar.querySelectorAll('button'))child.setAttribute('aria-pressed',String(child===button));if(new URL(location.href).searchParams.has('q')){const page=form.querySelector('[name="pageno"]');if(page)page.value='1';form.requestSubmit();}};bar.append(button)}
 form.insertAdjacentElement('afterend',bar);
 const footer=document.createElement('p');footer.className='artemis-credit';footer.append('Artemisearch · Ad-free metasearch by Artemis Softworks LLC. ');const link=document.createElement('a');link.href='https://github.com/danecohn/Artemisearch/blob/main/ATTRIBUTION.md';link.textContent='Built on SearXNG / AltStackSearch · Inspired by AT Protocol';footer.append(link);document.querySelector('footer')?.prepend(footer);
})();
