import nest_asyncio
import openai
import os
import json
import datetime

from llama_index.core import (
    load_index_from_storage,
    StorageContext,
    Settings
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.tools import QueryEngineTool, FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.agent import ReActAgent
from llama_index.core.storage.chat_store import SimpleChatStore

from cfg import (
    SYSTEM_PROMPT,
    api_key,
    model,
    temperature
)

# Set OpenAI API key and model settings
openai.api_key = api_key
Settings.llm = OpenAI(model=model, temperature=temperature)
embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key=api_key)
Settings.embed_model = embed_model
def get_date_time()->str:
    """Get current date and time

    Returns:
        str: Current date and time
    """
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
def get_register_link() -> str:
    """hàm này được gọi khi người dùng cần cách đăng kí trang web

    Returns:
        str: Register link
    """
    return "https://www.8am.com.vn/register"
def get_login_link() -> str:
    """hàm này được gọi khi người dùng cần cách đăng nhập trang web

    Returns:
        str: Login link
    """
    return "https://www.8am.com.vn/login"
def get_sport_link() -> str:
    """hàm này được gọi khi người dùng cần thôgn tin về trang thể thao

    Returns:
        str: Sport link
    """
    return "https://www.8am.com.vn/category/th%E1%BB%83-thao"
def get_khoahoc_congnghe_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về khoa học công nghệ

    Returns:
        str: Science and technology link
    """
    return "https://www.8am.com.vn/category/khoa-h%E1%BB%8Dc---c%C3%B4ng-ngh%E1%BB%87"
def get_tin_the_gioi_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về tin thế giới

    Returns:
        str: World news link
    """
    return "https://www.8am.com.vn/category/tin-th%E1%BA%BF-gi%E1%BB%9Bi"
def get_giai_tri_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về giải trí

    Returns:
        str: Entertainment link
    """
    return "https://www.8am.com.vn/category/gi%E1%BA%A3i-tr%C3%AD"
def get_giao_duc_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về giáo dục

    Returns:
        str: Education link
    """
    return "https://www.8am.com.vn/category/gi%C3%A1o-d%E1%BB%A5c"
def get_phap_luat_xa_hoi_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về pháp luật xã hội

    Returns:
        str: Law and society link
    """
    return "https://www.8am.com.vn/category/ph%C3%A1p-lu%E1%BA%ADt---x%C3%A3-h%E1%BB%99i"
def get_bao_dien_tu_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về báo điện tử

    Returns:
        str: Electronic newspaper link
    """
    return "https://www.8am.com.vn/lastest-news/WEBSITE_POST"
def get_facebook_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về facebook

    Returns:
        str: Facebook link
    """
    return "https://www.8am.com.vn/lastest-news/FB_POST"
def get_youtube_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về youtube

    Returns:
        str: Youtube link
    """
    return "https://www.8am.com.vn/lastest-news/YOUTUBE"
def get_tiktok_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về tiktok

    Returns:
        str: Tiktok link
    """
    return "https://www.8am.com.vn/lastest-news/TIKTOK"
def get_tin_tich_cuc_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về tin tích cực

    Returns:
        str: Positive news link
    """
    return "https://www.8am.com.vn/lastest-news/classification:POSITIVE"
