const fs=require('fs');
const B='https://fermi.ai';
const dec=s=>s.replace(/&amp;/g,'&').replace(/&#39;|&apos;/g,"'").replace(/&quot;/g,'"').replace(/&lt;/g,'<').replace(/&gt;/g,'>');
async function get(p,n=4){for(let i=0;i<n;i++){try{const r=await fetch(B+p);if(r.ok)return await r.text();if(r.status==404)return null;}catch(e){}await new Promise(r=>setTimeout(r,500*(i+1)));}return null;}
function parse(html){
  const m=html.match(/<main id="prerender">([\s\S]*?)<\/main>/); if(!m) return null;
  const body=m[1].replace(/<nav[\s\S]*?<\/nav>/g,'');
  const h1=(body.match(/<h1>([\s\S]*?)<\/h1>/)||[])[1];
  const sub=(body.match(/<h1>[\s\S]*?<\/h1>\s*<p>([\s\S]*?)<\/p>/)||[])[1]||'';
  const items=[...body.matchAll(/<li><a href="([^"]+)">([\s\S]*?)<\/a>(?:\s*—\s*([\s\S]*?))?<\/li>/g)].map(x=>({href:x[1],title:dec(x[2].replace(/<[^>]+>/g,'')),note:x[3]?dec(x[3].replace(/<[^>]+>/g,'')):''}));
  return {title:dec(h1||''),sub:dec(sub.replace(/<[^>]+>/g,'')),items};
}
async function node(path,depth=0){
  const h=await get(path); const p=h&&parse(h);
  if(!p) return {path,error:true,children:[],leaves:[]};
  const kids=p.items.filter(i=>i.href.startsWith('/concept/')&&i.href!==path);
  const leaves=p.items.filter(i=>!i.href.startsWith('/concept/'));
  const out={path,title:p.title,sub:p.sub,children:[],leaves:leaves.map(l=>({title:l.title,path:l.href}))};
  const res=[];let idx=0;
  async function worker(){while(idx<kids.length){const k=kids[idx++];const c=await node(k.href,depth+1);c.title=c.title||k.title;c.note=k.note;res[kids.indexOf(k)]=c;}}
  await Promise.all(Array.from({length:depth<2?3:1},worker));
  out.children=res;return out;
}
(async()=>{
  const h=await get('/concept');const p=parse(h);
  const roots=p.items.filter(i=>i.href.startsWith('/concept/'));
  console.log('roots',roots.length);
  const tree=fs.existsSync('tree.json')?JSON.parse(fs.readFileSync('tree.json')):{title:'Fermi Concept Library',children:[]};
  for(const r of roots){if(tree.children.some(c=>c.path===r.href))continue;const c=await node(r.href);c.note=r.note;c.title=c.title||r.title;tree.children.push(c);
    const cnt=n=>n.leaves.length+n.children.reduce((a,c)=>a+cnt(c),0);console.log(c.title,cnt(c));
    fs.writeFileSync('tree.json',JSON.stringify(tree));}
})();
