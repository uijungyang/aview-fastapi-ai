import wave
import sys

# SetEndpointerMode, SetEndpointerDelays
from vosk import Model, KaldiRecognizer, SetLogLevel

# Vosk에서 endpointer와 관련하여 제어할 수 있는 대체 방법
# import recognizer

# 프레임 단위로 음성 유무를 판단하여 endpoint 조절이 가능
# import webrtcvad


# you can set log level to -1 to disable debug messages
SetLogLevel(0)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

model = Model("vosk-model-small-ko-0.22")

# You can also init model by name or with a folder path
# model = Model(model_name="vosl-model-en-us-0.21")
# model = Model("models/en")

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)
rec.SetPartialWords(True)
# rec.SetEndpointerMode(EndpointerMode.VERY_LONG)


while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Reset())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

# rec.SetEndpointerDelays(0.5, 0.3, 10.0)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())