# IdeaBank

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
