import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel


SAMPLE_RATE = 16000

SetLogLevel(0)

model = Model("vosk-model-small-ko-0.22")
rec = KaldiRecognizer(model, SAMPLE_RATE)

with subprocess.Popen(
    [
        "ffmpeg", "-loglevel", "quiet", "-i",
        sys.argv[1],
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-",
    ],
    stdout=subprocess.PIPE
) as process:
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.Result())

    print(rec.FinalResult())