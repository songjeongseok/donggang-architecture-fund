# GitHub Pages 배포 결과

확인일: 2026-10-24 (한국 시간)

## 공개 주소와 소스

- 공개 홈페이지: https://songjeongseok.github.io/donggang-architecture-fund/
- 저장소: https://github.com/songjeongseok/donggang-architecture-fund
- 기본 브랜치: `main`
- 실제 배포된 소스 커밋: `8c67a39ab4561fee019cc2aa2c320bcdbc8a3eda`
- 공개 범위: 인터넷 공개. 현재는 개설 준비 안내이며 기부 신청·입금을 받지 않음.
- 기존 Sites 검토용 배포와 다른 저장소들은 변경하지 않음.

## 실행 결과

| 실행 | 결과 | 확인 내용 |
|---|---|---|
| [검증 실행 #1](https://github.com/songjeongseok/donggang-architecture-fund/actions/runs/40103049845) | 성공 | build 성공, deploy skipped |
| [공개 배포 #2](https://github.com/songjeongseok/donggang-architecture-fund/actions/runs/40103194354) | 성공 | build 성공, deploy 성공, 공식 page URL 반환 |
| 공개 페이지 열기 | 성공 | 한글 제목, 개설 준비 및 미접수 안내, 건축 이미지 정상 표시 |
| 메뉴 이동 | 성공 | 자주 묻는 질문 링크가 `#faq` 구역으로 이동 |
| FAQ 동작 | 성공 | 영수증 질문 클릭으로 펼침, Enter로 접힘 |
| HTTPS | 확인 | Enforce HTTPS 적용, HTTP URL을 열면 HTTPS로 이동 |
| 데스크톱 폭 | 확인 | 1348px 화면에서 가로 넘침 없음 |

빌드 검사는 내부 링크 12개, FAQ 7개, 폼 0개, 스크립트 0개를 확인했다. 공개 파일은 `index.html`과 `.nojekyll` 두 개뿐이다. HTML SHA-256: `b500ff7514ccacc43147b14f7ddeb0609157f6e18ea37c5e17c27255e8a8fa98`.

390px 모바일 배치는 같은 HTML의 이전 제작 검수에서 확인했다. 이번 공개 URL에서 320px/390px의 별도 화면 검수와 잘못된 URL의 404 응답 검사는 수행하지 않았다. 로그인·결제·신청 저장·실입금 집계 기능은 구현되어 있지 않아 해당 테스트도 수행하지 않았다.

## 실제 설정

| 위치 | 설정 |
|---|---|
| Settings → Pages → Build and deployment → Source | GitHub Actions |
| Settings → Pages → Enforce HTTPS | 적용됨; 기본 github.io 도메인에서 필수 |
| Settings → Pages → Custom domain | 미설정 |
| Settings → Environments → github-pages | `main` 브랜치 1개, 태그 0개 허용 |
| 환경 검토자 / 대기 시간 | 미설정; 기존 기본 상태 유지 |
| 환경 secrets / variables | 없음 |
| 워크플로 | `.github/workflows/pages.yml`; 수동 실행만 가능 |
| 빌드 | `python3 scripts/build.py`; Python 3.9 이상, 외부 패키지 없음 |
| 운영 서버 / DB | 필요 없음 |

GitHub가 공식 Actions의 Node.js 20 지원 종료와 ubuntu-latest 이미지 전환 안내를 표시했다. 이번 두 실행은 성공했고 Node.js 24에서 실행되었다. 이후 GitHub 공식 Pages Actions의 후속 버전이 나오면 호환성을 확인해 갱신할 항목이다. 경고를 숨기거나 실행 환경의 보안 보호를 낮추지 않았다.

## 이후 수정·재배포

1. `site/index.html`을 수정한다. `dist`는 생성물이라 직접 수정하지 않는다.
2. `python3 scripts/build.py`를 실행한다.
3. 검토한 소스를 `main`에 반영한다. 커밋만으로 자동 배포되지는 않는다.
4. Actions → Validate and optionally publish Pages → Run workflow에서 publish를 끄고 검증한다.
5. 공개할 변경이 확정되면 같은 메뉴에서 `main`과 publish를 선택해 실행한다.
6. build/deploy 성공과 실제 공개 URL의 화면을 확인한다.

이 보고서와 README의 배포 결과 기록은 문서만 변경한다. 홈페이지는 위 소스 커밋의 정적 산출물을 계속 사용하며 문서 갱신 때문에 재배포할 필요는 없다.

## 실제 모금 시작 전 담당 사항

- 대학 담당 부서와 운영 주체·공식 수납 및 회계 절차·모집 관련 필요 절차를 확정한다.
- 공식 계좌의 은행·예금주·번호, 담당 문의처, 영수증 발급 가능 여부를 확인한다.
- 개인정보 처리, 공개 동의, 반환 및 사용 내역 공개 절차를 마련한다.
- 확정된 정보에 맞춰 안내와 접수 방식 및 검증 규칙을 별도 변경한다. 계좌만 넣으면 결제·집계 기능이 생기는 구조가 아니다.

`DEPLOYMENT.md`는 최초 준비 시점의 상태와 상세 절차를 보존한 문서다. 현재 배포 여부와 실제 확인된 설정은 이 보고서를 기준으로 한다.
