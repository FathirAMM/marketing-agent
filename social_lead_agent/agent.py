from google.adk.agents import LlmAgent
from dotenv import load_dotenv
from . import prompt
from .tools import get_brand_persona
load_dotenv()

social_lead_agent = LlmAgent(
    name="social_lead_agent",
    model="gemini-3-flash-preview",
    description=(
        "Generates brand-aligned social media content across platforms. "
        "Uses retrieved brand personas to ensure consistent messaging."
    ),
    instruction=prompt.SOCIAL_LEAD_AGENT_PROMPT,
    tools=[get_brand_persona]
)

# root_agent = social_lead_agent