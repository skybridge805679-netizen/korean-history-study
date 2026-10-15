# 문화재 사진 수집 현황

기출 사진만으로는 문화재 사진이 부족해 Wikimedia Commons(자유 이용) 사진으로 보강하는 작업의 현황이다. 이어서 할 때는 아래 '남은 것'을 처리한다.

## 작업 방법

1. `python3 tools/heritage/fetch.py [--only id,id]` — `tools/heritage/targets.json` 의 항목을 Commons 에서 검색해 `site/heritage/<id>.jpg` 와 `credits.json`(저작자·라이선스·원본 주소)을 만든다. Commons 가 요청을 자주 429 로 거절하므로 간격을 두고 여러 번 돌린다(이미 받은 것은 건너뜀). 직접 Commons 에서 골라 같은 형식으로 넣어도 된다.
2. **받은 사진을 반드시 열어 보고** 이름과 맞는지 확인한다. 자동 검색 결과는 엉뚱한 사진(다른 유물·내부 사진·옛 신문 스캔 등)이 걸릴 수 있다. 틀리면 `targets.json` 의 `q` 를 고치거나 파일 제목을 직접 지정해 다시 받는다. 탈락 사유는 `tools/heritage/status.py` 의 `REJ` 에 적는다.
3. 확인된 사진은 `tools/heritage/build_sheets.py` 의 `N`(이름·설명)과 `GROUPS`에 추가하고 `python3 tools/heritage/build_sheets.py` 로 `site/summary/heritage.js` 를 다시 만든다. 설명은 확실한 사실만 쓴다.
4. `node tools/check_summary.js` 통과, `python3 tools/heritage/status.py` 로 이 문서 갱신 후 커밋한다.

## 반영됨 (77점) — 사진 확인 완료, 요약노트 ‘문화재 사진’에 표시

