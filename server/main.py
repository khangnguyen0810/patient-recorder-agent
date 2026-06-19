from utils.audio_processing import transcribe_medical_audio
import asyncio
from dotenv import load_dotenv
from utils.agent import clinical_scribe_agent, session_service
from google.adk.runners import Runner
from google.genai import types
import json

load_dotenv()

async def main():
    try:
        await session_service.delete_session(
            app_name="clinical_scribe_app",
            user_id="doctor_user_123",
            session_id="clinic_visit_001"
        )
    except Exception:
        pass

    await session_service.create_session(
        app_name="clinical_scribe_app",
        user_id="doctor_user_123",
        session_id="clinic_visit_001"
    )

    runner = Runner(
        session_service=session_service,
        app_name="clinical_scribe_app",
        agent=clinical_scribe_agent
    )

    audio_input = "cavern_escape.wav"
    raw_transcript = transcribe_medical_audio(audio_input)

    print("\n[*] Audio transcription complete. Handing payload to Google ADK...")
    print(raw_transcript)

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=f"Here is the recorded medical conversation:\n\n{raw_transcript}")]
    )

    event_stream = runner.run_async(
        user_id="doctor_user_123",
        session_id="clinic_visit_001",
        new_message=user_message
    )

    full_response = ""
    async for event in event_stream:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    full_response += part.text

    print("\n[*] Gemini Response (JSON):")
    try:
        parsed = json.loads(full_response)
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"Could not parse as JSON: {e}")

if __name__ == "__main__":
    asyncio.run(main())