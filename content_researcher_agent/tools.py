# tools.py
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

# 1. Load Env & Initialize Connections
load_dotenv()

qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"), 
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=60.0    
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name="dilmah_wishes",
    embedding=embeddings,
)

# 2. Define the Tool Function
def search_knowledge_base(query: str) -> str:
    """Searches the internal knowledge base to find specific information for Retrieval-Augmented Generation (RAG).

    This tool queries a vector database to retrieve contextually relevant data. 
    Use this to augment generative model responses with specific, factual information 
    from the knowledge base.

    Args:
        query: A specific and detailed search query to find relevant information. 
               Natural language questions or keywords are effective. For example: 
               "What are the key themes in recent marketing campaigns?"
    """
    try:
        results = vector_store.similarity_search(query, k=2)
        
        if not results:
            return "No relevant information found in the knowledge base."

        response_text = "Found the following info in the Knowledge Base:\n"
        
        for i, doc in enumerate(results, 1):
            metadata_dump = str(doc.metadata)
            
            response_text += f"\n-- Result {i} --\n"
            response_text += f"Content: {doc.page_content}\n"
            response_text += f"Metadata: {metadata_dump}\n"
    
        return response_text

    except Exception as e:
        return f"Error connecting to knowledge base: {str(e)}"


