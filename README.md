# 한능검 심화 학습실

한국사능력검정시험 심화 70–79회(500문항)를 풀고 복습하는 정적 웹사이트입니다.
회차별 모의고사(80분 타이머), 시대별·조건별 연습, 오답노트, 개념 정리, 암기팁, 출제 분석, 검색을 제공합니다.
학습 기록은 브라우저(localStorage)에만 저장되며, `기록 백업` 메뉴에서 파일로 내보내고 불러올 수 있습니다.

## 실행하기

Python 3만 있으면 됩니다(추가 라이브러리 없음).

- Mac: `사이트 실행.command` 더블클릭 (또는 터미널에서 `python3 run.py`)
- Windows: `사이트 실행.bat` 실행
- 브라우저에서 `http://127.0.0.1:8791/` 이 열립니다. 종료는 실행 창에서 `Ctrl+C`.

## GitHub Pages로 게시하기

`.github/workflows/pages.yml`이 `main` 브랜치에 push될 때마다 `site/` 폴더를 GitHub Pages에 배포합니다.
처음 한 번은 저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 바꿔 주세요.

## 문제 풀이 단축키

| 키 | 동작 |
| --- | --- |
| `1`–`5` | 보기 선택 |
| `←` / `→` | 이전 / 다음 문항 |

## 폴더 구조

```
run.py                  로컬 서버 (site/ 를 8791 포트로 제공)
site/index.html         앱 전체 (문항 데이터·화면·스타일 포함)
site/textbook.js        교과서 본문 (시대별 장 서술, 현재 일제강점기 8장)
site/reference-lessons.js  39개 단원 개념노트
site/fig/               문항 자료 그림 (JPEG)
site/character-art/     캐릭터 일러스트로 다시 그린 자료 그림 (SVG)
```
