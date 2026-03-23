from fastapi import FastAPI
from rag_sql_agent import SQLRAGAgent

app = FastAPI()

agent = SQLRAGAgent()

@app.get("/ask")
def ask(question:str):

    sql, result = agent.ask(question)

    return {
        "sql": sql,
        "result": result
    }

    