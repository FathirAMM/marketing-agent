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


# 3. New Tool: Web Search
import requests

def search_web(query: str) -> str:
    """Performs a web search using SerpApi to find external information.
    
    Use this tool when the internal knowledge base does not contain the answer,
    or when you need up-to-date real-world information.

    Args:
        query: The search string.
    """
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        return "Error: SERP_API_KEY not found in environment variables."

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google"
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = ""
        
        # organic results
        if "organic_results" in data:
            for item in data["organic_results"][:3]:
                title = item.get("title", "No Title")
                link = item.get("link", "No Link")
                snippet = item.get("snippet", "No Snippet")
                results += f"Title: {title}\nLink: {link}\nSnippet: {snippet}\n\n"
        
        if not results:
            return "No web search results found."
            
        return results

    except Exception as e:
        return f"Error performing web search: {str(e)}"



