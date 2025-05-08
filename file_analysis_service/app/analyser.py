from dataclasses import dataclass

@dataclass
class TextStatistics:
    word_count: int
    char_count: int
    paragraph_count: int

def analyze_text(content: str) -> TextStatistics:
    paragraphs = [p for p in content.split('\n') if p.strip()]
    words = content.split()
    return TextStatistics(
        word_count=len(words),
        char_count=len(content),
        paragraph_count=len(paragraphs)
    )