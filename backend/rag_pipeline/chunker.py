from typing import List
from llama_index.core import Document
from core.logging import logger
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import (
    SemanticNodeParser,
    SentenceNodeParser,
    HierarchicalNodeParser,
    SentenceSplitter
)
from llama_index.embedding.huggingface import HuggingFaceEmbedding
from core.state import state
from core.setting import setting

def adv_chunker():
    logger.info("advanced chunker is running")
    strategy = getattr(setting, "chunking_strategy", "standard")
    chunk_size = getattr(setting, "chunk_size", 1024)
    chunk_overlap = getattr(setting, "chunk_overlap", 200)

    if strategy == "semantic":
        embed_model_name = getattr(setting, "embed_model", "BAAI/bge-small-en-v1.5")
        embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
        return SemanticNodeParser.from_defaults(
            buffer_size = 1,
            breakpoint_percentile_threshold=95,
            embed_model=embed_model
        )

    elif strategy == "hierarchical":
        return SentenceNodeParser.from_default(
            chunk_size = [2048, 512, 128]
        )
        
    elif strategy == "sentence":
        return SentenceNodeParser.from_default()
    
    else:
        return SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

def chunk_embedding(documents: List[Document]) -> List[BaseNode]:
    logger.info("The Embedding model is Running")
    if not documents:
        return []

    print(f"Starting chunking process for {len(documents)} documents...")
    parser = get_node_parser()
    nodes = parser.get_node_from_documents(documents)

    if hasattr(state, "update"):
        state.update({"total_nodes_created": len(nodes)})
    print(f"Successfully created {len(nodes)} chunks using {parser.__class__.__name__}.")
    return nodes