class AppState:
    def __init__(self):
        self.vlm_model = None
        self.processor = None
        self.embedding_model = None
        self.reranker = None
        self.tokenizer = None

state = AppState()