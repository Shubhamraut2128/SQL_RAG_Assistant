from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from sqlalchemy import create_engine
import pandas as pd
import re

from config import GROQ_API_KEY, DB_URI
from prompt_template import SQL_PROMPT


# ⭐ SQL CLEANER FUNCTION
def extract_sql(query):
    match = re.search(r"```sql(.*?)```", query, re.DOTALL)
    if match:
        return match.group(1).strip()
    return query.strip()


class SQLRAGAgent:

    def __init__(self):

        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model="llama-3.1-8b-instant"
        )

        # ⭐ IMPORTANT FIX HERE
        self.engine = create_engine(DB_URI)

        print("✅ Connected DB:", DB_URI)

        # Simple Chat Memory
        self.chat_history = []

        docs = [
            Document(page_content="customers table contains customer details"),
            Document(page_content="orders table contains purchase transactions"),
            Document(page_content="products table contains product price details")
        ]

        embedding = HuggingFaceEmbeddings()
        self.vectordb = FAISS.from_documents(docs, embedding)

    def ask(self, question):

        # Retrieve context
        context_docs = self.vectordb.similarity_search(question)
        context_text = "\n".join([doc.page_content for doc in context_docs])

        history_text = "\n".join(self.chat_history)

        final_prompt = f"""
Schema Context:
{context_text}

Previous Conversation:
{history_text}

{SQL_PROMPT.format(question=question)}
"""

        # Generate SQL
        sql_query = self.llm.invoke(final_prompt).content

        # Clean SQL
        clean_query = extract_sql(sql_query)

        # Execute SQL
        try:
            df = pd.read_sql(clean_query, self.engine)

            if df.empty:
                answer = "No Data Found"
            else:
                answer = df.to_string(index=False)

        except Exception as e:
            answer = f"SQL Error: {str(e)}"

        # Save Memory
        self.chat_history.append(f"User: {question}")
        self.chat_history.append(f"SQL: {clean_query}")
        self.chat_history.append(f"Answer: {answer}")

        return clean_query, answer