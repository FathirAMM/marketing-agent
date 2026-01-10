from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from . import prompt
from .tools import search_knowledge_base
 
load_dotenv()

content_researcher_agent = LlmAgent(
    name="content_researcher_agent",
    model="gemini-3-flash-preview",
    description=(
        "Retrieves factual information, specific anecdotes, and strategic "
        "insights from the company's internal knowledge base (Annual Reports, "
        "Videos, Website). acts as the factual grounding for campaigns."
    ),
    instruction=prompt.CONTENT_RESEARCHER_AGENT_PROMPT,
    tools=[search_knowledge_base]
)

root_agent = content_researcher_agent