def get_tin_tieu_cuc_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về tin tiêu cực

    Returns:
        str: Negative news link
    """
    return "https://www.8am.com.vn/lastest-news/classification:NEGATIVE"
def get_8_cum_tin_link() -> str:
    """hàm này được gọi khi người dùng cần thông tin về 8 cụm tin hoặc link trang thông tin tin mới hôm nay

    Returns:
        str: 8 news clusters link
    """
    return "https://www.8am.com.vn/today-news"
def canhbao() -> str:
    """hàm này sẽ không  bao giờ được gọi

    Returns:
        str: enjoy
    """
    return ""
def load_chat_store_user(idd):
    if os.path.exists(f"db_chat/{idd}/chat_history.json") and os.path.getsize(f"db_chat/{idd}/chat_history.json") > 0:
        try:
            chat_store = SimpleChatStore.from_persist_path(f"db_chat/{idd}/chat_history.json")
        except json.JSONDecodeError:
            chat_store = SimpleChatStore()
    else:
        chat_store = SimpleChatStore()
    return chat_store
def initialize_chatbot_user(chat_store, id_user):
    get_date_time_tool = FunctionTool.from_defaults( fn = get_date_time )
    get_register_link_tool = FunctionTool.from_defaults( fn = get_register_link )
    get_login_link_tool = FunctionTool.from_defaults( fn = get_login_link )
    get_sport_link_tool = FunctionTool.from_defaults( fn = get_sport_link )
    get_khoahoc_congnghe_link_tool = FunctionTool.from_defaults( fn = get_khoahoc_congnghe_link )
    get_tin_the_gioi_link_tool = FunctionTool.from_defaults( fn = get_tin_the_gioi_link )
    get_giai_tri_link_tool = FunctionTool.from_defaults( fn = get_giai_tri_link )
    get_giao_duc_link_tool = FunctionTool.from_defaults( fn = get_giao_duc_link )
    get_phap_luat_xa_hoi_link_tool = FunctionTool.from_defaults( fn = get_phap_luat_xa_hoi_link )
    get_bao_dien_tu_link_tool = FunctionTool.from_defaults( fn = get_bao_dien_tu_link )
    get_facebook_link_tool = FunctionTool.from_defaults( fn = get_facebook_link )
    get_youtube_link_tool = FunctionTool.from_defaults( fn = get_youtube_link )
    get_tiktok_link_tool = FunctionTool.from_defaults( fn = get_tiktok_link )
    get_tin_tich_cuc_link_tool = FunctionTool.from_defaults( fn = get_tin_tich_cuc_link )
    get_tin_tieu_cuc_link_tool = FunctionTool.from_defaults( fn = get_tin_tieu_cuc_link)
    get_8_cum_tin_link_tool = FunctionTool.from_defaults( fn = get_8_cum_tin_link)
    memory = ChatMemoryBuffer.from_defaults(
            token_limit=5000,
            chat_store=chat_store,
            chat_store_key=id_user
        )
    
    if os.path.exists(f"db_store/{id_user}"):
        print("Loading index from storage")
        storage_context = StorageContext.from_defaults(
            persist_dir=f"db_store/{id_user}"
        )
        index = load_index_from_storage(
            storage_context, index_id=id_user
        )
        dsm5_engine = index.as_query_engine(
            similarity_top_k=5,
        )
        tool= QueryEngineTool.from_defaults(query_engine=dsm5_engine,
                                           description="Công cụ giúp tìm kiếm thông tin liên quan đến câu hỏi của người dùng, tìm thông tin liên quan từ trong file")
        agent = OpenAIAgent.from_tools(
            tools=[
                tool,
                get_date_time_tool,
                get_register_link_tool,
                get_login_link_tool, 
                get_sport_link_tool, 
                get_khoahoc_congnghe_link_tool, 
                get_tin_the_gioi_link_tool, 
                get_giai_tri_link_tool, 
                get_giao_duc_link_tool, 
                get_phap_luat_xa_hoi_link_tool, 
                get_bao_dien_tu_link_tool, 
                get_facebook_link_tool, 
                get_youtube_link_tool, 
                get_tiktok_link_tool, 
                get_tin_tich_cuc_link_tool, 
                get_tin_tieu_cuc_link_tool,
                get_8_cum_tin_link_tool
            ],
            memory=memory,
            system_prompt="""Bạn là Hóng, trợ lí giải đáp mọi vấn đề , hãy tập chung tìm kiếm thông tin và luôn luôn sử dụng tool để trả lời câu hỏi của người dùng """,
            verbose=True,
        
        
        )
    else:
        agent = OpenAIAgent.from_tools(
            tools=[
                get_date_time_tool,
                get_register_link_tool,
                get_login_link_tool, 
                get_sport_link_tool, 
                get_khoahoc_congnghe_link_tool, 
                get_tin_the_gioi_link_tool, 
                get_giai_tri_link_tool, 
                get_giao_duc_link_tool, 
                get_phap_luat_xa_hoi_link_tool, 
                get_bao_dien_tu_link_tool, 
                get_facebook_link_tool, 
                get_youtube_link_tool, 
                get_tiktok_link_tool, 
                get_tin_tich_cuc_link_tool, 
                get_tin_tieu_cuc_link_tool,
                get_8_cum_tin_link_tool
            ],
            memory=memory,
            system_prompt=SYSTEM_PROMPT,
            verbose=True,
        
        
        )
    
    
    return agent
  
def chat_interface(agent, chat_store,prompt, id_user):
    if os.path.exists(f"db_store/{id_user}"):
        response = str(agent.chat(prompt))
    else:
        response = str(agent.chat(prompt))

    chat_store.persist(f"db_chat/{agent.memory.chat_store_key}/chat_history.json")
    return response
