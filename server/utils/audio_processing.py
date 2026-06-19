def transcribe_medical_audio(audio_path: str) -> str:
    from faster_whisper import WhisperModel
    import torch

    print(f"[*] Local Whisper processing: {audio_path}")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"

    model = WhisperModel("tiny", device=device, compute_type=compute_type)

    segments, _ = model.transcribe(audio_path, beam_size=5)
    return "".join(segment.text for segment in segments)