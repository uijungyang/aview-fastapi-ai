import subprocess
import sys

from vosk import Model, KaldiRecognizer, SetLogLevel


SAMPLE_RATE = 16000

SetLogLevel(-1)

model = Model("vosk-model-small-ko-0.22")
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

with subprocess.Popen(
    [
        "ffmpeg", "-loglevel", "quiet", "-i",
        sys.argv[1],
        "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"
    ],
    stdout=subprocess.PIPE
).stdout as stream:

    print(rec.SrtResult(stream))