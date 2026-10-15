// 용어가 기출에서 어떤 역할로 나오는지 보여 준다(노트의 연결 방향이 기출과 맞는지 확인용).
//   node tools/term_evidence.js 용어 [용어...]
//   node tools/term_evidence.js --sheet <시트id>     시트의 강조어별 근거 요약
// 역할: 자료(ctx)·정답 선지·오답 선지·해설-단서(→ 앞)·해설-정답(→ 뒤, ① 앞)·해설-오답(① 이후)
const fs=require("fs"),path=require("path");
const site=path.join(__dirname,"..","site");
const {QS,key}=require("./check_clues.js");
const norm=s=>String(s).replace(/[\s·ㆍ,.\-‧'"“”‘’《》〈〉「」『』()]/g,"");
const stem=t=>t.length>3?t.slice(0,-1):t;
function roles(term){
  const t=norm(term),out=[];
  for(const q of QS){
    const r=[];
    const has=s=>{const n=norm(s);return n.includes(t)||(t.length>3&&n.includes(stem(t)))};
    if(has(q.ctx||""))r.push("자료");
    q.ch.forEach((c,i)=>{if(has(c))r.push(i+1===q.a?"정답선지":"오답선지")});
    const e=q.exp,ai=e.search(/[①②③④⑤]/),arrow=e.indexOf("→");
    const left=arrow>=0?e.slice(0,arrow):"",mid=arrow>=0?e.slice(arrow+1,ai>=0?ai:undefined):(ai>=0?e.slice(0,ai):e),dis=ai>=0?e.slice(ai):"";
    if(has(left))r.push("해설단서");if(has(mid))r.push("해설정답");if(has(dis))r.push("해설오답");
    if(r.length)out.push({k:key(q),era:q.era,topic:q.topic,r:[...new Set(r)]});
  }
  return out;
}
module.exports={roles,norm};
if(require.main===module){
  const a=process.argv.slice(2);
  if(a[0]==="--sheet"){
    global.window={};const dir=path.join(site,"summary");
    for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(dir,f),"utf8"));
    const s=window.SUMMARY_SHEETS.find(x=>x.id===a[1]);if(!s){console.log("시트 없음");process.exit(1)}
    const seen=new Set();
    const scan=txt=>{for(const m of String(txt).matchAll(/\{([rbgyx]):([^{}]*)\}/g)){const t=m[2].replace(/\([^)]*\)/g,"").split(/[:]/)[0].trim();if(seen.has(t))continue;seen.add(t);
      const ev=roles(t),good=ev.filter(e=>e.r.some(x=>["자료","정답선지","해설단서","해설정답"].includes(x))),bad=ev.filter(e=>!good.includes(e));
      const tag=!ev.length?"기출없음":!good.length?"오답/해설오답에만":"";
      console.log(`${tag?"⚠ "+tag+" ":"  "}${t} | 정답쪽 ${good.map(e=>e.k).join(",")||"-"} | 오답쪽 ${bad.map(e=>e.k).join(",")||"-"}`)}};
    const walk=n=>{if(typeof n==="string")scan(n);else{scan(n.t);(n.c||[]).forEach(walk)}};
    for(const sec of s.sections)for(const it of sec.body){
      if(it.line)scan(it.line);if(it.note)scan(it.note);if(it.tree)walk(it.tree);if(it.flow)it.flow.forEach(scan);
      if(it.grid)for(const r of it.grid.rows)r.forEach(c=>scan(typeof c==="string"?c:c.t));
    }
  }else for(const t of a){console.log("##",t);for(const e of roles(t))console.log("  ",e.k,e.era+"/"+e.topic,e.r.join(","))}
}
