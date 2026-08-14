from typing import Any, Optional

class AppState:
    def __init__(self):
        self.vlm_model: Optional[Any] = None
        self.processor: Optional[Any] = None
        self.embedding_model: Optional[Any] = None
        self.reranker: Optional[Any] = None
        self.tokenizer: Optional[Any] = None