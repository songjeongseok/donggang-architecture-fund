# 최신 변경: 계좌 안내 및 기부자 접수 준비

새마을금고 **9002205750266 / 동강대학교 건축과** 계좌번호 복사를 추가했습니다.

이름·연락처 저장, 비공개 관리자 명단, 감사 팝업은 별도 서버 앱에 구현되어 있습니다. 현재 소유자 전용 시험 단계이며 공개 연결 전 개인정보 운영 정보를 확정해야 합니다. 자세한 내용은 [DONOR_INTAKE.md](DONOR_INTAKE.md)를 보세요.

---

# 동강대학교 건축학과 발전기금

**대상 저장소: `songjeongseok/donggang-architecture-fund` · 기본 브랜치: `main`**

**공개 주소: https://songjeongseok.github.io/donggang-architecture-fund/**

2026-10-24 GitHub Pages 배포를 완료했습니다. 빌드·공개 배포 성공과 실제 페이지의 메뉴·FAQ·HTTPS를 확인했습니다. 상세 결과와 미검증 항목은 [PUBLICATION_REPORT.md](PUBLICATION_REPORT.md)를 확인하세요.

호스팅은 GitHub Pages, 빌드와 배포는 GitHub Actions를 사용합니다.

현재 배포 대상은 **금액 선택이 가능한 개설 준비 안내용 정적 홈페이지**입니다. 1천원·5천원·1만원·3만원·5만원·10만원·20만원·50만원·100만원 선택과 금액 복사를 지원합니다. 받는 은행은 새마을금고이며 계좌번호와 예금주가 없어 실제 이체는 비활성 상태입니다. 로그인, 관리자 화면, 결제, 신청 저장, 실입금 집계는 구현되어 있지 않습니다. 계좌번호만 넣어서 이런 기능이 활성화되지는 않습니다.

## 실행

```sh
python3 scripts/build.py
```

Python 3.9 이상, 외부 패키지 없이 실행합니다. Windows에서는 `py -3 scripts/build.py`를 사용할 수 있습니다.

- 원본: `site/index.html`, `site/donation.js`
- 공개 산출물: `dist/index.html`, `dist/.nojekyll`, `dist/donation.js`
- 빌드 결과: `.build/report.json` (공개 산출물에 포함하지 않음)
- 설치 명령: 없음
- Node.js/npm: 필요 없음
- 운영 서버 시작 명령: 없음
- 환경 변수·비밀키: 없음
- 배포 흐름: `.github/workflows/pages.yml`
- 자세한 단계, 설정 위치, 미확인 항목과 검증 방법: `DEPLOYMENT.md`

`dist/`는 생성 폴더이므로 수정하지 말고 `site/index.html`을 수정한 뒤 다시 빌드합니다. 배포 스크립트는 `dist/`를 다시 생성합니다. 임시 파일이나 사용자 자료를 넣지 마세요.

로컬 브라우저 확인이 필요할 때:

```sh
python3 -m http.server 8080 --bind 127.0.0.1 --directory dist
```

브라우저에서 `http://127.0.0.1:8080/`를 엽니다. 이 명령은 로컬 확인용이며 운영 서버가 아닙니다. 프로젝트 루트를 HTTP 공개 디렉터리로 사용하지 마세요.

## 수동 배포만 가능

워크플로는 `workflow_dispatch` 하나만 사용합니다. push, PR, 태그, 예약 실행에 따른 자동 배포는 없습니다. `Run workflow`에서도 `publish`를 체크하지 않으면 빌드와 후보 산출물 업로드까지만 실행하고 배포 작업은 건너뜁니다.

최종 공개가 승인된 시점에만 기본 브랜치에서 `publish`를 체크해 실행합니다. 이 선택은 인터넷 공개 배포를 시작합니다. 저장소 공개 범위와 Pages 방문자 접근 범위는 동일한 설정이 아닙니다.

이번 준비본에는 기존 Sites 프로젝트 식별자, 원격 주소, 인증 정보가 포함되지 않습니다. 기존 Sites 검토용 배포는 수정하지 않았습니다.
