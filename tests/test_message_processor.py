from app.utils import message_processor
from datetime import datetime

def test_process_message_removes_blocked_words():
    content = "Hola recorcholis mundo"
    cleaned, metadata = message_processor.process_message(content)
    assert "***" in cleaned
    assert metadata["word_count"] == len(cleaned.split())
    
def test_process_message_generate_metadata():
    content = "Hola querido mundo"
    cleaned, metadata = message_processor.process_message(content)
    assert isinstance(metadata["word_count"], int)
    assert metadata["word_count"] == len(cleaned.split())
    assert isinstance(metadata["character_count"], int)
    assert metadata["character_count"] == len(cleaned)
    assert isinstance(metadata["processed_at"], datetime)