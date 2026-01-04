from google.adk import Agent
from google.adk.tools import load_artifacts
from google.adk.tools.tool_context import ToolContext
from google.genai import Client
from google.genai import types
from dotenv import load_dotenv
from .tools import get_brand_persona
from . import prompt
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = Client(api_key=GOOGLE_API_KEY)

async def create_image(prompt: str, tool_context: 'ToolContext'):
    """Generates a brand new image from a text description."""
    return await _process_image_request(prompt, None, tool_context)

async def edit_image(instruction: str, tool_context: 'ToolContext'):
    """Edits the most recently generated image based on new instructions."""
    image = None
    try:
        available_files = await tool_context.list_artifacts()
        if available_files:
            # Load the last image to use as a reference for editing
            image = await tool_context.load_artifact(available_files[-1])
        else:
            return {'status': 'failed', 'detail': 'No image exists to edit. Use create_image first.'}
    except Exception as e:
        return {'status': 'error', 'detail': str(e)}
    
    return await _process_image_request(instruction, image, tool_context)

async def _process_image_request(prompt: str, reference_image, tool_context: 'ToolContext'):
    """Internal helper to handle the API call and artifact saving."""
    contents = [prompt]
    if reference_image:
        contents.append(reference_image)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview", # cheap
        contents=contents,
    )
    
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            image_bytes = part.inline_data.data
            filename = 'image_edited.png' if reference_image else 'image_new.png'
            await tool_context.save_artifact(
                filename,
                types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
            )
            return {
                'status': 'success',
                'detail': f'Image processed and saved as {filename}',
                'filename': filename,
            }
    return {'status': 'failed', 'detail': 'Model did not return image data.'}

# Agent Configuration
visualist_agent = Agent(
    model='gemini-3-flash-preview',
    name='visualist_agent',
    description="Creates and edits on-brand marketing visuals and provides strong image generation prompts.",
    instruction=prompt.VISUALIST_AGENT_PROMPT,
    tools=[create_image, edit_image, load_artifacts, get_brand_persona],
)

# Backwards-compatible alias (in case other modules still import root_agent)
root_agent = visualist_agent
