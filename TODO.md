# 🚀 넥스트 스텝: Notion API & 자동화 (실시간 연동) TODO

현재 프로젝트는 노션에서 '수동으로' 마크다운을 다운로드 받아 빌드 및 배포하는 구조입니다. 이를 **노션에서 글을 수정하면 웹사이트에 자동으로(실시간 혹은 주기적으로) 반영되도록** 고도화하기 위한 향후 작업(TODO) 가이드입니다.

---

## 1. 아키텍처 개요 (목표 모델)
노션 자체는 현재 공식적인 '발신 웹훅(Outgoing Webhook)'을 지원하지 않기 때문에, 아래의 두 가지 방식 중 하나를 선택해야 합니다.

* **A안 (스케줄링 기반 주기적 동기화)**: GitHub Actions의 `cron`을 사용해 매일/매시간 주기적으로 노션 데이터를 긁어와서 자동 빌드 후 배포합니다.
* **B안 (외부 자동화 툴 활용 실시간 동기화)**: Zapier 또는 Make(구 Integromat)를 사용하여 노션 페이지 변경이 감지되면 GitHub Actions의 `repository_dispatch` 웹훅을 쏴서 빌드 파이프라인을 트리거합니다.

---

## 2. 세부 구현 TODO 리스트

### ✅ [단계 1] Notion API 연동 및 자동 추출기(Exporter) 구축
수동으로 마크다운을 압축 해제하던 과정을 자동화해야 합니다.

- [ ] **Notion Integration(API Key) 발급**: [Notion Developers](https://developers.notion.com/)에서 새 API 프라이빗 키 발급하기
- [ ] **가이드 대상 Notion 페이지에 API 봇 초대하기**
- [ ] **파이썬 추출 스크립트 작성 (또는 오픈소스 활용)**:
  - `notion-client` 라이브러리를 사용해 특정 최상위 페이지의 하위 구조를 재귀적으로 순회하는 로직 구현.
  - 각 페이지의 블록(Block) 데이터를 읽어 마크다운으로 역변환(Reverse Parsing)하는 로직 추가. (기존 오픈소스인 `notion2md` 같은 패키지를 활용하는 것을 적극 권장)
  - 파싱된 마크다운과 이미지 에셋들을 기존의 `notion/` 폴더 위치에 자동으로 저장하도록 스크립트화(`fetch_notion.py`).

### ✅ [단계 2] 빌드 및 배포 파이프라인 자동화 (CI/CD)
GitHub Actions를 이용하여 모든 과정을 스크립트로 자동 실행합니다.

- [ ] **GitHub Secrets 설정**:
  - `NOTION_API_KEY`: 노션 API 키
  - `CLOUDFLARE_API_TOKEN`: Cloudflare Pages 배포용 토큰
  - `CLOUDFLARE_ACCOUNT_ID`: Cloudflare 계정 ID
- [ ] **`.github/workflows/deploy.yml` 작성**:
  ```yaml
  name: Notion to Cloudflare Pages Auto Deploy
  
  on:
    # 1. 주기적으로 실행 (예: 매일 자정)
    schedule:
      - cron: '0 0 * * *'
    # 2. 외부 웹훅 트리거 (Zapier 등에서 호출 시)
    repository_dispatch:
      types: [notion_updated]
    # 3. 수동 실행 버튼
    workflow_dispatch:

  jobs:
    build-and-deploy:
      runs-on: ubuntu-latest
      steps:
        - name: 저장소 체크아웃
          uses: actions/checkout@v3

        - name: 파이썬 환경 설정
          uses: actions/setup-python@v4
          with:
            python-version: '3.10'

        - name: 패키지 설치
          run: pip install -r requirements.txt

        - name: Notion 데이터 자동 추출 (새로 만들 스크립트)
          env:
            NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          run: python fetch_notion.py

        - name: 사이트 정적 빌드 (메뉴 O / 메뉴 X)
          run: |
            python build.py --out web
            python build.py --out web2 --no-menu

        - name: Cloudflare Pages 배포 (메뉴 있는 버전)
          uses: cloudflare/pages-action@v1
          with:
            apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
            accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
            projectName: flexg-guide
            directory: web
            branch: production

        - name: Cloudflare Pages 배포 (메뉴 없는 버전)
          uses: cloudflare/pages-action@v1
          with:
            apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
            accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
            projectName: flexg-guides
            directory: web2
            branch: production
  ```

### ✅ [단계 3] 실시간 트리거 구성 (선택 사항: B안)
페이지가 갱신될 때마다 즉시 배포되게 만들고 싶을 때 진행합니다.

- [ ] **Zapier / Make(Integromat) 가입 및 시나리오 생성**
- [ ] **트리거(Trigger) 설정**: Notion - "Updated Page in Database" 이벤트 감지
- [ ] **액션(Action) 설정**: Webhooks by Zapier (또는 HTTP 모듈)
  - **Method**: `POST`
  - **URL**: `https://api.github.com/repos/ojykme/notion-to-site/dispatches`
  - **Headers**:
    - `Accept: application/vnd.github.v3+json`
    - `Authorization: token [GitHub Personal Access Token]`
  - **Body**: `{"event_type": "notion_updated"}`

---

## 💡 요약 및 팁
이 TODO 대로 구축이 완료되면, 사용자는 그저 **노션에서 글을 쓰고 수정하기만 하면 됩니다.** 
수정이 감지되거나 정해진 시간마다 GitHub가 자동으로 노션에서 데이터를 가져와(Fetch), 파이썬으로 HTML로 변환하고(Build), Cloudflare로 전 세계에 배포(Deploy)하는 "완전 자동화 무인 파이프라인"이 완성됩니다!
