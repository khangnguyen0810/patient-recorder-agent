import os
import sys
import tempfile
import mimetypes
from typing import Optional

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest, LlmResponse

prompt_folder = os.path.abspath("../prompts")
sys.path.insert(0, prompt_folder)

from utils.audio_processing import transcribe_medical_audio
from utils.extract_instruction import extract_instruction
from utils.schemas_demo import SOAPNoteSchema

mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('audio/wav', '.wav')
mimetypes.add_type('audio/x-wav', '.wav')
mimetypes.add_type('audio/ogg', '.ogg')
mimetypes.add_type('audio/m4a', '.m4a')
mimetypes.add_type('audio/x-m4a', '.m4a')
mimetypes.add_type('audio/mp4', '.mp4')


async def transcriber_combined_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    llm_request.config.system_instruction = (
        "You are a precise, verbatim text transmission assistant. "
        "Your sole task is to repeat the provided text transcript exactly word-for-word. "
        "Do not summarize, do not omit any sentences, do not correct grammar or stutters, "
        "and do not add any commentary. Output only the verbatim transcript."
    )

    if llm_request.contents:
        llm_request.contents = [llm_request.contents[-1]]

        for content in llm_request.contents:
            if not content.parts:
                continue
            for part in content.parts:
                if part.inline_data and part.inline_data.mime_type and \
                   part.inline_data.mime_type.startswith("audio/"):

                    detected_mime = part.inline_data.mime_type
                    computed_suffix = mimetypes.guess_extension(detected_mime) or ".wav"
                    audio_bytes = part.inline_data.data

                    with tempfile.NamedTemporaryFile(delete=False, suffix=computed_suffix) as tmp:
                        tmp.write(audio_bytes)
                        tmp_path = tmp.name

                    try:
                        print(f"\n[*] Intercepted Web UI audio ({detected_mime} -> {computed_suffix}).")
                        print("[*] Transcribing via OpenAI Whisper...")
                        transcript = transcribe_medical_audio(tmp_path)
                        print("[*] Transcription complete. Injecting text into Gemini payload.")

                        part.inline_data = None
                        part.text = f"Here is the transcribed medical conversation:\n\n{transcript}"
                    finally:
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)

    return None


async def clean_system_instruction_modifier(
    callback_context: CallbackContext,
    llm_request: LlmRequest
) -> Optional[LlmResponse]:
    llm_request.config.system_instruction = extract_instruction("prompts/prompt_v1.yaml")
    
    if llm_request.contents:
        llm_request.contents = [llm_request.contents[-1]]
    
    callback_context.state["extracted_soap_note"] = None
    
    return None


transcriber_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='transcriber_agent',
    description='Transcribes raw audio payloads and streams text back to the session.',
    before_model_callback=transcriber_combined_callback
)

clinical_scribe_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='clinical_scribe_agent',
    description='Medical Audio Extraction Agent: builds structured SOAP notes from transcripts.',
    output_schema=SOAPNoteSchema,
    output_key="extracted_soap_note",
    before_model_callback=clean_system_instruction_modifier
)

web_ui_agent = SequentialAgent(
    name="medical_scribe_team",
    sub_agents=[transcriber_agent, clinical_scribe_agent],    
    description=(                                              
        "Transcribes raw audio via Whisper, then extracts a structured SOAP note."
    )
)

root_agent = web_ui_agent

session_service = InMemorySessionService()