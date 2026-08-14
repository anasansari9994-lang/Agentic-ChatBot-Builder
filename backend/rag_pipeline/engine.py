from llama_index.core import VectorStoreIndex
from llama_index.retrievers import VectorIndexRetriever, Documents, StorageContext
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core.postprocessor import SentenceTransformerRerank

from core.setting import setting
from core.state import state

from rag_pipeline.chunker import chunk_embedding

def get_postgres_vector_store():
    return PGVectorStore.from_params(
        database="posgress",
        port=5432,
        host="localhost",
        user="postgres",
        password="Anas#786",
        table_name="chatbot_knowledge",
        embed_dim=384,
        hnsw_kwargs={
            "hnsw_m": 16,
            "hnsw_ef_construction": 64,
            "hnsw_ef_search": 40,
            "hnsw_dist_method": "vector_cosine_ops"
        }
    )

def build_query_engine(documents):

    vector_store = get_postgres_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if documents:
        nodes = chunk_embedding(documents)
        index = VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=state.embedding_model,
            show_progress=True
        )
    else:
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=state.embedding_model
        )
    retrival = index.as_retriever(
        similarity_top_k=setting.TOP_K_RETRIVAL
    )

    reranker = SentenceTransformerRerank(
            model=setting.RERANKING_MODEL,
            top_n=setting.TOP_N_RERANKING
    )

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retrival,
        node_postprocessors=[reranker],
        llm = state.vlm_model
    )

    return query_engine