import os
import sqlite3
import re
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai

# Load .env file manually without extra dependencies
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    question: str

def get_db_schema():
    conn = sqlite3.connect('local_shop.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    schema = ""
    for table_name in tables:
        table_name = table_name[0]
        if table_name == 'sqlite_sequence':
            continue
        c.execute(f"PRAGMA table_info({table_name})")
        columns = c.fetchall()
        schema += f"Table: {table_name}\nColumns:\n"
        for col in columns:
            schema += f" - {col[1]} ({col[2]})\n"
        schema += "\n"
    
    conn.close()
    return schema

def is_safe_query(query: str) -> bool:
    # Basic safety check: only allow SELECT queries, forbid modifying operations
    q = query.upper().strip()
    if not q.startswith("SELECT"):
        return False
    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "EXEC", "TRUNCATE"]
    for word in forbidden:
        if re.search(r'\b' + word + r'\b', q):
            return False
    return True

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.get("/schema")
def get_schema_json():
    conn = sqlite3.connect('local_shop.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    schema = {}
    for table_name in tables:
        tname = table_name[0]
        if tname == 'sqlite_sequence':
            continue
        c.execute(f"PRAGMA table_info({tname})")
        columns = [{"name": col[1], "type": col[2]} for col in c.fetchall()]
        schema[tname] = columns
    
    conn.close()
    return schema

@app.post("/ask")
def ask_question(req: QueryRequest):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    schema = get_db_schema()
    
    prompt = f"""
You are an expert SQL assistant. Given the following SQLite database schema, 
translate the user's natural language question into a valid SQL query.
Return ONLY the raw SQL query, with no markdown formatting, no explanation, and no backticks.
The query must be a valid SQLite SELECT statement.

Schema:
{schema}

Question: {req.question}
"""
    
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        response = model.generate_content(prompt)
        sql_query = response.text.strip()
        
        # Strip markdown if LLM still returned it
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        sql_query = sql_query.strip()

        if not is_safe_query(sql_query):
            raise HTTPException(status_code=400, detail="Generated query is not a safe SELECT statement.")
        
        conn = sqlite3.connect('local_shop.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(sql_query)
        rows = c.fetchall()
        
        # Get column names
        columns = [description[0] for description in c.description] if c.description else []
        
        results = []
        for row in rows:
            results.append(dict(row))
            
        conn.close()
        
        return {
            "query": sql_query,
            "columns": columns,
            "data": results
        }
        
    except Exception as e:
        # Log to process_log.txt for demonstration
        with open("process_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[Error] /ask endpoint: {str(e)}\n")
        raise HTTPException(status_code=500, detail=str(e))
