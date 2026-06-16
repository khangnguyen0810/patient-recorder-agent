# utils/agent.py
from utils.extract_instruction import extract_instruction
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
import os
import sys

prompt_folder = os.path.abspath("../prompts")
sys.path.insert(0, prompt_folder)


from utils.schemas_demo import SOAPNoteSchema 

clinical_scribe_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='clinical_scribe_agent',
    description='Medical Audio Extraction Agent assists doctors in creating automated patient records.',
    instruction=extract_instruction("prompts/prompt_v1.yaml"),
    output_schema=SOAPNoteSchema, 
    output_key="extracted_soap_note"
)

session_service = InMemorySessionService()