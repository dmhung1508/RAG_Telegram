from cfg import *
from fastapi import FastAPI, File, UploadFile, Depends, Form
from pydantic import BaseModel, validator
import uvicorn
from openai import OpenAI
from typing import Optional, List
import os
import aiohttp
import tempfile
import shutil
from create_node import create_node_telegram,create_or_update_node_telegram
from load_chat import load_chat_store_user, initialize_chatbot_user, chat_interface
app = FastAPI(
    title="Chatbot API",
    description="API for chatbot",
    version="0.1",
    path = "/"
)

@app.get("/")
def read_root():
    return "USE POST"
class CreateDB:
    def __init__(self, id_user: str = Form(...), session_id: str = Form(...)):
        self.id_user = id_user
        self.session_id = session_id


@app.post("/upload")
async def upload_and_process_files(
    id_user: str = Form(...), 
    file_links: List[str] = Form(...)
):
    temp_dir = tempfile.mkdtemp()
    try:
        file_paths = []
        
        for file_link in file_links:
            file_name = file_link.split("/")[-1]
            file_path = os.path.join(temp_dir, file_name)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(file_link) as response:
                    if response.status == 200:
                        with open(file_path, "wb") as f:
                            f.write(await response.read())  # Save the file
                        file_paths.append(file_path)
                    else:
                        return {"message": f"Failed to download file from {file_link}"}

        vector_index = create_or_update_node_telegram(id_user, file_paths)

        return {"message": "Files processed successfully"}
    
    finally:
        # Clean up: remove the temporary directory
        shutil.rmtree(temp_dir)
@app.post("/chat")
async def chat(
    id_user: str = Form(...),
    message: str = Form(...)
):
    try:
        chat_store = load_chat_store_user(id_user)
        agent = initialize_chatbot_user(chat_store, id_user)
        response = chat_interface(agent,chat_store, message, id_user)

        return {"message": response}
    except Exception as e:
        return {"message": str(e)}
@app.post("/delete")
async def delete(
    id_user: str = Form(...),
):
    try:
        shutil.rmtree(f"db_store/{id_user}")
        shutil.rmtree(f"db_chat/{id_user}")
        return {"message": "Deleted"}
    except Exception as e:
        return {"message": str(e)}
if __name__ == "__main__":
    uvicorn.run(app, host = '0.0.0.0', port=8500)
