#!/usr/bin/env python3
"""claude.ai 대화 내보내기(conversations.json)에서 '만들고 싶었던 것'의 흔적을 추출한다.

사용법:
    python3 tools/extract_ideas.py data/conversations.json [output/idea-traces-raw.md]

사용자(human) 발화 중 프로그램/서비스/도구를 만들고 싶어 했거나 필요로 했던
신호가 담긴 문장을 찾아, 대화별로 묶어 Markdown으로 출력한다.
"""

import json
import re
import sys
from pathlib import Path

# "만들고 싶다 / 필요하다 / 있으면 좋겠다" 류의 신호 (한국어 + 영어)
SIGNAL_PATTERNS = [
    r"만들\s*고\s*싶",
    r"만들\s*어\s*(줘|주세요|볼까|보고\s*싶)",
    r"개발\s*(하고\s*싶|해\s*줘|해\s*주세요|해\s*볼까)",
    r"구현\s*(하고\s*싶|해\s*줘|해\s*주세요)",
    r"있으면\s*좋겠",
    r"필요\s*(해|한데|하다|할\s*것\s*같)",
    r"자동화\s*(하고\s*싶|하면|해\s*줘)",
    r"(앱|어플|웹\s*사이트|사이트|서비스|프로그램|도구|툴|봇|크롬\s*확장|확장\s*프로그램)\s*(을|를)?\s*만들",
    r"이런\s*(거|것|게)\s*(있나|없나|있을까|없을까)",
    r"\bI\s+(want|wanted|need|needed|wish)\s+(to\s+)?(build|make|create|develop|have)\b",
    r"\b(can|could)\s+(you|we)\s+(build|make|create|develop)\b",
    r"\bit\s+would\s+be\s+(nice|great|cool)\s+(to\s+have|if)\b",
    r"\bis\s+there\s+(a|an|any)\s+(tool|app|service|extension|bot)\b",
]

SIGNALS = [re.compile(p, re.IGNORECASE) for p in SIGNAL_PATTERNS]

# 문맥으로 넣을 앞뒤 글자 수
CONTEXT_CHARS = 400


def message_text(msg):
    """내보내기 포맷 차이를 흡수해 메시지의 텍스트를 얻는다."""
    text = msg.get("text") or ""
    if not text and isinstance(msg.get("content"), list):
        parts = []
        for block in msg["content"]:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        text = "\n".join(parts)
    return text


def find_hits(text):
    """신호가 걸린 위치들을 (패턴, 발췌문) 목록으로 반환."""
    hits = []
    for sig in SIGNALS:
        for m in sig.finditer(text):
            start = max(0, m.start() - CONTEXT_CHARS // 2)
            end = min(len(text), m.end() + CONTEXT_CHARS)
            excerpt = text[start:end].strip()
            hits.append(excerpt)
    # 중복/포함 관계 제거
    unique = []
    for h in sorted(hits, key=len, reverse=True):
        if not any(h in u for u in unique):
            unique.append(h)
    return unique


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("output/idea-traces-raw.md")
    dst.parent.mkdir(parents=True, exist_ok=True)

    conversations = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(conversations, dict):  # 일부 포맷은 {"conversations": [...]}
        conversations = conversations.get("conversations", [])

    sections = []
    total_hits = 0
    for conv in conversations:
        name = conv.get("name") or "(제목 없음)"
        created = (conv.get("created_at") or "")[:10]
        conv_hits = []
        for msg in conv.get("chat_messages", []):
            if msg.get("sender") != "human":
                continue
            text = message_text(msg)
            if not text:
                continue
            conv_hits.extend(find_hits(text))
        if conv_hits:
            total_hits += len(conv_hits)
            body = "\n\n".join(f"> {h}" for h in conv_hits)
            sections.append(f"## {name} ({created})\n\n{body}\n")

    header = (
        "# 아이디어 흔적 (원본 추출)\n\n"
        f"- 원본 파일: `{src}`\n"
        f"- 대화 수: {len(conversations)}개 중 흔적 발견 {len(sections)}개\n"
        f"- 발췌 수: {total_hits}건\n\n"
        "이 파일은 기계 추출 결과입니다. Claude에게 `templates/idea-traces-template.md` "
        "형식으로 압축 정리(이미 구현한 것 제외)를 요청하세요.\n\n---\n\n"
    )
    dst.write_text(header + "\n".join(sections), encoding="utf-8")
    print(f"완료: {dst} (대화 {len(sections)}개, 발췌 {total_hits}건)")


if __name__ == "__main__":
    main()
