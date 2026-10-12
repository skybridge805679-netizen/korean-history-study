# PC 작업 인계 ZIP 다운로드

완료·미완성 결과물 전체 ZIP을 보관하는 다운로드 전용 브랜치입니다. 사이트 배포 코드 브랜치와 별개입니다.

원본 ZIP은 **2,192,218,758바이트(약 2.1GB)**입니다. GitHub 파일 크기 제한 때문에 **24개 조각**으로 나눴습니다. 아래 스크립트는 조각을 자동으로 다운로드해 원래 ZIP으로 합치고 SHA-256을 검증합니다. 생성한 ZIP은 일반 압축 프로그램으로 열 수 있습니다.

## Windows (Python 설치 불필요)

빈 폴더에서 PowerShell을 열고 다음 명령을 실행하세요.

```powershell
Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/skybridge805679-netizen/korean-history-study/pc-handoff-20261012/download.ps1' -OutFile download.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\download.ps1
```

## macOS / Linux / Python 사용 PC

빈 폴더에서 다음 명령을 실행하세요.

```sh
curl -L 'https://raw.githubusercontent.com/skybridge805679-netizen/korean-history-study/pc-handoff-20261012/download.py' -o download.py
python3 download.py
```

Windows에서 Python을 사용하는 경우 마지막 명령을 `python download.py`로 실행할 수 있습니다.

다운로드가 끊겨도 스크립트를 다시 실행하면 정상적으로 받은 조각은 재사용합니다. 원본 ZIP과 조각을 함께 저장하므로 다운로드·조립에 약 4.2GB 여유 공간이 필요합니다. 압축 해제를 위한 공간도 별도로 필요합니다.

## 결과와 내용

완료 파일: `korean-history-study-download/korean-history-study-all-results-20261012.zip`

- GitHub 반영 완료본 34문항의 사이트 전체 스냅샷.
- 미완성 포함 현재 작업본: 장면 재구성 99문항 중 미반영 65문항을 포함하며 최종 검수는 미완료입니다.
- 생성 PNG 전체, 검수/비교 이미지·스크린샷, 작업/검증 도구와 원본 문제지 PDF.
- PC 작업 인계 메모, 파일 해시 목록, 클라우드 절대 경로를 PC 경로로 바꾸는 도구.

ZIP 안의 `handoff-notes/PC_작업_인계.md`를 먼저 확인하세요. **미완성본을 그대로 배포하지 마세요.**

원본 ZIP SHA-256:

```
e09e1ec537644a3c5a5c4c17eb731683d9308c5ca7881e6c31e81182d3224aa4
```

GitHub Release API에 접근할 수 없어 이 브랜치에 분할 업로드했습니다. 24개 조각을 개별 ZIP 파일로 열면 안 됩니다. 이 브랜치의 GitHub 자동 저장소 ZIP 다운로드 대신 위 자동 다운로드 스크립트를 사용하세요.
