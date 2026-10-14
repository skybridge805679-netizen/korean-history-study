// 핵심노트 커버리지·형식 검사: node tools/check_core_notes.js
const fs=require("fs"),path=require("path");
const site=path.join(__dirname,"..","site");
const L=fs.readFileSync(path.join(site,"index.html"),"utf8").split("\n");
const QS=eval("("+L.find(x=>x.startsWith("const QS=")).slice(9).replace(/;\s*$/,"")+")");
global.window={};
for(const f of fs.readdirSync(path.join(site,"core-notes")).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(site,"core-notes",f),"utf8"));
const N=window.CORE_NOTES,key=q=>q.r+"-"+q.n;let err=0;
const bad=m=>{console.log("✗",m);err++};
const ids=new Set();
for(const n of N){
  if(!n.id||ids.has(n.id))bad("id 중복/누락 "+n.id);ids.add(n.id);
  if(!n.title||!n.era||!n.match?.length)bad("필수 필드 누락 "+n.id);
  if(!n.tables?.length)bad("표 없음 "+n.id);
  for(const t of n.tables||[]){if(!t.h||!t.r?.length)bad("표 형식 "+n.id);for(const r of t.r||[])if(r.length!==t.h.length)bad(`열 수 불일치 ${n.id}: ${r[0]}`)}
  for(const k of n.keys||[])if(k.length!==2)bad("키워드 형식 "+n.id);
}
const idx={};N.forEach(n=>n.match.forEach(m=>(idx[m]=idx[m]||[]).push(n)));
const miss=[];const cnt={};
for(const q of QS){const ns=new Set([...(idx[q.era+"/"+q.topic]||[]),...(idx[key(q)]||[])]);if(!ns.size)miss.push(key(q)+" "+q.era+"/"+q.topic);ns.forEach(n=>cnt[n.id]=(cnt[n.id]||0)+1)}
const used=new Set(QS.flatMap(q=>[q.era+"/"+q.topic,key(q)]));
for(const n of N)for(const m of n.match)if(!used.has(m))bad(`연결 없는 match: ${n.id} ${m}`);
console.log(`노트 ${N.length}개 · 문항 ${QS.length}개 · 미연결 ${miss.length}개`);
if(miss.length){const g={};miss.forEach(m=>{const t=m.split(" ").slice(1).join(" ");(g[t]=g[t]||[]).push(m.split(" ")[0])});for(const [t,a] of Object.entries(g))console.log("  미연결",t,a.join(","))}
console.log("노트별 문항 수:",Object.entries(cnt).sort((a,b)=>b[1]-a[1]).slice(0,5).map(([k,v])=>k+":"+v).join(", "));
const chars=JSON.stringify(N).length;console.log("데이터 크기",Math.round(chars/1000)+"K자");
process.exit(err||miss.length?1:0);
