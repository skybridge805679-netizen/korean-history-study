# 한능검 심화 학습실

한국사능력검정시험 심화 70–79회(500문항)를 풀고 복습하는 정적 웹사이트입니다.
회차별 모의고사(80분 타이머), 시대별·조건별 연습, 오답노트, 개념 정리, 암기팁, 출제 분석, 검색을 제공합니다.
학습 기록은 브라우저(localStorage)에만 저장되며, `기록 백업` 메뉴에서 파일로 내보내고 불러올 수 있습니다.

## 실행하기

설치할 것이 없습니다. 아래 중 편한 방법을 쓰세요.

- **온라인:** GitHub Pages 주소로 접속합니다.
- **오프라인:** 저장소를 내려받아 맨 위의 `index.html`(또는 `site/index.html`)을 브라우저로 엽니다.

학습 기록은 브라우저의 주소별로 따로 저장됩니다. 온라인 사이트와 내려받은 파일 사이에 기록을 옮기려면 `기록 백업` 메뉴에서 내보내고 불러오세요.

## GitHub Pages로 게시하기

두 가지 방법 중 하나를 고르세요.

- **브랜치에서 바로 게시 (간단):** Settings → Pages → Source를 **Deploy from a branch**, 폴더를 **/ (root)** 로 둡니다.
  루트의 `index.html`이 `site/`로 자동 이동시키므로 주소는 `https://<아이디>.github.io/<저장소>/` 그대로 쓰면 됩니다.
- **GitHub Actions로 게시:** Source를 **GitHub Actions**로 바꾸면 `.github/workflows/pages.yml`이 `main`에 push될 때마다 `site/` 폴더만 배포합니다.

## 문제 풀이 단축키

| 키 | 동작 |
| --- | --- |
| `1`–`5` | 보기 선택 |
| `←` / `→` | 이전 / 다음 문항 |

## 폴더 구조

```
index.html              site/index.html로 이동
site/index.html         앱 전체 (문항 데이터·화면·스타일 포함)
site/core-notes/*.js    핵심노트 97개(해설 아래 비교표·연결 키워드) — 500문항 전부 연결
site/textbook.js        교과서 본문 (시대별 장 서술, 현재 일제강점기 8장)
site/reference-lessons.js  39개 단원 개념노트
site/question-explanations.js  500문항의 단서·정답 근거·보기별 해설
site/fig/               문항 자료 그림 (JPEG)
site/character-art/     캐릭터 일러스트로 다시 그린 자료 그림 (SVG)
```

문항별 해설의 작성 기준과 검증 방법은 [해설 보완 기록](docs/question-explanations.md)에 정리되어 있습니다.

## 생성 원화 보관함

`archive/`에는 GPT가 만든 장면 원화 243장 전부(인계 ZIP `pc-handoff-20261012`의 `generated_images/`)를 WebP로 옮겨 두었습니다.
사이트 주소 뒤에 `/archive/`를 붙여 열면 문항별로 후보를 비교하고, 사이트에 쓸 그림을 골라 목록으로 복사할 수 있습니다.
`archive/index.json`에 문항별 후보와 원본 PNG의 SHA-256을 기록했습니다.

## 핵심노트 관리

`site/core-notes/`의 노트는 `match`("시대/주제" 또는 문항 키)로 문항과 연결됩니다.
노트를 고치거나 추가한 뒤에는 `node tools/check_core_notes.js`로 500문항이 모두 연결되는지, 표 열 수가 맞는지 확인하세요.
