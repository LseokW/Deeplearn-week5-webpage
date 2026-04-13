import json
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent.parent / "content" / "week5"
ALLOWED_SECTIONS = {"reg", "overfit", "augment", "transfer", "cnn"}


def get_sections_metadata() -> list[dict]:
    sections_file = CONTENT_DIR / "sections.json"
    with open(sections_file, encoding="utf-8") as f:
        return json.load(f)


def get_section_content(section_id: str) -> str:
    # path traversal 방지: 화이트리스트 검증
    if section_id not in ALLOWED_SECTIONS:
        return None
    md_file = CONTENT_DIR / f"{section_id}.md"
    if not md_file.exists():
        return None
    return md_file.read_text(encoding="utf-8")


def get_image_path(filename: str) -> Path | None:
    # path traversal 방지: 파일명에 경로 구분자 불허
    if "/" in filename or "\\" in filename or ".." in filename:
        return None
    image_path = CONTENT_DIR / "images" / filename
    if not image_path.exists():
        return None
    return image_path
