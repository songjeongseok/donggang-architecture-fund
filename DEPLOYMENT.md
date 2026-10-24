# 배포 준비 및 운영 인계

검토 기준일: 2026-10-24 (한국 시간)

> 이 문서는 배포 전 준비 당시의 검증 범위와 절차를 보존한 기록입니다. 이후 사용자가 배포 진행을 요청하여 전용 저장소 `songjeongseok/donggang-architecture-fund`를 생성했습니다. 아래의 “이번에는 실행하지 않음”, “미정”, “미검증”은 최초 준비 시점의 상태입니다. 실제 실행 후 상태와 공개 주소는 `PUBLICATION_REPORT.md`에 기록합니다.

## 1. 대상과 결론

- 앱: 동강대학교 건축학과 발전기금 개설 준비 안내 페이지.
- 기술: HTML5, 내부 CSS, 내부 SVG, HTML details/summary. JavaScript 없음.
- 준비 플랫폼: GitHub.com의 GitHub Pages + GitHub-hosted Actions runner.
- 정확한 대상 저장소: **미정 / 플랫폼 측 확인 필요**. 특정 저장소로 원격 쓰기를 하지 않았다.
- 현재 완료 범위: 코드와 배포 설정을 로컬에서 준비하고 검사. 실제 GitHub Actions 실행은 미검증.
- 기존 Sites에 있던 비공개 검토용 배포는 변경하지 않았다. 이번 준비가 새 배포를 의미하지 않는다.

연결된 `songjeongseok/duda` 저장소는 조회 당시 공개, 기본 브랜치 `main`, 크기 0이며 현재 계정의 관리 권한이 확인되었다. 이름만으로 이번 프로젝트의 대상이라고 확정하지 않았다. 이 저장소의 Pages/Actions/Environment/DNS 상태는 조회된 저장소 메타데이터로 확인할 수 없다.

## 2. 빌드·설정·서버 요구 사항

| 항목 | 값 / 위치 |
|---|---|
| 설치 명령 | 없음 |
| 빌드 명령 | `python3 scripts/build.py` |
| Windows 대체 | `py -3 scripts/build.py` |
| 원본 HTML | `site/index.html` |
| 배포 출력 디렉터리 | `dist` |
| 배포 진입 파일 | `dist/index.html` |
| 빌드 환경 | Python 3.9 이상, 표준 라이브러리만 사용 |
| Actions runner | `ubuntu-latest`, 제공되는 `python3` 사용 |
| 운영 환경 | 정적 HTTPS 호스팅; 앱 서버·포트·컨테이너·DB 필요 없음 |
| 세션·쿠키·저장소 | 앱에서 생성하지 않음. 호스팅 측 접속기록은 별도 |
| 앱 환경 변수 | 없음 |
| SPA rewrite | 불필요. 내부 이동은 `#purpose`, `#faq` 등 해시 링크 |
| 사용자 지정 404 | 없음. 미존재 경로는 플랫폼 기본 404 |
| 도메인 | 우선 GitHub Pages 기본 도메인. 사용자 도메인은 미정 |
| GitHub 설정 파일 | `.github/workflows/pages.yml` |
| 출력 검사 보고서 | `.build/report.json` |

`.env.example`은 현재 읽지 않는 설명용 파일이다. 그 안의 `<...>`는 미래 서버 개발을 위한 자리표시자이며 설정하지 않아도 현 사이트가 빌드된다. 정적 HTML에 환경 변수를 넣으면 공개 정보가 되므로 비밀키를 넣어서는 안 된다.

워크플로는 GitHub가 자동 발급하는 임시 `GITHUB_TOKEN`과 배포 OIDC를 사용한다. 수동 PAT, 계정 비밀번호, 카드 결제 키를 추가할 필요가 없다. 향후 서버 비밀값은 서버 호스팅의 secret 저장소에 두며 GitHub 저장소나 `dist/`에 넣지 않는다.

## 3. 프로젝트 쪽에서 정리한 사항

