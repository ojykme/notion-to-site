# Notion to Static Site Generator

노션(Notion)에서 마크다운(Markdown) 형식으로 내보낸 파일들을 파싱하여, 깔끔한 레이아웃을 가진 HTML 정적 웹사이트로 변환해 주는 프로젝트입니다. 

변환된 웹사이트는 Cloudflare Pages, Vercel, Netlify 등을 통해 서버 비용 없이 무료로 배포할 수 있습니다.

## 🚀 주요 기능

- **노션 UUID 제거**: 파일 및 폴더명 끝에 자동으로 붙는 32자리 식별자(UUID)를 제거하여 깔끔한 파일명과 URL을 생성합니다.
- **GitBook 스타일의 계층형 사이드바 메뉴**: 폴더 구조를 재귀적으로 분석하여 접고 펼칠 수 있는(`<details>`) 계층형 트리 메뉴를 자동 생성합니다.
- **바닐라 JS 기반 강력한 검색 기능**: 외부 라이브러리(Fuse.js)의 느린 속도와 한글 형태소 분석 한계를 극복하기 위해, 브라우저 내장 기능을 이용한 초고속 100% 매칭 검색 기능(검색어 하이라이팅 지원)을 자체 구현했습니다.
- **두 가지 레이아웃 모드 지원**: 사이드바 메뉴가 있는 버전(`--out web`)과 사이드바 없이 메인 콘텐츠만 노출되는 버전(`--out web2 --no-menu`)을 독립적으로 생성할 수 있습니다.
- **스마트 링크 변환**: 마크다운 파일(`.md`) 간의 내부 링크를 새롭게 생성된 HTML(`.html`) 상대 경로로 자동 연결합니다.
- **CDN / S3 호환**: 코드 내의 `BASE_DOMAIN` 설정을 통해 이미지 등의 정적 에셋 경로를 일괄적으로 외부 저장소(S3 등) 주소로 변경할 수 있습니다.

## 🛠️ 설치 및 실행 방법

### 1. 파이썬 가상환경 세팅
프로젝트 폴더에서 가상환경을 생성하고 접속합니다.
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
.\venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate
```

### 2. 필요 패키지 설치
마크다운 파싱과 HTML 조작을 위한 패키지를 설치합니다.
```bash
pip install markdown beautifulsoup4
```

### 3. 노션 파일 준비
노션에서 [HTML 내보내기]가 아닌 **[Markdown 및 CSV 내보내기]**를 선택하여 다운로드한 압축 파일을 프로젝트의 `notion` 폴더 안에 압축 해제합니다.
- `notion/` 폴더 안에는 `.md` 파일과 이미지들이 담긴 폴더들이 위치해야 합니다.

### 4. 변환 스크립트 실행 (두 가지 모드)

**메뉴가 있는 버전으로 빌드하기:**
```bash
python build.py --out web
```
- 실행이 완료되면 `web/` 폴더에 사이드바 내비게이션 메뉴가 포함된 HTML 웹사이트가 생성됩니다.

**메뉴가 없는 버전으로 빌드하기:**
```bash
python build.py --out web2 --no-menu
```
- 실행이 완료되면 `web2/` 폴더에 사이드바가 숨겨진 깔끔한 단일 페이지 뷰 형태의 HTML 웹사이트가 생성됩니다.

## 🌐 무료 웹 호스팅 배포 (Cloudflare Pages)

생성된 폴더들은 Cloudflare Pages를 통해 전 세계 어디서든 빠르게 접속 가능한 무료 웹사이트로 배포할 수 있습니다.

1. Cloudflare CLI(`wrangler`)로 로그인합니다.
```bash
npx wrangler login
```

2. 메뉴가 있는 버전 배포 (`flexg-guide`)
```bash
npx wrangler pages deploy web --project-name=flexg-guide --branch=production
```

3. 메뉴가 없는 버전 배포 (`flexg-guides`)
```bash
npx wrangler pages deploy web2 --project-name=flexg-guides --branch=production
```

배포가 완료되면 터미널에 생성된 웹사이트 주소(URL)가 나타납니다!

## ⚙️ 설정 (CDN 연동)

추후 이미지나 정적 파일을 AWS S3나 별도의 CDN에 올려서 트래픽을 분산하고 싶다면, `build.py` 파일 내의 `BASE_DOMAIN` 변수에 주소를 입력하고 스크립트를 다시 실행하시면 됩니다.

```python
# build.py
BASE_DOMAIN = 'https://cdn.example.com/' 
```
값이 비어있을 경우(`''`) 자동으로 로컬 폴더의 상대 경로로 동작합니다.
