#!/usr/bin/env python3
"""site/heritage/credits.json(검수 통과분) + 아래 설명으로 site/summary/heritage.js 를 만든다."""
import json,os,re
R=os.path.join(os.path.dirname(__file__),"..","..")
C=json.load(open(os.path.join(R,"site/heritage/credits.json")))
# id: (표시 이름, 설명(인라인 표시 허용)) — 사진을 직접 열어 확인한 것만 둔다.
N={
# --- 삼국
"gwanggaeto-stele":("광개토 대왕릉비(전시 사진)","{r:장수왕} 건립(414)·{b:영락} 연호·신라 구원, 왜 격퇴"),
"chungju-stele":("충주(중원) 고구려비","{r:장수왕}의 남진·{g:국내 유일}의 고구려 비석"),
"janggunchong":("집안 장군총","{r:고구려} {b:돌무지무덤}(계단식 적석총)·국내성 일대"),
"gangseo-sasindo":("강서대묘 현무(조선고적도보 도판)","{r:고구려} {b:사신도}·{b:도교} 사상"),
"seokchon-tomb":("서울 석촌동 고분군","{r:백제} 한성 시기 {b:계단식 돌무지무덤} → 고구려 계통"),
"muryeong-tomb":("공주 무령왕릉 내부","{r:벽돌무덤}(중국 남조 영향)·송산리 고분군·1971 발굴"),
"muryeong-stone":("무령왕릉 지석","{g:무령왕}의 사망 기록·토지신에게 묘지를 산 {b:매지권}"),
"sataek-stele":("사택지적비","{r:백제} 사비 시기·{g:사택지적}이 불당을 세운 기록"),
"jeongnimsa":("부여 정림사지 오층 석탑","{r:사비} 시기·소정방 기록을 새겨 {b:평제탑}이라 불림"),
"mireuksa":("익산 미륵사지 석탑(복원)","{g:무왕}·가장 큰 석탑·목탑 양식·사리봉영기"),
"yeongnisan-incense":("백제 금동 대향로","{r:능산리} 절터 출토(1993)·{b:도교·불교} 사상"),
"chilji-do":("칠지도","{g:근초고왕}이 왜왕에게 하사(4C)·이소노카미 신궁"),
"cheomseongdae":("경주 첨성대","{g:선덕여왕}·현존 동양 최고(最古) 천문대"),
"bunhwangsa":("분황사 모전 석탑","{g:선덕여왕}·벽돌 모양으로 쌓은 {b:모전 석탑}"),
"silla-crown":("신라 금관(황남대총 출토)","{r:신라} 금관·{b:출(出)자형} 장식"),
"cheonmachong-mural":("천마총 천마도","{r:신라} {b:천마총}·말다래(장니)에 그린 천마도"),
"jinheung-stele":("북한산 진흥왕 순수비(국립중앙박물관)","{g:진흥왕}·한강 유역 확보·{b:순수비} 4곳(북한산·창녕·황초령·마운령)"),
"gaya-pottery":("기마 인물형 토기(국보 91호)","{r:신라} 토기 — 가야 토기와 구별"),
# --- 남북국·고려
"seokguram":("석굴암 본존불(롯데월드 민속박물관 모형)","{r:통일 신라} {g:김대성}이 창건(경덕왕) — 사진은 모형"),
"bulguksa-seokgatap":("불국사 삼층 석탑(석가탑)","{r:통일 신라} {b:무구정광대다라니경} 출토(현존 최고 목판 인쇄물)"),
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
"bongjeongsa":("안동 봉정사 극락전","{r:고려} 목조 건축·현존 가장 오래된 목조 건축물로 꼽힘"),
"sudeoksa":("예산 수덕사 대웅전","{r:고려} 목조 건축·{b:주심포}·1308년 건립 기록"),
"woljeongsa-9":("평창 월정사 팔각 구층 석탑","{r:고려} {b:다각 다층탑}·송 영향"),
"gyeongcheonsa":("개성 경천사지 십층 석탑","{r:고려 말} 원 영향(1348)·조선 원각사지 십층 석탑에 영향"),
"manwoldae":("개성 만월대","{r:고려} 개경의 궁궐터"),
"tripitaka":("팔만대장경 경판","{g:고종} 때 {r:몽골 침입 극복} 기원·합천 해인사 보관"),
"haeinsa-janggyeong":("합천 해인사 장경판전(외부)","{b:팔만대장경} 보관·통풍·습도 조절 건축 {n:(건물은 조선 초기)}"),
"jikji":("직지심체요절","{r:1377} {b:흥덕사}(청주) 금속 활자·현존 최고(最古) 금속 활자본"),
# --- 조선 전기
"gyeongbokgung-geunjeongjeon":("경복궁 근정전","{r:조선} 정전·태조 창건(1395)·{g:흥선 대원군} 중건(1867)"),
"jongmyo":("종묘 정전","{r:조선} 역대 왕과 왕비의 신주를 모신 사당·유네스코 세계 유산(1995)"),
"hunminjeongeum":("훈민정음 해례본","{g:세종} 1446·{b:국보 70호}·유네스코 기록 유산"),
"cheugugi":("측우기(측우대)","{g:세종} 때 강우량 측정·{b:측우기} {n:(복제)}"),
"angbuilgu":("앙부일구","{g:세종} 때 {b:오목 해시계}·{n:(복제)}"),
"jagyeongnu":("자격루(보루각, 복원 모형)","{g:세종} 때 {g:장영실}·자동 물시계(1434)"),
"cheonsang-yeolcha":("천상열차분야지도","{g:태조} 때 제작·돌에 새긴 {b:별자리 지도}"),
"honil-gangni":("혼일강리역대국도지도","{g:태종} 때 제작(1402)·{b:세계 지도}"),
"mongyu-dowondo":("몽유도원도","{g:안견}·{g:안평대군}의 꿈 이야기(1447)·15C 산수화"),
"wongaksa-pagoda":("원각사지 십층 석탑","{g:세조} 때(1467)·고려 경천사지 탑 영향·서울 탑골 공원"),
"buncheong":("분청사기 장군","{r:조선 전기} {b:분청사기}(15~16C)"),
# --- 조선 후기
"baekja-moon-jar":("백자 달항아리(대영 박물관)","{r:조선 후기} {b:백자 달항아리}(18C)"),
"suwon-hwaseong":("수원 화성 장안문(옛 사진)","{g:정조}·{g:정약용}·{b:수원 화성}(1796)"),
"geojunggi":("거중기(복원)","{g:정약용} 고안·{b:수원 화성} 축조 {n:(화성성역의궤)}"),
"inwang-jesaekdo":("인왕제색도","{g:정선}·{b:진경산수화}·비 갠 뒤 인왕산"),
"ssireum":("씨름(단원 풍속도첩)","{g:김홍도}·{b:풍속화}"),
"wolha-jeongin":("월하정인(혜원전신첩)","{g:신윤복}·{b:풍속화}·달밤의 남녀"),
"sehando":("세한도(부분)","{g:김정희}·제주도 유배 중 그린 {b:문인화}"),
"daedong-yeojido":("대동여지도","{g:김정호}·1861·{b:분첩 절첩식} 지도"),
"palsangjeon":("보은 법주사 팔상전","{r:조선 후기} 현존하는 유일한 5층 목탑"),
"geumsansa-mireukjeon":("김제 금산사 미륵전","{r:조선 후기} 3층 불전·{b:국보 62호}"),
"hwaeomsa-gakhwangjeon":("구례 화엄사 각황전과 석등","{r:조선 후기} 숙종 때(1702) 중건한 {b:각황전}"),
"hahoe-mask":("병산탈(하회탈과 함께 국보 121호)","{r:조선 후기} {b:하회 별신굿 탈놀이}"),
# --- 근대·일제강점기
"independence-gate":("독립문(1955년 사진)","{g:서재필}·{b:독립 협회}가 세움(1897)·영은문 자리 근처"),
"deoksugung-seokjojeon":("덕수궁 석조전","{r:대한 제국} 서양식 건물(1910 완공)"),
"jungmyeongjeon":("덕수궁 중명전","{r:대한 제국} {b:을사늑약}(1905) 체결 장소"),
"myeongdong-cathedral":("명동 성당","{b:고딕 양식} 벽돌 성당·1898 완공"),
"cheokhwabi":("척화비(청주)","{g:흥선 대원군}·신미양요(1871) 후 전국에 건립"),
"gwangseongbo":("강화 광성보 안해루","{g:신미양요}(1871) 격전지·강화도"),
"seodaemun-prison":("서대문 형무소 역사관","{r:일제 강점기} 독립운동가를 수감한 곳"),
"tapgol-park":("탑골 공원 팔각정","{r:3·1 운동} 때 독립 선언서 낭독 장소"),
"bongo-dong":("상하이 대한민국 임시 정부 수립지","{r:대한민국 임시 정부}(1919, 상하이)"),
}
GROUPS=[
("heritage-1","삼국","삼국 시대 문화재 사진","삼국",["gwanggaeto-stele","chungju-stele","janggunchong","gangseo-sasindo","seokchon-tomb","muryeong-tomb","muryeong-stone","sataek-stele","jeongnimsa","mireuksa","yeongnisan-incense","chilji-do","cheomseongdae","bunhwangsa","silla-crown","cheonmachong-mural","jinheung-stele","gaya-pottery"]),
("heritage-2","남북국","남북국·고려 문화재 사진","남북국",["seokguram","bulguksa-seokgatap","bulguksa-dabotap","emille-bell","gamunsa","hwaeomsa-lion","anapji","mireuk-gwanchoksa","hasachang-buddha","suwol-gwaneum","cheongja-sanggam","cheongja-gourd","buseoksa-muryangsujeon","bongjeongsa","sudeoksa","woljeongsa-9","gyeongcheonsa","manwoldae","tripitaka","haeinsa-janggyeong","jikji"]),
("heritage-3","조선전기","조선 전기 문화재 사진","조선전기",["gyeongbokgung-geunjeongjeon","jongmyo","hunminjeongeum","cheugugi","angbuilgu","jagyeongnu","cheonsang-yeolcha","honil-gangni","mongyu-dowondo","wongaksa-pagoda","buncheong"]),
("heritage-4","조선후기","조선 후기 문화재 사진","조선후기",["baekja-moon-jar","suwon-hwaseong","geojunggi","inwang-jesaekdo","ssireum","wolha-jeongin","sehando","daedong-yeojido","palsangjeon","geumsansa-mireukjeon","hwaeomsa-gakhwangjeon","hahoe-mask"]),
("heritage-5","근대","근대·일제강점기 유적 사진","근대",["independence-gate","deoksugung-seokjojeon","jungmyeongjeon","myeongdong-cathedral","cheokhwabi","gwangseongbo","seodaemun-prison","tapgol-park","bongo-dong"]),
]
def credit(c):
    a=re.sub(r"(Unknown author)+","",c["author"]).strip() or "작자 미상"
    a=re.sub(r"\s*\(talk\).*","",a).split("\n")[0][:30]
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