| 발견 사항 | 준비본의 처리 |
|---|---|
| 기존 단독 HTML에는 GitHub용 빌드·배포 설정이 없음 | `scripts/build.py`, 수동 Actions 워크플로 추가 |
| Sites의 `.openai/hosting.json`은 GitHub Pages 설정이 아님 | 새 배포 패키지에 포함하지 않음; 기존 사이트 식별자 재사용 방지 |
| 원본·설명서·비밀파일이 함께 공개될 가능성 | 공개 대상 `index.html`, `.nojekyll`만 허용하고 `dist`에 복사 |
| 저장만 해도 배포되는 것을 방지할 필요 | push/PR/schedule 트리거 없음; 수동 `publish`의 기본값 false |
| 서브경로(`/저장소명/`)에서 링크가 깨질 수 있음 | 현재 모든 12개 링크가 같은 문서의 해시 링크인지 검증 |
| 실제 접수 기능으로 오인할 가능성 | 미접수 안내 확인, 폼·스크립트·자동 이동을 빌드에서 거부 |
| 이전 첨부본의 `claude.use('db')` 의존성 | 현 홈페이지에는 없음. 빌드 검사에서 재도입 감지 |

검사기는 이 정적 안내 버전에 맞춘 제한이다. 새로운 링크·이미지 파일·신청·분석 스크립트를 추가하려면 기능 요구와 개인정보 처리를 검토한 뒤 검사 규칙도 함께 수정해야 한다. 비밀값 탐지는 일부 형식만 검사하며 전문 비밀 탐지·보안감사를 대체하지 않는다.

## 4. 플랫폼 측 확인 필요 — 이번에는 변경하지 않은 항목

| 항목 | 설정 위치 | 확인 내용 |
|---|---|---|
| 실제 배포 저장소 | 소유자/저장소 선택 | 전용 저장소 또는 사용 승인된 기존 저장소 확정. 다른 프로젝트 덮어쓰기 금지 |
| 기존 자동 게시 | Settings → Pages 및 Actions 목록 | 파일을 올리기 전에 기존 branch 기반 Pages나 다른 자동 deploy workflow가 없는지 확인 |
| Pages 사용 가능 여부 | 저장소 요금제·조직 정책 | 공개 저장소 기준 지원 확인. 비공개 저장소는 요금제 조건 확인 |
| Pages 게시 방식 | Settings → Pages → Build and deployment → Source | 배포 준비가 승인된 시점에 `GitHub Actions` 선택; `Deploy from a branch` 방식 사용 안 함 |
| Actions 허용 정책 | Settings → Actions → General | `actions/checkout@v6`, `configure-pages@v5`, `upload-pages-artifact@v4`, `deploy-pages@v4` 허용 여부 |
| 배포 환경 | Settings → Environments → github-pages | 기본 브랜치만 허용. 가능한 경우 검토자 승인 규칙 설정 |
| 권한 | 워크플로의 permissions 및 조직 정책 | build는 contents:read, deploy는 contents:read/pages:write/id-token:write 필요 |
| 기본 브랜치 | 저장소 기본 브랜치 설정 | 워크플로 파일이 기본 브랜치에 있어야 수동 실행 가능; publish도 기본 브랜치만 허용 |
| HTTPS | Settings → Pages → Enforce HTTPS | 공개 후 HTTPS 및 HTTP 리다이렉트 확인 |
| 사용자 도메인 | Pages → Custom domain, 학교 DNS 관리 화면 | 도메인 사용 승인과 DNS 소유권·인증서 확인. 이번 패키지에는 CNAME 없음 |
| 공개 범위 | Pages 게시 범위 확인 | 일반 Pages 배포는 공개 웹사이트로 간주. 소스 저장소 비공개가 방문자 로그인 제한을 보장하지 않음 |

환경 보호 규칙, 허용 action 정책, 인증서와 DNS 상태는 실제 계정/도메인에서 확인해야 한다. 접근 가능한 도구에는 이 설정의 조회 기능이 없어 검증 완료로 표시하지 않았다.

## 5. 정확한 진행 순서

### 지금 가능한 로컬 준비

1. ZIP을 풀고 `donggang-fund-github-pages` 디렉터리로 이동한다.
2. `python3 scripts/build.py`를 실행한다. 종료 코드 0과 `.build/report.json`의 passed를 확인한다.
3. `dist`를 로컬로 열어 콘텐츠를 확인한다. 파일 직접 열기도 가능하며 README의 로컬 HTTP 명령을 사용할 수도 있다.
4. 배포 대상 저장소와 기존 자동 게시 여부를 먼저 확인한다. 이번 작업에서는 push/업로드/설정 변경/원격 실행을 하지 않았다.

