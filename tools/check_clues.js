// 문항 단서 커버리지: 문항 exp·선지의 고유명 단서가 연결 노트의 표·키워드에 있는지 검사
// node tools/check_clues.js [--all] [문항키]
const fs=require("fs"),path=require("path");
const site=path.join(__dirname,"..","site");
const L=fs.readFileSync(path.join(site,"index.html"),"utf8").split("\n");
const QS=eval("("+L.find(x=>x.startsWith("const QS=")).slice(9).replace(/;\s*$/,"")+")");
global.window={};
for(const f of fs.readdirSync(path.join(site,"core-notes")).filter(f=>f.endsWith(".js")).sort())eval(fs.readFileSync(path.join(site,"core-notes",f),"utf8"));
const N=window.CORE_NOTES,key=q=>q.r+"-"+q.n;
const idx={};N.forEach(n=>n.match.forEach(m=>(idx[m]=idx[m]||[]).push(n)));
const strip=s=>s.replace(/<[^>]+>/g,"");
const noteText=n=>strip(JSON.stringify([n.tables,n.keys])).replace(/[\s"\\\[\],·ㆍ()]/g,"");
const STOP=new Set(("시기 이후 이전 때로 모두 정답 문제 사실 설명 내용 시대 나라 왕이 하였 했다 있다 였다 된다 하는 위한 통해 대한 에서 으로 에게 같은 다른 이다 아니 않은 않았 국가 지역 사람 시작 결과 이후의 이전의 당시 처음 최초 이를 이에 그리고 하지 또한 여러 일부 전체 관련 주요 중심 가장").split(" "));
const JOSA=/(으로|에서|에게|까지|부터|이며|이고|이다|였다|했다|하였다|하였|이라|라고|에는|으로는|에도|과의|와의|들의|은|는|이|가|을|를|의|에|와|과|도|로|만|며|고|들)$/;
function terms(q){
  const lhs=q.exp.split("→")[0];
  const rest=q.exp.replace(/①.*$/,"");
  const choice=q.exp.match(/①.*$/)?.[0]||"";
  const src=[lhs,...(q.exp.includes("→")?[q.exp.split("→")[1].split("①")[0]]:[]),choice];
  const out=new Set();
  for(const s of src)for(let t of (s.match(/[가-힣0-9]{2,}/g)||[])){
    t=t.replace(/^[0-9]+$/,"");if(!t)continue;
    let b=t;for(let i=0;i<2;i++){const m=b.replace(JOSA,"");if(m.length>=2)b=m}
    if(b.length<2||STOP.has(b)||/^(하|했|되|된|있|없|이었|였)/.test(b))continue;
    out.add(b);
  }
  return [...out];
}
const only=process.argv.slice(2).filter(a=>a[0]!=="-")[0],all=process.argv.includes("--all");
const df={};for(const q of QS)for(const t of terms(q))df[t]=(df[t]||0)+1;
const GEN=t=>df[t]>=10||/^(.*(하여|하고|했|하며|했다|시켰|되었|되어|받았|이었|한다|하는|하다|한|된|적|인|으로|에서|이라|처럼|까지|보다|라는|라고|었다|았다|졌다|겼다|했던|하였던|시켜|시킨|받아|받은|맺었다|두어|파견해|가르쳤다|사용|설치|실시|지원|확산|철회|생산|활동|개봉|모집|선택지|문화유산|해석|출신|새긴|함께|대표|기원|기준|간행|담당|교재|공부|따라|차지|직후|발발|체결|소유|토지|도읍|국호|부하|지배층|유행|탈환|참전|종결|교역|난|등을|등))$/.test(t);
module.exports={QS,terms,GEN,key};
if(require.main===module){
let tot=0,bad=0;const rep=[];
for(const q of QS){
  if(only&&key(q)!==only)continue;
  const ns=[...new Set([...(idx[q.era+"/"+q.topic]||[]),...(idx[key(q)]||[])])];
  const txt=ns.map(noteText).join("");
  const miss=terms(q).filter(t=>!GEN(t)).filter(t=>!txt.includes(t)&&!(t.length>=3&&txt.includes(t.slice(0,-1))&&/[가-힣]$/.test(t)&&t.length>3));
  tot++;if(miss.length){bad++;rep.push([key(q),ns.map(n=>n.id).join("+"),miss])}
}
for(const [k,n,m] of rep)console.log(k,n,"✗",m.join(" "));
console.log(`문항 ${tot} · 누락 있는 문항 ${bad}`);

}
