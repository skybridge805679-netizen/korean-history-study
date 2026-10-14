#!/usr/bin/env python3
"""site/heritage/credits.json(검수 통과분) + 아래 설명으로 site/summary/heritage.js 를 만든다."""
import json,os,re
R=os.path.join(os.path.dirname(__file__),"..","..")
C=json.load(open(os.path.join(R,"site/heritage/credits.json")))
# id: (표시 이름, 설명(인라인 표시 허용)) — 사진을 직접 열어 확인한 것만 둔다.
N={
"gwanggaeto-stele":("광개토 대왕릉비(전시 사진)","{r:장수왕} 건립(414)·{b:영락} 연호·신라 구원, 왜 격퇴"),
"chungju-stele":("충주(중원) 고구려비","{r:장수왕}의 남진·{g:국내 유일}의 고구려 비석"),
"seokchon-tomb":("서울 석촌동 고분군","{r:백제} 한성 시기 {b:계단식 돌무지무덤} → 고구려 계통"),
"muryeong-tomb":("공주 무령왕릉 내부","{r:벽돌무덤}(중국 남조 영향)·송산리 고분군·1971 발굴"),
"muryeong-stone":("무령왕릉 지석","{g:무령왕}의 사망 기록·토지신에게 묘지를 산 {b:매지권}"),
"jeongnimsa":("부여 정림사지 오층 석탑","{r:사비} 시기·소정방 기록을 새겨 {b:평제탑}이라 불림"),
"mireuksa":("익산 미륵사지 석탑(복원)","{g:무왕}·가장 큰 석탑·목탑 양식·사리봉영기"),
"yeongnisan-incense":("백제 금동 대향로","{r:능산리} 절터 출토(1993)·{b:도교·불교} 사상"),
"chilji-do":("칠지도","{g:근초고왕}이 왜왕에게 하사(4C)·이소노카미 신궁"),
"cheomseongdae":("경주 첨성대","{g:선덕여왕}·현존 동양 최고(最古) 천문대"),
"bunhwangsa":("분황사 모전 석탑","{g:선덕여왕}·벽돌 모양으로 쌓은 {b:모전 석탑}"),
"jinheung-stele":("북한산 진흥왕 순수비(국립중앙박물관)","{g:진흥왕}·한강 유역 확보·{b:순수비} 4곳(북한산·창녕·황초령·마운령)"),
"gaya-pottery":("기마 인물형 토기(국보 91호)","{r:신라} 토기 — 가야 토기와 구별"),
"bulguksa-dabotap":("불국사 다보탑","{r:통일 신라}·석가탑과 쌍을 이룸·화려한 목조 건축풍"),
"emille-bell":("성덕대왕 신종","{r:통일 신라} 혜공왕 때 완성(771)·{b:에밀레종}"),
"gamunsa":("감은사지 동 삼층 석탑 사리 장엄구","{g:문무왕}이 착공·{b:감은사}·동해 대왕암"),
"hwaeomsa-lion":("구례 화엄사 사사자 삼층 석탑","{r:통일 신라}·네 마리 사자가 받치는 탑 {n:(화엄종)}"),
"anapji":("경주 안압지(동궁과 월지)","{g:문무왕}이 궁 안에 조성(674)·{b:임해전}"),
"mireuk-gwanchoksa":("논산 관촉사 석조 미륵보살 입상","{r:고려} 초·{b:은진 미륵}·거대 불상 양식"),
"hasachang-buddha":("하남 하사창동 철조 석가여래 좌상","{r:고려} 초 {b:철불}·호족 후원"),
"suwol-gwaneum":("수월관음도","{r:고려} 불화 {n:(혜허의 양류관음도도 유명)}"),
"cheongja-sanggam":("청자 상감 운학문 매병","{b:상감 청자}(고려 독창)·12~13C"),
"cheongja-gourd":("청자 참외 모양 주전자","{r:고려} 비색 청자·12C"),
"buseoksa-muryangsujeon":("영주 부석사 무량수전과 석등","{r:고려} 목조 건축·{b:주심포}·배흘림기둥"),
"tripitaka":("팔만대장경 경판","{g:고종} 때 {r:몽골 침입 극복} 기원·합천 해인사 보관"),
"jikji":("직지심체요절","{r:1377} {b:흥덕사}(청주) 금속 활자·현존 최고(最古) 금속 활자본"),
"gyeongbokgung-geunjeongjeon":("경복궁 근정전","{r:조선} 정전·태조 창건(1395)·{g:흥선 대원군} 중건(1867)"),
"hunminjeongeum":("훈민정음 해례본","{g:세종} 1446·{b:국보 70호}·유네스코 기록 유산"),
"cheugugi":("측우기(측우대)","{g:세종} 때 강우량 측정·{b:측우기} {n:(복제)}"),
"angbuilgu":("앙부일구","{g:세종} 때 {b:오목 해시계}·{n:(복제)}"),
}
GROUPS=[
("heritage-1","삼국","삼국 시대 문화재 사진","삼국",["gwanggaeto-stele","chungju-stele","seokchon-tomb","muryeong-tomb","muryeong-stone","jeongnimsa","mireuksa","yeongnisan-incense","chilji-do","cheomseongdae","bunhwangsa","jinheung-stele","gaya-pottery"]),
("heritage-2","남북국","남북국·고려 문화재 사진","남북국",["bulguksa-dabotap","emille-bell","gamunsa","hwaeomsa-lion","anapji","mireuk-gwanchoksa","hasachang-buddha","suwol-gwaneum","cheongja-sanggam","cheongja-gourd","buseoksa-muryangsujeon","tripitaka","jikji"]),
("heritage-3","조선전기","조선 문화재 사진","조선전기",["gyeongbokgung-geunjeongjeon","hunminjeongeum","cheugugi","angbuilgu"]),
]
def credit(c):
    a=re.sub(r"(Unknown author)+","",c["author"]).strip() or "작자 미상"
    a=a.split("\n")[0][:30]
    return f'{a} · {c["license"]}'
out=["// 자동 생성: tools/heritage/build_sheets.py — 직접 고치지 말고 스크립트의 설명을 수정한다.","window.SUMMARY_SHEETS=window.SUMMARY_SHEETS||[];"]
for sid,era,title,_,ids in GROUPS:
    items=[]
    for k in ids:
        if k not in C or k not in N:continue
        name,note=N[k]
        items.append({"img":C[k]["file"],"name":name,"note":note,"credit":credit(C[k])})
    sheet={"id":sid,"era":era,"eras":[era],"title":title,"sections":[{"h":"[사진으로 보는 "+title.replace(" 사진","")+"]","w":"full","body":[{"gallery":items},{"note":"사진은 Wikimedia Commons 의 자유 이용 사진이며 저작자·라이선스는 각 사진 아래와 site/heritage/credits.json 에 있다. 기출 사진이 아닌 '다음 시험에 나올 만한' 문화재로 고른 것이다."}]}]}
    out.append("window.SUMMARY_SHEETS.push("+json.dumps(sheet,ensure_ascii=False,indent=1)+");")
open(os.path.join(R,"site/summary/heritage.js"),"w").write("\n".join(out)+"\n")
print("ok")