### 나중에 GitHub에서 검증만 할 때

1. 대상 저장소를 확정한다. 기존 저장소라면 위 표의 자동 게시 설정부터 확인한다.
2. 기본 브랜치에 이 패키지의 소스 내용을 올린다. `.github` 디렉터리가 누락되지 않도록 한다. ZIP 파일 자체를 올리는 방식은 사용하지 않는다. `dist`, `.build`, `.env`, `.openai`는 올리지 않는다.
3. 등록할 소스는 `.github/workflows/pages.yml`, `.gitignore`, `.env.example`, `README.md`, `DEPLOYMENT.md`, `site/`, `scripts/`이다.
4. Actions → **Validate and optionally publish Pages** → **Run workflow**로 이동한다.
5. 기본 브랜치를 선택하고 **publish를 체크하지 않은 상태**로 실행한다.
6. build 성공, deploy가 skipped인 것을 확인한다. 이 경로는 Pages 설정을 조회/활성화하거나 인터넷 공개 배포를 하지 않는다. 후보 artifact 업로드만 이루어진다.

### 공개 배포를 승인한 뒤에만 할 단계 — 이번에는 실행하지 않음

1. 대학의 사전 안내 게시 승인, 사이트 표시 문구, 공개 범위를 최종 확인한다. 실제 모금 시작에 필요한 승인과 절차는 이 안내 페이지 배포와 별개이다.
2. Settings → Pages → Source를 **GitHub Actions**로 설정한다. 조직의 Pages·Actions 허용 정책을 확인한다.
3. Settings → Environments → `github-pages`에서 허용 브랜치를 기본 브랜치로 제한한다. 검토 규칙이 있다면 승인 담당자를 정한다.
4. Actions → **Validate and optionally publish Pages** → **Run workflow**에서 기본 브랜치를 선택하고 **publish를 체크**한다. 이 실행은 실제 공개 배포이다.
5. 필요 시 환경 승인 단계를 완료한다. build와 deploy가 모두 성공했는지 확인한다.
6. 실행 결과의 `page_url` 또는 Settings → Pages에 표시된 URL을 사용한다. 예상 형식은 `https://<OWNER>.github.io/<REPOSITORY>/`이나, 실제 주소는 플랫폼 결과로 확인한다.
7. Settings → Pages의 HTTPS와 아래 점검 항목을 확인한다.

대상 저장소가 아직 정해지지 않아 원격 주소·도메인을 코드에 고정하지 않았다. 빌드에는 base URL이나 도메인 환경 변수가 필요 없다.

## 6. 핵심 기능 확인 방법

| 기능 | 현재 상태 | 확인 방법 / 합격 기준 |
|---|---|---|
| 첫 화면 | 구현됨 | 제목·대학 영문명 Donggang University·개설 준비 안내가 보이고 문자 깨짐이 없어야 함 |
| 내부 메뉴 | 구현됨 | 사용 계획/운영 원칙/FAQ/개설 안내를 누르면 같은 문서의 해당 구역으로 이동 |
| FAQ | 구현됨 | 질문을 클릭하거나 키보드 Enter로 열고 닫을 수 있어야 함 |
| 모바일 | 반응형 CSS 있음 | 390px 및 320px 너비에서 가로 잘림·겹침 없이 읽을 수 있어야 함 |
| 공개 실적 | 아직 미접수 상태 | 1억원은 목표 계획으로 표시, 실제 모금액이나 기부 완료로 표시하지 않아야 함 |
| 개인정보 제출 | 의도적으로 없음 | 입력 폼·기부자 명단·신청 API 요청이 없어야 함 |
| 로그인/관리자 | 미구현 | 테스트할 로그인 화면·계정·세션이 없음. 성공했다고 표시할 수 없음 |
| 결제/계좌 입금 | 미구현 | 결제 버튼·카드번호 입력·실제 계좌번호 없음. 실제 송금 시험 금지 |
| 영수증 | 안내문만 구현 | FAQ에 발급 주체·가능 여부 확인 전임을 표시 |
| HTTPS | 플랫폼 확인 필요 | 공개 후 HTTPS 연결, 혼합 콘텐츠 경고 없음, HTTP 접근은 HTTPS 이동 |
| 잘못된 경로 | 플랫폼 확인 필요 | 존재하지 않는 URL에 플랫폼 404가 나와야 함. SPA 경로로 대체하지 않음 |

