import os
import sys
import tempfile
import mimetypes  # <--- Built-in module to resolve extensions
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

# Set up prompt paths
prompt_folder = os.path.abspath("../prompts")
sys.path.insert(0, prompt_folder)

from utils.audio_processing import transcribe_medical_audio
from utils.extract_instruction import extract_instruction
from utils.schemas_demo import SOAPNoteSchema 

# --- Explicitly register common audio MIME types to guarantee proper extensions ---
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('audio/wav', '.wav')
mimetypes.add_type('audio/x-wav', '.wav')
mimetypes.add_type('audio/ogg', '.ogg')
mimetypes.add_type('audio/m4a', '.m4a')
mimetypes.add_type('audio/x-m4a', '.m4a')
mimetypes.add_type('audio/mp4', '.mp4')


async def clinical_scribe_combined_callback(
    callback_context: CallbackContext, 
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Unified callback handling both system prompt initialization 
    and dynamic OpenAI Whisper audio conversion based on incoming MIME type.
    """
    llm_request.config.system_instruction = extract_instruction("prompts/prompt_v1.yaml")
    
    if llm_request.contents:
        for content in llm_request.contents:
            if not content.parts:
                continue
            for part in content.parts:
                if part.inline_data and part.inline_data.mime_type and part.inline_data.mime_type.startswith("audio/"):
                    
                    detected_mime = part.inline_data.mime_type
                    computed_suffix = mimetypes.guess_extension(detected_mime) or ".wav"
                    
                    audio_bytes = part.inline_data.data
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=computed_suffix) as temp_audio:
                        temp_audio.write(audio_bytes)
                        temp_audio_path = temp_audio.name
                    
                    try:
                        print(f"\n[*] Intercepted Web UI audio ({detected_mime} -> {computed_suffix}).")
                        print(f"[*] Transcribing via OpenAI Whisper...")
                        text_transcript = transcribe_medical_audio(temp_audio_path)
                        print(f"[*] Whisper Transcription complete! Ijecting text into Gemini payload.")
                        
                        part.inline_data = None
                        part.text = f"Here is the transcribed medical conversation context:\n\n{text_transcript}"
                        
                    finally:
                        if os.path.exists(temp_audio_path):
                            os.remove(temp_audio_path)
                            
    return None


clinical_scribe_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='clinical_scribe_agent',
    description='Medical Audio Extraction Agent assists doctors in creating automated patient records.',
    output_schema=SOAPNoteSchema, 
    output_key="extracted_soap_note",
    before_model_callback=clinical_scribe_combined_callback
)

session_service = InMemorySessionService()
root_agent = clinical_scribe_agent