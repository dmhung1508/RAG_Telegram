from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext,
    Settings
)
from mongo import get_prompt_comment
from llama_index.embeddings.openai import OpenAIEmbedding
from cfg import api_key
embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=api_key)
Settings.embed_model = embed_model
def load_phongcach(prompt, role_id):
    storage_context = StorageContext.from_defaults(
        persist_dir="storage_pcc/"
    )
    vector_index = load_index_from_storage(
        storage_context, index_id="index_pc"
    )
    query_engine = vector_index.as_query_engine(
        similarity_top_k=3,
        response_mode = "no_text"
    )
    search_results = query_engine.query(prompt)
    b1 = search_results.source_nodes[0].text
    b2 = search_results.source_nodes[1].text
    b3 = search_results.source_nodes[2].text
    prompt = get_prompt_comment(role_id)
    prompt_comment = prompt.format(b1=b1, b2=b2, b3=b3)
    return prompt_comment
