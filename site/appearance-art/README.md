# 2026-10-12 인물·의상 개선 기록

익명 인물과 가상 진행자에만 적용한다. 실제 역사 인물의 초상·사진, 문화재 사진, 글자, 시대 판단의 단서는 원본을 보존한다. 여러 사람이 나오면 얼굴형·눈매·머리 모양과 색·표정을 각각 다르게 표현한다.

이번에는 49문항의 의상을 개선하고 지적된 6문항을 수정해 총 55문항을 변경했다. 원피스·치마·한복·메이드·고양이귀·마법소녀·아이돌·오피스웨어를 장면별로 다르게 사용했다. 익명 성인 캐릭터의 변형이며, 전체 자료와 실제 역사 인물을 새로운 그림으로 교체하지 않는다.

사용자의 추가 요청에 따라 73회 10번은 레오타드 기반 마법사 코스프레, 78회 8번은 스쿠미즈풍의 스포츠 원피스 수영복, 79회 25번은 레오타드 기반 아이돌 코스프레, 79회 36번은 비키니와 비치웨어를 사용했다. 해당 인물은 성인 외모·체형과 원래의 설명 자세를 유지한다.

## 지적된 문항

| 문항 | 수정 |
| --- | --- |
| 70-37 | 두 익명 인물을 서로 다른 얼굴·갈색 땋은 머리와 은청색 올림머리의 한복 미소녀로 변경; 말풍선·신문 자료 보존 |
| 79-45 | 익명 구술자를 차분한 미소녀 아바타로 변경하고 카메라의 미리보기 얼굴도 맞춤 |
| 77-10 | 가상 뉴스 진행자를 통일 신라풍 한복의 여성 캐릭터로 변경 |
| 77-25 | 갓을 쓰고 붓글씨를 쓰는 여성 캐릭터로 변경; 상소문과 종이의 글씨 보존 |
| 78-34 | 가운데 인물 위에 남은 원래 머리 흔적 제거 및 책장 복원 |
| 78-14 | 보기 사진을 답안 버튼으로 분리하고 네 인물을 서로 다른 외모·의상으로 개선; 직지 사진 보존 |

## 재현과 보존

`../question-materials/source-map.json`의 `appearanceEdit`에 문항별 의상, 생성 레이어 파일·SHA256, 표시 좌표, 적용 마스크와 원본 글자·자료 보호 영역을 기록했다. 파일은 실제 SVG에 내장해 외부 파일 로딩 없이도 표시된다. `tools/rebuild_question_materials.py`는 원본 PDF와 저장된 인물 레이어를 사용해 같은 자료를 재추출한다. 원본 JPG, 원본 PDF 자료 WebP와 이전 인물 작업 SVG는 보존한다.

## 변경 문항

