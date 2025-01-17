import numpy as np 
import os, json
from llama_index.llms.groq import Groq 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding 
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from dotenv import load_dotenv



print("...")
os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

# Set GROQ_API_KEY = "your api key" in the .env environment and load it below.
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

print(f"GROQ API Key: {GROQ_API_KEY}")


models = [
    # 'llama-3.1-405b-reasoning'
    'llama-3.1-70b-versatile'
    'llama-3.1-80b-instant'
    'mixtral-8x7b-32768'
    'claude-3.5-sonnet'
    'gemini-1.5-flash'
    'gemini-1.5-pro'
]


"""
In llama-index, LLM and embed_model can be set at any of 2 levels:
    - global seting with settings (both llm and embed_model)
    - index level (embed_model only)
    - query engine level (llm only)
"""


Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

# Settings.context_windowllm = Groq(
#     models[0],
#     api_key=GROQ_API_KEY,
#     temperature=0.1
# )

def upload_doc(dir):
    documents = SimpleDirectoryReader(dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index
# Index the document using vector store document


def qa_engine(query: str, index, model=models[0]):

    llm = Groq(model, api_key = GROQ_API_KEY, temperature = 0.1)
    query_engine = index.as_query_engine(llm=llm)
    response = query_engine.query(query)
    return response

if __name__ == "__main__":
    index = upload_doc("./data")
    query = input("Ask me anything: ")
    model = input("Enter model code: ")
    response = qa_engine(query, index, model)
    print(response)