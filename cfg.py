# model openai
api_key = 
mongo_url = 
model = "gpt-4o-mini"
temperature = 0

CACHE_FILE = "data/cache/pipeline_cache1.json"
CONVERSATION_FILE = "data/cache/chat_history1.json"
STORAGE_PATH = "data/ingestion_storage1/"
FILES_PATH = ["data/ingestion_storage/dsm-5-cac-tieu-chuan-chan-doan.docx"]
INDEX_STORAGE = "data/index_storage1"
SCORES_FILE = "data/user_storage/scores.json"
USERS_FILE = "data/user_storage/users.yaml"
STORE_TEXT = "textcontent"
CUSTORM_SUMMARY_EXTRACT_TEMPLATE = """
Dưới đây là nội dung của phần:
{context_str}

Hãy tóm tắt các chủ đề và thực thể chính của phần này.

Tóm tắt: """
SYSTEM_PROMPT = """
   Bạn là Hóng, trợ lí giải đáp mọi vấn đề , hãy tập chung tìm kiếm thông tin và luôn luôn sử dụng tool để trả lời câu hỏi của người dùng ( có thể sẽ hỏi về cà phê )
   tập chung sử dụng query_engine_tool để tìm thông tin liên quan đến câu hỏi của người dùng

"""
