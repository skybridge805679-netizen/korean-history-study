// 요약노트·핵심노트의 표시 용어가 70~79회 기출(문제·자료·선지·해설)에 실제로 나오는지 검사
// node tools/check_grounding.js [summary|notes] [-v] [시트id]
const fs=require("fs"),path=require("path");
const site=path.join(__dirname,"..","site");
const {QS}=require("./check_clues.js");
global.window={};
eval(fs.readFileSync(path.join(site,"question-explanations.js"),"utf8"));
const E=window.QUESTION_EXPLANATIONS;
const norm=s=>String(s).replace(/[\s·ㆍ,.\-‧'"“”‘’《》〈〉「」『』()]/g,"");
const corpus=norm(QS.map(q=>[q.q,q.ctx,q.ch.join(" "),q.exp,JSON.stringify(E[q.r+"-"+q.n]||{})].join(" ")).join(" "));
const mode=process.argv[2]&&!process.argv[2].startsWith("-")?process.argv[2]:"summary";
const verbose=process.argv.includes("-v");
function ground(chip){
  // 괄호 안 보충은 제외하고, ·/→ 로 나뉜 각 낱말이 기출에 있는지
  const base=chip.replace(/\([^)]*\)/g,"").split(/[·→/,]|\s{2,}|:/).map(norm).filter(x=>x.length>=2&&!/^[0-9]+$/.test(x));
  if(!base.length)return {ok:true,missing:[]};
  const missing=base.filter(t=>!corpus.includes(t)&&!(t.length>3&&corpus.includes(t.slice(0,-1))));
  return {ok:missing.length===0,missing};
}
let tot=0,bad=0;const rows=[];
if(mode==="summary"){
  const dir=path.join(site,"summary");
  for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(dir,f),"utf8"));
  for(const s of window.SUMMARY_SHEETS){
    if(s.id.startsWith("heritage"))continue;
    let t=0,b=0;const miss=[];
    const scan=txt=>{for(const m of String(txt).matchAll(/\{([rbgyx]):([^{}]*)\}/g)){t++;const g=ground(m[2]);if(!g.ok){b++;miss.push(m[2])}}};
    const walk=n=>{if(typeof n==="string")scan(n);else{scan(n.t);(n.c||[]).forEach(walk)}};
    for(const sec of s.sections)for(const it of sec.body){
      if(it.line)scan(it.line);if(it.note)scan(it.note);if(it.tree)walk(it.tree);if(it.flow)it.flow.forEach(scan);
      if(it.grid)for(const r of it.grid.rows)r.forEach(c=>scan(typeof c==="string"?c:c.t));
    }
    tot+=t;bad+=b;console.log(`${s.id}: 강조어 ${t} · 기출에 없는 것 ${b} (${Math.round(b/t*100)}%)`);
    if(verbose&&(process.argv[3]===s.id||!process.argv[3]||process.argv[3]==="-v"))console.log("   "+miss.join(" | "));
  }
}else{
  const dir=path.join(site,"core-notes");
  for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(dir,f),"utf8"));
  for(const n of window.CORE_NOTES){
    let t=0,b=0;const miss=[];
    for(const tb of n.tables||[])for(const r of tb.r){const g=ground(String(r[0]));t++;if(!g.ok){b++;miss.push(r[0])}}
    for(const k of n.keys||[]){for(const x of String(k[0]).split(/[·]/)){t++;const g=ground(x);if(!g.ok){b++;miss.push(x)}}}
    tot+=t;bad+=b;if(verbose)console.log(`${n.id}: ${t} 중 ${b}`+(b?"  "+miss.slice(0,12).join(" | "):""));
  }
}
console.log(`합계: ${tot} 중 기출에 없는 것 ${bad} (${Math.round(bad/tot*100)}%)`);
