# IdeaBank

## TakeHome — 미국 세후 소득 계산기 (배포 준비 완료)

`docs/` 폴더에 배포용 사이트가 있습니다 (SEO 메타태그·구조화 데이터·robots.txt·sitemap.xml 포함).

**GitHub Pages로 공개하는 법** (이 브랜치를 main에 머지한 뒤):

1. GitHub 저장소 → **Settings → Pages**
2. Source: **Deploy from a branch** → Branch: `main`, Folder: `/docs` → Save
3. 몇 분 뒤 `https://danieldongjunlee-cell.github.io/IdeaBank/` 에서 공개됩니다.

**검색 노출을 위해 배포 직후 할 일:**

1. [Google Search Console](https://search.google.com/search-console)에 사이트 등록 → 소유권 확인 → `sitemap.xml` 제출 → URL 검사에서 "색인 생성 요청"
2. [Bing Webmaster Tools](https://www.bing.com/webmasters)에도 동일하게 등록
3. `prototype/takehome-map.html`과 `docs/index.html`의 `AFFILIATES` 객체에 실제 제휴 링크를 넣기 (현재는 자리표시자)
4. **사용자 입력 수집**: `analytics/README.md`의 5분 설정(구글 시트 + Apps Script)을 마친 뒤
   두 HTML 파일의 `ANALYTICS_ENDPOINT`에 웹앱 URL을 넣으면 방문자 시나리오가 시트에 쌓입니다
   (비워두면 수집 완전 비활성화)
4. 커스텀 도메인(예: takehome.tax 같은)을 쓰면 신뢰도·클릭률·순위에 모두 유리합니다 — Pages 설정에서 연결 후 `canonical`/`sitemap`/`robots`의 URL을 교체하세요.

순위는 색인 시간·콘텐츠·백링크에 따라 올라갑니다. 페이지 내부(on-page) SEO는 모두 적용되어 있습니다.

---

지금까지 Claude와 나눈 대화에서 **"내가 만들고 싶어 했거나 필요로 했던"** 프로그램·서비스·도구의 흔적을 발굴하고, 압축 정리한 뒤, 전문가 컨설팅까지 이어가는 파이프라인입니다.

## 왜 이런 구조인가?

Claude Code 세션(이 리포지토리)에서는 claude.ai 웹/앱의 과거 대화 기록에 직접 접근할 수 없습니다. 그래서 대화 기록을 **내보내기(export)** 한 뒤 이 리포지토리에 넣으면, 나머지는 자동으로 처리되도록 만들어져 있습니다.

## 사용 방법

### 1단계 — 대화 기록 내보내기

1. [claude.ai](https://claude.ai) 접속 → **설정(Settings) → 프라이버시(Privacy) → 데이터 내보내기(Export data)**
2. 이메일로 도착한 압축 파일에서 `conversations.json`을 꺼냅니다.
3. 이 리포지토리의 `data/` 폴더에 넣습니다:

```
data/conversations.json
```

### 2단계 — 아이디어 흔적 추출

```bash
python3 tools/extract_ideas.py data/conversations.json
```

- 사용자 발화 중 "만들고 싶다 / 필요하다 / 있으면 좋겠다" 류의 신호를 탐지해
  `output/idea-traces-raw.md`(원본 흔적)를 생성합니다.
- 이후 Claude에게 "output의 원본 흔적을 `templates/idea-traces-template.md` 형식으로
  압축 정리해줘"라고 요청하면 최종 `output/idea-traces.md`가 만들어집니다.
  (이미 완성/구현한 프로젝트는 이 단계에서 제외합니다.)

### 3단계 — 전문가 컨설팅

`consulting/expert-consult-prompt.md`의 프롬프트에 `output/idea-traces.md`를 첨부해
Claude에게 전달하면, 제품/시장/기술 관점의 다각도 컨설팅 리포트를 받을 수 있습니다.

## 폴더 구조

```
data/        # 대화 내보내기 파일 (git에 커밋되지 않음)
tools/       # 추출 스크립트
templates/   # 압축 MD 템플릿
consulting/  # 전문가 컨설팅 프롬프트
output/      # 생성된 결과물 (git에 커밋되지 않음)
```
