// 요약노트 검사: node tools/check_summary.js [시대]  — 형식·이미지·문항번호 검사 + 시대별 단서 커버리지
const fs=require("fs"),path=require("path");
const site=path.join(__dirname,"..","site");
const {QS,terms,GEN,key}=require("./check_clues.js");
global.window={};
const dir=path.join(site,"summary");
for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(dir,f),"utf8"));
const SH=window.SUMMARY_SHEETS||[];let err=0;const bad=m=>{console.log("✗",m);err++};
const byKey=Object.fromEntries(QS.map(q=>[key(q),q]));
const strip=s=>s.replace(/\{[rbgyxns]:([^{}]*)\}/g,"$1");
const cellText=c=>typeof c==="string"?c:c.t;
const texts={};
function walkTree(n,out){out.push(typeof n==="string"?n:n.t);if(n.c)n.c.forEach(x=>walkTree(x,out))}
for(const s of SH){
  if(!s.id||!s.era||!s.title||!s.sections?.length)bad("필수 필드 "+s.id);
  const out=[];
  for(const sec of s.sections||[]){out.push(sec.h);
    for(const it of sec.body||[]){
      if(it.line!=null)out.push(it.line);else if(it.note!=null)out.push(it.note);
      else if(it.tree)walkTree(it.tree,out);else if(it.flow)out.push(...it.flow);
      else if(it.grid){const g=it.grid;out.push(...g.cols);
        for(const r of g.rows){if(r.length!==g.cols.length)bad(`${s.id} 열 수 불일치: ${strip(cellText(r[0]))}`);r.forEach(c=>out.push(cellText(c)))}}
      else if(it.gallery)for(const p of it.gallery){
        if(!fs.existsSync(path.join(site,p.img.split("?")[0])))bad(`${s.id} 이미지 없음 ${p.img}`);
        if(p.q&&!byKey[p.q])bad(`${s.id} 문항 없음 ${p.q}`);out.push(p.name,p.note||"")}
      else bad(`${s.id} 알 수 없는 블록 ${Object.keys(it)}`);
    }}
  const t=out.join("\n");
  const open=(t.match(/\{[rbgyxns]:/g)||[]).length,all=(t.match(/\{[a-z]?:?/g)||[]).length;
  if((t.replace(/\{[rbgyxns]:[^{}]*\}/g,"").match(/[{}]/g)||[]).length)bad(`${s.id} 표시 괄호 오류`);
  texts[s.id]=strip(t).replace(/\s/g,"");
  const col={r:0,b:0,g:0,y:0,x:0};for(const m of t.matchAll(/\{([rbgyx]):/g))col[m[1]]++;
  console.log(`${s.id} (${s.era}) 글자 ${texts[s.id].length} · 색 ${JSON.stringify(col)}`);
}
const only=process.argv[2];
for(const era of [...new Set(QS.map(q=>q.era))]){
  if(only&&era!==only)continue;
  const txt=SH.filter(s=>(s.eras||[s.era]).includes(era)).map(s=>texts[s.id]).join("");
  const qs=QS.filter(q=>q.era===era);if(!txt)continue;let miss=0;const rep=[];
  for(const q of qs){const m=terms(q).filter(t=>!GEN(t)).filter(t=>!txt.includes(t)&&!(t.length>3&&txt.includes(t.slice(0,-1))));if(m.length){miss++;rep.push(key(q)+" "+m.join(" "))}}
  console.log(`[${era}] 문항 ${qs.length} · 단서 누락 있는 문항 ${miss}`);
  if(process.argv.includes("-v"))rep.forEach(x=>console.log("   ",x));
}
process.exit(err?1:0);
