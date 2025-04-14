import json

from vosk import Model, KaldiRecognizer

# set model's language mode to korean model
model = Model("vosk-model-spk-0.4")
rec = KaldiRecognizer(model, 8000)

# Response
res = json.loads(rec.FinalResult())
print(res)