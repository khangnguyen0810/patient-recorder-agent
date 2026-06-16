def transcribe_medical_audio(audio_path: str) -> str:
    from transformers import pipeline
    import torch

    print(f"[*] Local Whisper processing: {audio_path}")
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    pipe = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-tiny",
        chunk_length_s=30,
        device=device
    )

    result = pipe(audio_path)
    return result["text"]