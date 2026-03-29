import asyncio
import logging
from groq import Groq
from app.config import config
from app.utils.prompts import PROMPTS

logger = logging.getLogger(__name__)

async def get_translation(text: str, mode: str, target_lang: str) -> str:
   
    api_key = config.groq_api_key.get_secret_value()
    client = Groq(api_key=api_key)
    
    model_name = "llama-3.3-70b-versatile"
    
    style_instruction = PROMPTS.get(mode, PROMPTS["ordinary"])
    
    current_temperature = 0.8 if mode == "friendly" else 0.3
    
    system_prompt = (
        f"{style_instruction}\n"
        f"Target language: {target_lang}.\n"
        "OUTPUT: Only the translated text, nothing else."
    )
    
    try:
        loop = asyncio.get_event_loop()
        
        def run_groq():
            return client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user","content": text}
                ],
                model=model_name,
                temperature=current_temperature,
            )

        chat_completion = await loop.run_in_executor(None, run_groq)
        
        if chat_completion and chat_completion.choices:
            return chat_completion.choices[0].message.content
        return "⚠️ Empty response."

    except Exception as e:
        logger.error(f"GROQ translation failed: {e}", exc_info=True)
        return "Sorry, translation service error."