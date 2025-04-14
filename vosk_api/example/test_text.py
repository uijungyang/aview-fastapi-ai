import sys
import json

from vosk import Model, KaldiRecognizer


model = Model("vosk-model-small-ko-0.22")

# Large vocabulary free form recognition
rec = KaldiRecognizer(model, 16000)

# You can also specify the possible word list
# rec = KaldiRecognizer(model, 16000, "zero oh one two three four five six ...")

with open(sys.argv[1], "rb") as wf:
    wf.read(44) # skip header

    while True:
        data = wf.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            print(res["text"])

    res = json.loads(rec.FinalResult())
    print(res["text"])