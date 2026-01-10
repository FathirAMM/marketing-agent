from typing import Any, AsyncGenerator

class GuardrailEvent:
    def __init__(self, content):
        self.content = content

    def is_final_response(self):
        return True

class SimpleGuardrailRunner:
    """
    A simple mockup of a guardrail runner.
    In a real system, this might call a separate Classification LLM.
    """
    async def run_async(self, user_id: str, session_id: str, new_message: Any) -> AsyncGenerator[Any, None]:
        # Extract text from the message object
        user_text = ""
        if hasattr(new_message, 'parts'):
            for part in new_message.parts:
                if hasattr(part, 'text'):
                    user_text += part.text

        user_text = user_text.lower()
        
        # --- SAFETY POLICIES ---
        # 1. Competitor mentions
        if "lipton" in user_text or "twinings" in user_text:
             # Create a mock response object structure similar to what the callback expects
            class MockPart:
                text = "true"
            class MockContent:
                parts = [MockPart()]
            
            yield GuardrailEvent(MockContent())
            return

        # 2. Offensive language (Simple list)
        unsafe_words = ["hate", "stupid", "idiot"]
        if any(word in user_text for word in unsafe_words):
             class MockPart:
                text = "true"
             class MockContent:
                parts = [MockPart()]
            
             yield GuardrailEvent(MockContent())
             return

        # Default: Safe
        class MockPart:
            text = "false"
        class MockContent:
            parts = [MockPart()]
        yield GuardrailEvent(MockContent())

guardrail_runner = SimpleGuardrailRunner()