| 문항 | 의상·변경 |
| --- | --- |
| 70-5 | Only the seated lecturer: French navy A-line knee-length office dress, white Peter Pan collar, pearl buttons and modest heeled shoes; retain the lovely brown hair and seated crossed-leg speaking pose. |
| 70-13 | Teal fitted museum-guide blazer, ivory blouse, charcoal pleated knee-length skirt and a small elegant ribbon; no trousers. |
| 70-18 | Back-facing lavender-haired visitor: lime blouse, lavender calf-length pleated skirt with a delicate ribbon waist and comfortable ankle boots, small tasteful cat-ear headband; keep the headphones. |
| 70-35 | Chocolate tailored vest over ivory ruffle-collar blouse, burgundy high-waist midi skirt, tasteful dark-academia office fashion. |
| 71-20 | Back-facing silver-haired viewer in a lavender modern hanbok-inspired dress with flowing dark plum chima skirt; headphones unchanged. |
| 71-21 | Cream wrap midi dress with burgundy sash and low boots, a refined sightseeing outfit. |
| 71-27 | Rose-pink tailored blazer over ivory blouse, charcoal A-line knee-length skirt, polished feminine officewear. |
| 71-32 | Mustard-and-midnight-blue magical-girl inspired knee-length dress with tiny subtle constellation embroidery and a flowing navy skirt; remain a respectful fully clothed museum visitor. |
| 71-46 | Mustard cropped field vest, cream blouse, warm brown pleated knee-length skirt, opaque tights and practical ankle boots; confident archaeology visitor. |
| 72-21 | Dusty rose floral wrap midi dress, white cardigan and low walking shoes; natural garden fashion. |
| 72-43 | Indigo denim pinafore knee-length SKIRT over a white puff-sleeve blouse, relaxed feminine casual outfit. |
| 73-7 | Rust-colored linen midi skirt, olive cardigan, ivory blouse and practical ankle boots; gentle field-trip outfit. |
| 73-10 | Adult stage magician cosplay: orange-and-ivory leotard with a short flared navy star-pattern overskirt, little shoulder cape, cat-ear headband, black opaque tights and gloves. Keep an unmistakably adult face and neutral teaching gesture. |
| 73-39 | Lavender idol-inspired tailored jacket dress with a flared knee-length plum skirt, modest bow and feminine low heels. |
| 74-2 | Cream frilled knee-length skirt and rose blouse with a subtle ribbon belt, elegant everyday dress. |
| 74-3 | Classic navy-and-ivory maid-inspired knee-length dress, modest long-sleeved bodice, white apron, a small ribbon cat-ear headband, opaque tights; keep original gesture and museum surroundings. |
| 74-7 | Blush cardigan, lavender pleated midi skirt and white blouse, cute adult everyday fashion. |
| 74-21 | Grey checked collared blouse and navy high-waist A-line knee-length skirt; refined professional curator. |
| 75-13 | Back-facing headphone visitor in a pink short-sleeved blouse and grey petal-pleated midi skirt with a simple ribbon waist; preserve headphones and device. |
| 75-15 | Mint blouse, lilac A-line knee-length skirt and a violet waist ribbon, feminine librarian fashion. |
| 75-21 | Powder-blue short-sleeved blouse, matching tailored blue knee-length pleated skirt and a delicate navy hair ribbon. |
| 75-24 | Adult wheelchair-using guide: white sailor-collar blouse and a navy knee-length pleated skirt, carefully draped over seated knees; retain the wheelchair exactly and dignified pose. |
| 75-27 | Violet magical-girl inspired knee-length dress with pink puff-sleeve blouse, modest star ribbon and flowing lavender skirt; adult polished anime fashion. |
| 75-40 | Navy blouse, sky-blue gingham midi skirt with soft gathers and a waist ribbon, natural everyday style. |
| 75-42 | Only the standing long-dark-haired lecturer at LEFT: pink blouse and ivory pleated knee-length skirt with a black waist ribbon; leave all seated people unchanged. |
| 75-44 | Only the LEFT blonde visitor: a cream-and-mustard elegant long skirt dress with a lace collar, low shoes; leave the right blue-skirt visitor unchanged. |
| 75-46 | Lilac tailored blouse and midnight-blue pleated midi skirt, a silver ribbon brooch and professional feminine styling. |
| 75-48 | BOTH standing women: LEFT auburn-haired adult with rounder warm face in sunny ivory bow-neck knee-length dress; RIGHT dark-haired adult with sharper emerald almond eyes in sage green pleated midi dress with white collar. Clearly distinct faces and hairstyles, never twins. |
| 76-13 | Sky-blue structured knee-length office coatdress with a flowing A-line skirt, white collar and navy waist ribbon. |
| 76-16 | BOTH adult visitors: LEFT pale purple-haired woman wears sage wrap midi dress and practical boots; RIGHT auburn-haired woman wears a navy cardigan and dusty rose knee-length skirt. Preserve distinct faces, the monument and all carved text. |
| 76-20 | Rose cardigan, ivory blouse and navy polka-dot knee-length skirt, gentle cute adult casual fashion. |
| 76-37 | A plum-and-ivory librarian maid-inspired knee-length dress, lace collar and cream apron, sensible low shoes; retain presentation gesture. |
| 76-45 | Green field-trip jacket, lemon pleated knee-length skirt, white blouse and ankle boots; practical feminine visitor fashion. |
| 76-48 | Navy long structured jacket over cream blouse and slate pleated knee-length skirt, modest grey tights and low pumps; polished feminine office style. |
| 77-10 | 통일 신라풍 한복의 성인 여성 가상 뉴스 진행자 |
| 77-23 | Back-facing music-headphone visitor in a salmon pink blouse and indigo apron-style knee-length skirt with a ribbon waist; headphones and tablet retained. |
| 77-25 | 갓과 한복을 입고 붓글씨를 쓰는 성인 미소녀 |
| 77-32 | Teal office skirt suit with knee-length pleated skirt, ivory blouse, chartreuse ribbon, small subtle cat-ear headband; refined adult curator. |
| 77-39 | Cream ruffled blouse, dark burgundy suspender A-line knee-length skirt with antique brass buttons, adult steampunk librarian styling. |
| 78-1 | Tangerine-orange tailored knee-length skirt suit, ivory blouse, green silk neck scarf, elegant adult news presenter style. |
| 78-6 | Lavender tailored wrap knee-length skirt dress with a pale blouse and delicate waist bow; elegant modern curator. |
| 78-8 | Sporty navy one-piece swimsuit (Japanese sukumizu-inspired simple athletic cut, NO school badge or child styling), pale lavender hair ribbon, white open beach cover-up draped lightly at the shoulders, and matching sandals. An unmistakably adult woman age 25+ with mature adult proportions, still holding the microphone in the same neutral pose. |
| 78-10 | Navy-and-ivory cat-maid inspired knee-length dress, modest bodice, white apron, small navy cat-ear headband and pale lavender hair bow; retain pointing gesture. |
| 78-14 | 서로 다른 네 명의 성인 미소녀 박물관 관람객 |
| 78-15 | Only the standing CENTRAL adult teacher: pastel yellow blouse, sage-green knee-length pleated skirt and white ribbon belt. Keep every seated person unchanged with their own distinct faces, hair and skirts. |
| 78-19 | Navy knee-length field dress under a white-and-navy vest, brown walking boots and a camera strap, tasteful outdoor style. |
| 78-20 | Modern hanbok: powder-blue jeogori-inspired blouse and a lavender flowing knee-length chima skirt, a burgundy ribbon; retain presentation gesture. |
| 78-34 | 중앙 은발 인물과 머리 위 원래 머리 잔상 제거 |
| 78-41 | Navy tailored skirt suit with a knee-length pencil skirt, ivory blouse and a teal silk scarf; elegant officewear. |
| 78-47 | Plum-purple wrap knee-length dress with a white lace collar and small ivory sash, calm adult news-presenter fashion. |
| 79-18 | Sky-blue sailor-collar knee-length one-piece dress, white pleated skirt panels and a navy ribbon belt; adult refined casual fashion. |
| 79-25 | Adult idol magical-girl cosplay: pastel pink and black fitted leotard with a short flowing translucent star-pattern overskirt, matching wrist ribbons and a tasteful cat-ear headband. Unmistakably adult face, mature adult proportions, same standing museum-guide gesture, no sexual pose. |
| 79-36 | Stylish lilac-and-navy two-piece bikini swimsuit, an open sky-blue beach shrug and a tiny chiffon waist ribbon, matching low sandals, a star hair clip. Unmistakably adult woman age 25+, mature adult facial features and adult proportions, same neutral standing curator gesture, no sexual pose. |
| 79-45 | 차분한 구술 인터뷰의 성인 미소녀 아바타, 로즈 원피스 |

