import whisper
import sys

model = whisper.load_model("tiny")

audio_file = sys.argv[1]
result = model.transcribe(audio_file)
text = result["text"]

with open(audio_file.rsplit(".",1)[0]+".txt", "w", encoding="utf-8") as f:
    f.write(text)

print(text)
