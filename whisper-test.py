from transformers import pipeline

asr = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-large-v3-turbo",
    device=0
)

result = asr("https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac")
print(result)