| id | 이름 | 시대 | 라이선스 |
|---|---|---|---|
| gungseong-bandaji | 금동 연가7년명 여래 입상 | 삼국 | KOGL Type 1 |
| janggunchong | 집안 장군총 | 삼국 | CC BY-SA 4.0 |
| gwanggaeto-stele | 광개토 대왕릉비 | 삼국 | CC BY-SA 4.0 |
| chungju-stele | 충주 고구려비 | 삼국 | CC BY-SA 3.0 |
| gangseo-sasindo | 강서대묘 현무도(사신도) | 삼국 | Public domain |
| muryeong-tomb | 공주 무령왕릉 | 삼국 | CC0 |
| muryeong-stone | 무령왕릉 지석 | 삼국 | CC BY 4.0 |
| seokchon-tomb | 서울 석촌동 고분군 | 삼국 | CC0 |
| sataek-stele | 사택지적비 | 삼국 | Public domain |
| seosan-buddha | 서산 마애여래삼존상 | 삼국 | CC BY-SA 4.0 |
| jeongnimsa | 부여 정림사지 오층 석탑 | 삼국 | CC0 |
| mireuksa | 익산 미륵사지 석탑 | 삼국 | CC BY-SA 4.0 |
| yeongnisan-incense | 백제 금동 대향로 | 삼국 | CC BY-SA 4.0 |
| chilji-do | 칠지도 | 삼국 | CC0 |
| cheonmachong-mural | 천마총 천마도 | 삼국 | Public domain |
| silla-crown | 신라 금관 | 삼국 | CC BY-SA 2.0 |
| cheomseongdae | 경주 첨성대 | 삼국 | CC BY-SA 4.0 |
| bunhwangsa | 분황사 모전 석탑 | 삼국 | CC BY-SA 3.0 |
| imsin-stone | 임신서기석 | 삼국 | KOGL Type 1 |
| jinheung-stele | 북한산 신라 진흥왕 순수비 | 삼국 | CC BY-SA 4.0 |
| gaya-pottery | 가야 토기(수레바퀴 장식 뿔잔 등) | 삼국 | CC BY-SA 3.0 |
| seokguram | 경주 석굴암 본존불 | 남북국 | CC BY-SA 4.0 |
| bulguksa-seokgatap | 불국사 삼층 석탑(석가탑) | 남북국 | CC0 |
| bulguksa-dabotap | 불국사 다보탑 | 남북국 | CC0 |
| emille-bell | 성덕대왕 신종 | 남북국 | CC BY-SA 4.0 |
| gamunsa | 감은사지 동·서 삼층 석탑 | 남북국 | CC BY-SA 2.0 |
| hwaeomsa-lion | 구례 화엄사 사사자 삼층 석탑 | 남북국 | CC BY 2.0 |
| anapji | 경주 안압지(동궁과 월지) | 남북국 | CC BY-SA 2.0 |
| mireuk-gwanchoksa | 논산 관촉사 석조 미륵보살 입상 | 고려 | CC BY-SA 4.0 |
| buseoksa-muryangsujeon | 영주 부석사 무량수전 | 고려 | CC BY-SA 2.0 kr |
| bongjeongsa | 안동 봉정사 극락전 | 고려 | CC BY-SA 3.0 |
| sudeoksa | 예산 수덕사 대웅전 | 고려 | CC BY-SA 4.0 |
| haeinsa-janggyeong | 합천 해인사 장경판전 | 고려 | CC BY-SA 4.0 |
| tripitaka | 팔만대장경판 | 고려 | CC BY-SA 3.0 |
| jikji | 직지심체요절 | 고려 | Public domain |
| woljeongsa-9 | 평창 월정사 팔각 구층 석탑 | 고려 | CC BY-SA 2.0 |
| gyeongcheonsa | 경천사지 십층 석탑 | 고려 | CC BY-SA 4.0 |
| cheongja-sanggam | 청자 상감 운학문 매병 | 고려 | CC0 |
| cheongja-gourd | 청자 참외 모양 병 | 고려 | CC0 |
| suwol-gwaneum | 수월관음도 | 고려 | Public domain |
| hasachang-buddha | 하남 하사창동 철조 석가여래 좌상 | 고려 | Public domain |
| manwoldae | 개성 만월대 | 고려 | CC BY-SA 4.0 |
| gyeongbokgung-geunjeongjeon | 경복궁 근정전 | 조선전기 | CC BY-SA 4.0 |
| jongmyo | 종묘 정전 | 조선전기 | CC BY 2.0 |
| hunminjeongeum | 훈민정음 해례본 | 조선전기 | Public domain |
| cheugugi | 측우기 | 조선전기 | CC BY-SA 3.0 |
| angbuilgu | 앙부일구 | 조선전기 | CC BY-SA 2.0 |
| jagyeongnu | 자격루 | 조선전기 | CC BY-SA 4.0 |
| honil-gangni | 혼일강리역대국도지도 | 조선전기 | Public domain |
| cheonsang-yeolcha | 천상열차분야지도 | 조선전기 | Public domain |
| mongyu-dowondo | 몽유도원도 | 조선전기 | Public domain |
| wongaksa-pagoda | 원각사지 십층 석탑 | 조선전기 | CC BY-SA 4.0 |
| buncheong | 분청사기 | 조선전기 | CC BY-SA 4.0 |
| baekja-moon-jar | 백자 달항아리 | 조선후기 | CC BY-SA 4.0 |
| suwon-hwaseong | 수원 화성(팔달문·화서문·장안문) | 조선후기 | Public domain |
| geojunggi | 거중기 | 조선후기 | CC BY-SA 3.0 |
| uigwe | 조선왕조의궤 | 조선후기 | KOGL Type 1 |
| geumgang-jeondo | 금강전도(정선) | 조선후기 | Public domain |
| inwang-jesaekdo | 인왕제색도(정선) | 조선후기 | Public domain |
| ssireum | 씨름(김홍도) | 조선후기 | Public domain |
| wolha-jeongin | 월하정인(신윤복) | 조선후기 | Public domain |
| sehando | 세한도(김정희) | 조선후기 | Public domain |
| daedong-yeojido | 대동여지도 | 조선후기 | Public domain |
| palsangjeon | 법주사 팔상전 | 조선후기 | CC BY-SA 4.0 |
| geumsansa-mireukjeon | 김제 금산사 미륵전 | 조선후기 | CC BY-SA 4.0 |
| hwaeomsa-gakhwangjeon | 구례 화엄사 각황전 | 조선후기 | CC BY 2.0 |
| hahoe-mask | 탈춤(하회별신굿탈) | 조선후기 | CC0 |
| independence-gate | 독립문 | 근대 | CC BY-SA 4.0 |
| deoksugung-seokjojeon | 덕수궁 석조전 | 근대 | CC BY-SA 3.0 |
| jungmyeongjeon | 덕수궁 중명전 | 근대 | CC BY-SA 4.0 |
| myeongdong-cathedral | 명동 성당 | 근대 | CC BY-SA 4.0 |
| cheokhwabi | 척화비 | 근대 | CC0 |
| gwangseongbo | 강화 초지진·광성보 | 근대 | CC BY-SA 4.0 |
| seodaemun-prison | 서대문 형무소 | 일제강점기 | CC BY-SA 4.0 |
| declaration-of-independence | 3·1 독립 선언서 | 일제강점기 | CC BY-SA 4.0 |
| tapgol-park | 탑골 공원 | 일제강점기 | CC BY-SA 4.0 |
| bongo-dong | 대한민국 임시 정부 청사(상하이) | 일제강점기 | CC BY-SA 3.0 |

## 검수 탈락 (3점) — 다시 찾아야 함

| id | 이름 | 사유 |
|---|---|---|
| gaya-iron-ingot | 가야 덩이쇠 | 덩이쇠가 아니라 철제 갑옷 부품 사진이 걸려 탈락(덩이쇠 사진을 다시 찾아야 함) |
| cheolgam-seonsa-pagoda | 쌍봉사 철감선사탑(승탑) | 쌍봉사 담장과 정자 사진이라 철감선사탑(승탑)이 아니어서 탈락 |
| gosagwansudo | 고사관수도 | 받은 사진이 강희안의 다른 산수화라 고사관수도로 확인되지 않아 탈락 |

## 남은 것 (7점) — 아직 받지 못함

429(요청 제한)로 실패했거나 검색에서 자유 라이선스 사진이 잡히지 않은 항목이다. 검색어(`q`)를 바꾸거나 Commons 에서 직접 찾는다.

| id | 이름 | 시대 | 검색어(q) |
|---|---|---|---|
| changnyeong-stele | 창녕 신라 진흥왕 척경비 | 삼국 | 창녕 신라 진흥왕 척경비 |
| balhae-buddha | 발해 이불병좌상 | 남북국 | 이불병좌상 |
| balhae-lion | 발해 석등(상경 용천부) | 남북국 | 발해 석등 |
| jeonghyo-tomb | 정혜공주묘 / 정효공주묘 | 남북국 | 정효공주묘 |
| najeon-box | 나전 칠기 | 고려 | 나전 칠기 고려 |
| seonjukgyo | 개성 선죽교 | 고려 | 선죽교 |
| cheonghwa-baekja | 청화백자 | 조선후기 | 청화백자 조선 |
