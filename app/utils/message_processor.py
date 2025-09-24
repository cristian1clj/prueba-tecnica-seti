import re
import json
from datetime import datetime, timezone
from typing import List

BLOCKED_WORDS = ['maldicion', 'estupidez', 'recorcholis']

def _replace_blocked_words(content: str, banned: List[str]) -> str:
    cleaned = []
    for word in content.split():
        normalized = re.sub(r'[^\w]', '', word.lower())
        if any(banned_word in normalized for banned_word in banned):
            cleaned.append('***')
        else:
            cleaned.append(word)
            
    return ' '.join(cleaned)

def process_message(content: str):
    cleaned = _replace_blocked_words(content, BLOCKED_WORDS)
    word_count = len(re.findall(r"\w+", cleaned, flags=re.UNICODE))
    character_count = len(cleaned)
    processed_at = datetime.now(timezone.utc)
    
    metadata = {
        'word_count': word_count,
        'character_count': character_count,
        'processed_at': processed_at
    }
    
    return cleaned, metadata