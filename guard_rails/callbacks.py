from google.adk.agents.llm_agent import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from .runner import guardrail_runner

async def before_model_callback(callback_context: CallbackContext,
                                 llm_request: LlmRequest) -> LlmResponse | None:
    user_text = None
    if llm_request.contents:
        last_content = llm_request.contents[-1]
        # Check if it's a user message
        if last_content.role == "user" and last_content.parts and hasattr(last_content.parts[0], 'text'):
            user_text = last_content.parts[0].text

    if user_text:
        # Re-wrap for the runner
        user_content = types.Content(role='user', parts=[types.Part(text=user_text)])
        
        state = callback_context.state
        user_id = str(state.get("user_id", "unknown_user"))
        session_id = state.get("session_id", "unknown_session")
        
        final_guardrail_response = "false" # Default to allow

        # Run the guardrail check
        async for event in guardrail_runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=user_content
            ):
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text is not None:
                        final_guardrail_response = part.text
                        break
                break
        
        if final_guardrail_response == "true":
            # Guardrail triggered, block main LLM
            print(f"!!! GUARDRAIL TRIGGERED: Blocking input '{user_text}' !!!")
            return LlmResponse(
                content=types.Content(
                    parts=[types.Part(text="I cannot fulfill this request as it violates our safety or brand guidelines (Competitor mention or Unsafe content).")],
                    role="model"
                )
            )
    # No guardrail triggered
    return None
