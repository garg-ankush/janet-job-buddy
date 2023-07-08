import whisper
model = whisper.load_model("base")


def transcribe_audio(filename):
    result = model.transcribe(f"{filename}.wav")
    return result["text"]
