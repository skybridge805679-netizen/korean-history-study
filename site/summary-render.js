// 손필기식 요약노트 렌더러. 데이터: window.SUMMARY_SHEETS (summary/*.js), 형식은 docs/summary-notes.md 참고.
(function(){
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const CLS={r:"sm-r",b:"sm-b",g:"sm-g",y:"sm-y",x:"sm-x",n:"sm-n",s:"sm-s"};
const COUNTED=new Set(["r","b","g","y","x"]);
let counter=null;
// {r:문구} 형식의 인라인 표시를 HTML로 바꾼다. r 빨강(정답·빈출) b 파랑 g 초록 y 형광 x 네모 n 작은 회색 메모 s 빨간 X(오답 함정)
function inline(s){
  return esc(s).replace(/\{([rbgyxns]):([^{}]*)\}/g,(m,c,t)=>{
    const raw=t.replace(/&amp;/g,"&").replace(/&lt;/g,"<").replace(/&gt;/g,">").replace(/&quot;/g,'"');
    let sup="";
    if(counter&&COUNTED.has(c)){const k=counter(raw);if(k&&k.length)sup=`<sup class="sm-q" data-smq="${esc(raw)}" title="이 용어가 나온 기출 ${k.length}문항 — 눌러서 풀기">${k.length}</sup>`}
    return `<span class="${CLS[c]}">${t}</span>${sup}`;
  });
}
const lines=s=>String(s).split("\n").map(l=>`<div class="sm-ln">${inline(l)}</div>`).join("");
function tree(n){
  if(typeof n==="string")return `<div class="sm-ln">${inline(n)}</div>`;
  return `<div class="sm-node"><div class="sm-ln">${inline(n.t)}</div>${n.c?`<div class="sm-kids">${n.c.map(tree).join("")}</div>`:""}</div>`;
}
function item(it){
  if(it.line!=null)return `<div class="sm-line" style="margin-left:${(it.ind||0)*16}px">${lines(it.line)}</div>`;
  if(it.note!=null)return `<div class="sm-note">${inline(it.note)}</div>`;
  if(it.tree)return `<div class="sm-tree">${tree(it.tree)}</div>`;
  if(it.flow)return `<div class="sm-flow">${it.flow.map(x=>`<span class="sm-step">${inline(x)}</span>`).join('<span class="sm-arrow">→</span>')}</div>`;
  if(it.grid){const g=it.grid;
    return `<div class="sm-gridwrap"><table class="sm-grid" style="--cols:${g.cols.length}"><thead><tr>${g.cols.map(c=>`<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${g.rows.map(r=>`<tr>${r.map((c,i)=>{const hl=typeof c==="object"&&!Array.isArray(c)&&c.hl;const t=typeof c==="object"&&!Array.isArray(c)?c.t:c;return `<${i?"td":"th"} class="${i?"":"sm-rowh"} ${hl?"sm-hl":""}">${lines(t||"")}</${i?"td":"th"}>`}).join("")}</tr>`).join("")}</tbody></table></div>`}
  if(it.gallery)return `<div class="sm-gallery">${it.gallery.map(p=>`<figure class="sm-fig"><img loading="lazy" src="${esc(p.img)}" alt="${esc(p.name)}"><figcaption><b>${inline(p.name)}</b>${p.note?`<span>${inline(p.note)}</span>`:""}${p.credit?`<span class="sm-credit">© ${esc(p.credit)}</span>`:""}${p.q?`<a class="sm-qlink" data-smgo="${esc(p.q)}">기출 ${esc(p.q)}</a>`:""}</figcaption></figure>`).join("")}</div>`;
  return "";
}
function sheet(s,opt){
  counter=opt&&opt.counter;
  return `<article class="sm-sheet" id="sm-${esc(s.id)}">
  <div class="sm-head"><div class="sm-script">study</div><div class="sm-exam">한국사능력검정시험 – 심화</div></div>
  <div class="sm-title"><span>TITLE</span><b>@오르페이아 ${esc(s.title)}</b><span class="sm-date">70~79회 기출 500문항 기반</span></div>
  <div class="sm-body">${s.sections.map(sec=>`<section class="sm-sec ${sec.w==="full"?"sm-full":""}"><h4 class="sm-h">${inline(sec.h)}</h4>${sec.body.map(item).join("")}</section>`).join("")}</div>
  </article>`;
}
window.SummaryNotes={sheet};
})();
