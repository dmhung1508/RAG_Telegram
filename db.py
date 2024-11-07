import sqlite3
from openai import OpenAI
from cfg import api_key
from mongo import find_by_id
from utils import load_phongcach
conn = sqlite3.connect('ids.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ids (id TEXT PRIMARY KEY)''')
c.execute('''
    CREATE TABLE IF NOT EXISTS binhluan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        articleId TEXT UNIQUE,
        articleLink TEXT UNIQUE,
        text TEXT
    )
''')
c.execute('''
          CREATE TABLE IF NOT EXISTS next_question (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              id_post TEXT UNIQUE,
              question_1 TEXT UNIQUE,
              question_2 TEXT UNIQUE,
              question_3 TEXT UNIQUE
          )
          ''')

def getbinhluan(text, prompt):
    client = OpenAI(
        api_key=api_key,
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                'role': 'user',
                'content': text
            }
        ],
        temperature=0.2,
        max_tokens=2056,

        # request_timeout=config.REQUEST_TIMEOUT,
        model='gpt-4o-mini',
    )
    response = chat_completion.choices[0].message.content
    return response
def delete_ids():
    c.execute('DELETE FROM ids')
    conn.commit()
def delete_binhluan():
    c.execute('DELETE FROM binhluan')
    conn.commit()
def add_comment_if_not_exists(articleId, articleLink, text, role):
    # Kiểm tra xem articleId hoặc articleLink đã tồn tại chưa
    if articleId is not None:
        articleId = f"{articleId}_{role}"
    if articleLink is not None:
        articleLink = f"{articleLink}_{role}"
    c.execute('''
            SELECT text FROM binhluan
            WHERE articleId = ? OR articleLink = ?
        ''', (articleId, articleLink))

    result = c.fetchone()

    if result is None:
        # roles = find_by_id(role)
        # prompt = roles["promptComment"]
        prompt = load_phongcach(text,role)
        text = getbinhluan(text, prompt)    
        # Nếu chưa tồn tại, thêm mới
        c.execute('''
                INSERT INTO binhluan (articleId, articleLink, text)
                VALUES (?, ?, ?)
            ''', (articleId, articleLink, text))
        conn.commit()
        return text
    else:
        # Nếu đã tồn tại, trả về text hiện có
        existing_text = result[0]
        return existing_text
def add_comment_if_not_exists_8am(articleId, articleLink, text, role):
    if articleId is not None:
        articleId = f"{articleId}_{role}"
    if articleLink is not None:
        articleLink = f"{articleLink}_{role}"
    c.execute('''
              SELECT text FROM binhluan
              WHERE articleId = ? OR articleLink = ?
              ''', (articleId, articleLink))
    result = c.fetchone()
    if result is None:
        roles = find_by_id(role)
        prompt = load_phongcach(text,role)
        text = getbinhluan(text, prompt)    
        c.execute('''
                  INSERT INTO binhluan (articleId, articleLink, text)
                  VALUES (?, ?, ?)
                  ''', (articleId, articleLink, text))
        conn.commit()
        return text
    else:
        existing_text = result[0]
        return existing_text

def id_exists(id):
    c.execute('SELECT 1 FROM ids WHERE id=?', (id,))
    return c.fetchone() is not None

def add_id(id):
    c.execute('INSERT OR IGNORE INTO ids (id) VALUES (?)', (id,))
    conn.commit()
def add_question(id_post, question_1, question_2, question_3):
    c.execute('''
            INSERT INTO next_question (id_post, question_1, question_2, question_3)
            VALUES (?, ?, ?, ?)
        ''', (id_post, question_1, question_2, question_3))
    conn.commit()
def get_question(id_post):
    c.execute('''
            SELECT question_1, question_2, question_3
            FROM next_question
            WHERE id_post = ?
        ''', (id_post,))
    return c.fetchone()
def delete_question(id_post):
    c.execute('''
            DELETE FROM next_question
            WHERE id_post = ?
        ''', (id_post,))
    conn.commit()
    