첫 화면·390px 모바일 배치·메뉴 이동·FAQ 펼침은 이전 제작 단계에서 검수했다. 이번에는 HTML을 변경하지 않고 배포 패키징과 정적 구조를 검사했다. 새 플랫폼 배포가 없으므로 GitHub URL에서의 모바일·HTTPS·404 동작은 아직 검증하지 않았다. 320px 너비 검수는 공개 전 확인 항목이다.

## 7. 로그인·결제를 추가할 때 필요한 별도 작업

GitHub Pages 자체는 서버 실행이나 데이터베이스를 제공하지 않는다. 비밀번호·카드정보와 같은 민감한 거래를 처리하는 용도로 사용하지 않는 것이 GitHub의 안내다. 실제 기부 접수는 대학 공식 시스템 또는 적합한 서버 호스팅/결제사업자 화면에 연결하는 별도 설계가 필요하다.

- 로그인: 허용/거부 계정, 세션 만료, 로그아웃, 관리자 권한 우회 차단을 검증해야 한다.
- 결제: 사업자 테스트 모드에서 성공/취소/실패, 웹훅 서명, 중복 알림의 중복 집계 방지, 환급 반영을 검증해야 한다.
- 입금 관리: 담당자 승인 전에는 합계에 반영하지 않고, 입금·환급 원장으로 전체 금액을 계산해야 한다.
- 개인정보: 최소 수집, 공개 동의 분리, 보유기간·파기, 위탁·국외 이전, 접근 기록을 대학과 확정해야 한다.
- 은행·영수증·등록 관련 운영 정보는 앞선 검토처럼 대학 확인 후 반영한다.

이 내용은 향후 요구 사항이며 이번 패키지에 동작하는 백엔드가 포함되어 있다는 뜻이 아니다.

## 8. 문제 해결과 복구

| 증상 | 확인 위치 / 조치 |
|---|---|
| Run workflow가 안 보임 | 기본 브랜치에 `.github/workflows/pages.yml`이 있는지, Actions와 쓰기 권한이 허용되어 있는지 확인 |
| build 실패 | Actions의 Validate and build static output 로그 확인. `site/` 파일 목록, UTF-8, 링크, 폼·스크립트 추가 여부 점검 |
| validate만 했는데 deploy skipped | 정상. publish 기본값 false에 따른 결과 |
| 기본 브랜치 오류 | 실제 공개는 저장소 기본 브랜치를 선택 |
| configure-pages에서 404 | Pages가 미활성화되어 있거나 Actions 방식이 아님. 승인된 시점에 Pages 설정 확인; 자동 활성화는 끔 |
| permissions / OIDC 오류 | deploy job 권한과 조직 Actions 정책, github-pages 환경 규칙 확인 |
| 대기 중 | 환경 검토자의 승인 대기인지 확인 |
| 홈페이지 404 | deploy 성공 여부, 실제 반환 URL, artifact의 최상위 index.html 확인 |
| 변경이 보이지 않음 | 최신 배포 SHA와 해당 workflow의 artifact를 확인한 뒤 캐시를 갱신 |

이전 버전으로 되돌릴 때는 정상 버전의 변경을 기본 브랜치로 되돌린 뒤 새 빌드를 검증하고, 승인을 받아 수동 publish한다. 저장소 이력 강제 덮어쓰기는 필요 없다. 긴급 중단은 Pages 설정의 게시 중단 기능을 대학 운영 책임자가 확인해 수행한다. 복구/게시 중단 모두 이번에는 실행하지 않았다.

## 9. 공식 문서

아래는 2026-10-24 확인한 GitHub 공식 문서이며 실제 설정 화면은 계정/조직에 따라 달라질 수 있다.

- [사용자 정의 Pages workflow](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [게시 소스 설정](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
- [수동 workflow 실행](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [Pages HTTPS](https://docs.github.com/en/pages/getting-started-with-github-pages/securing-your-github-pages-site-with-https)
- [Pages 제한·사용 범위](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)
- [configure-pages 소스](https://github.com/actions/configure-pages)
