from utils.schemas import AudioMetadata
import os
from typing import Tuple
from faster_whisper import WhisperModel
import torch

def transcribe_medical_audio(audio_path: str) -> Tuple[str, AudioMetadata]:
    print(f"[*] Local Whisper processing: {audio_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"

    model = WhisperModel("tiny", device=device, compute_type=compute_type)

    segments, info = model.transcribe(audio_path, beam_size=5)
    transcript = "".join(segment.text for segment in segments)
    
    metadata = AudioMetadata(
        audio_file_ref=os.path.basename(audio_path),
        duration_sec=round(info.duration, 2) if info.duration else None,
        language=info.language,
        speaker_count=None,        # Requires an external diarization pipeline (e.g., PyAnnote)
        diarization_quality=None   # Requires an external diarization pipeline
    )
    
    return transcript, metadata