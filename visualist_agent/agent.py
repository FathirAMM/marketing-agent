from google.adk import Agent
from google.adk.tools import load_artifacts
from .tools import get_brand_persona, create_image, edit_image
from . import prompt


# Agent Configuration
visualist_agent = Agent(
    model='gemini-2.5-flash',
    name='visualist_agent',
    description="Creates and edits brand-aligned marketing visuals",
    instruction=prompt.VISUALIST_AGENT_PROMPT,
    tools=[create_image, edit_image, load_artifacts, get_brand_persona],
)

# root_agent = visualist_agent