70회 30번은 김옥균 등의 역사 인물과 연결되는 장면이므로 보존한다. 70회 18번과 74회 2번의 발·치마 크롭을 넓혀 원래 바지 잔상과 잘린 발을 제거했다.

## 검증

- 500문항의 문제·선택지·정답은 유지했다. 71회 7번의 기존 해설 중 사진과 맞지 않던 탑 이름 한 곳만 수정했다.
- 1280px·390px·360px에서 전체 500문항을 확인했고, 자료 및 선택지 이미지 605개가 기록한 크기로 정상 로드된다.
- 사진 선택지 21문항 모두 사진 클릭 채점·확대·답안 저장을 확인했다. 확대는 답안을 선택하지 않으며 모의고사는 채점 전 사진 이름을 표시하지 않는다.
- 55문항의 수정 범위 밖 픽셀은 보존되며, 보호한 글자·자료 159개 영역은 원본과 일치한다. 원본 500개와 문화재 사진 105개의 해시도 검증했다.
- 새 인물 그림 70-37·77-10·77-25·79-45는 재추출 도구로 만든 결과와 브라우저 렌더링 픽셀이 일치한다.
- GitHub의 새 PC 좌우 배치를 통합하고, 좁은 답안 열에서 사진을 두 열로 배치했다. 그림의 높이가 제한될 때도 가로·세로 비율을 유지한다.


## 2026-10-12 완료분 우선 반영

총 34문항의 인물과 배경을 함께 재구성한 완료분만 반영했다. 79회 21번의 익명 등장인물을 여성으로 변경했고, 78회 4·8·9·14·34번과 79회 48번의 비율·합성 경계를 개선했다. 대사와 핵심 문화재·역사 자료는 원본 PDF 자료층으로 보존하며, 일반 자료층은 PDF를 두 배 밀도로 렌더링하고 직지는 원본 내장 이미지에서 추출했다. 실제 역사 인물의 정체성은 유지한다.

완료 문항: 70-13, 70-19, 70-36, 71-6, 71-17, 71-24, 71-25, 71-26, 72-18, 72-32, 72-44, 73-17, 73-35, 73-44, 74-10, 74-22, 75-20, 75-25, 75-48, 76-26, 76-37, 76-45, 77-24, 77-36, 78-4, 78-8, 78-9, 78-14, 78-34, 79-11, 79-21, 79-31, 79-34, 79-48.

79회 3번을 비롯한 검수 보류 7문항과 추가 생성 중인 그림은 이번 반영에서 제외했다. 문제·선택지·정답 데이터와 500문항 원본 자료는 변경하지 않았다.
