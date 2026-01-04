from google.adk.agents import LlmAgent

import os
from dotenv import load_dotenv
from . import prompt

from google.adk.tools.agent_tool import AgentTool

from social_lead_agent.agent import social_lead_agent
from visualist_agent.agent import visualist_agent
from content_researcher_agent.agent import content_researcher_agent
from .tools import get_brand_persona


load_dotenv()

marketing_coordinator = LlmAgent(
    name="marketing_coordinator",
    model="gemini-3-flash-preview",
    description=(
        "marketing coordinator agent"
    ),
    instruction=prompt.MARKETING_COORDINATOR_PROMPT,
    tools=[
        get_brand_persona,
        AgentTool(content_researcher_agent),
        AgentTool(social_lead_agent),
        AgentTool(visualist_agent),
        ]

)


root_agent = marketing_coordinator
