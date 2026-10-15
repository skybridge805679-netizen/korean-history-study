#!/usr/bin/env python3
"""docs/heritage-status.md 생성: 수집 현황(반영됨/검수 탈락/남은 것)."""
import json,os
R=os.path.join(os.path.dirname(__file__),"..","..")
T=json.load(open(os.path.join(R,"tools/heritage/targets.json")))
C=json.load(open(os.path.join(R,"site/heritage/credits.json")))
REJ={
"gaya-iron-ingot":"덩이쇠가 아니라 철제 갑옷 부품 사진이 걸려 탈락(덩이쇠 사진을 다시 찾아야 함)",
"cheolgam-seonsa-pagoda":"쌍봉사 담장과 정자 사진이라 철감선사탑(승탑)이 아니어서 탈락",
"gosagwansudo":"받은 사진이 강희안의 다른 산수화라 고사관수도로 확인되지 않아 탈락", # 내려받았지만 사진을 열어 보고 탈락시킨 것(사유)


}
done=[t for t in T if t["id"] in C];rej=[t for t in T if t["id"] in REJ and t["id"] not in C]
todo=[t for t in T if t["id"] not in C and t["id"] not in REJ]
L=["# 문화재 사진 수집 현황","",
"기출 사진만으로는 문화재 사진이 부족해 Wikimedia Commons(자유 이용) 사진으로 보강하는 작업의 현황이다. 이어서 할 때는 아래 '남은 것'을 처리한다.","",
"## 작업 방법","",
"1. `python3 tools/heritage/fetch.py [--only id,id]` — `tools/heritage/targets.json` 의 항목을 Commons 에서 검색해 `site/heritage/<id>.jpg` 와 `credits.json`(저작자·라이선스·원본 주소)을 만든다. Commons 가 요청을 자주 429 로 거절하므로 간격을 두고 여러 번 돌린다(이미 받은 것은 건너뜀). 직접 Commons 에서 골라 같은 형식으로 넣어도 된다.",
"2. **받은 사진을 반드시 열어 보고** 이름과 맞는지 확인한다. 자동 검색 결과는 엉뚱한 사진(다른 유물·내부 사진·옛 신문 스캔 등)이 걸릴 수 있다. 틀리면 `targets.json` 의 `q` 를 고치거나 파일 제목을 직접 지정해 다시 받는다. 탈락 사유는 `tools/heritage/status.py` 의 `REJ` 에 적는다.",
"3. 확인된 사진은 `tools/heritage/build_sheets.py` 의 `N`(이름·설명)과 `GROUPS`에 추가하고 `python3 tools/heritage/build_sheets.py` 로 `site/summary/heritage.js` 를 다시 만든다. 설명은 확실한 사실만 쓴다.",
"4. `node tools/check_summary.js` 통과, `python3 tools/heritage/status.py` 로 이 문서 갱신 후 커밋한다.","",
f"## 반영됨 ({len(done)}점) — 사진 확인 완료, 요약노트 ‘문화재 사진’에 표시","",
"| id | 이름 | 시대 | 라이선스 |","|---|---|---|---|"]
for t in done:L.append(f'| {t["id"]} | {t["name"]} | {t["era"]} | {C[t["id"]]["license"]} |')
L+=["",f"## 검수 탈락 ({len(rej)}점) — 다시 찾아야 함","","| id | 이름 | 사유 |","|---|---|---|"]
for t in rej:L.append(f'| {t["id"]} | {t["name"]} | {REJ[t["id"]]} |')
L+=["",f"## 남은 것 ({len(todo)}점) — 아직 받지 못함","","429(요청 제한)로 실패했거나 검색에서 자유 라이선스 사진이 잡히지 않은 항목이다. 검색어(`q`)를 바꾸거나 Commons 에서 직접 찾는다.","","| id | 이름 | 시대 | 검색어(q) |","|---|---|---|---|"]
for t in todo:L.append(f'| {t["id"]} | {t["name"]} | {t["era"]} | {t["q"]} |')
open(os.path.join(R,"docs/heritage-status.md"),"w").write("\n".join(L)+"\n")
print(len(done),len(rej),len(todo))
