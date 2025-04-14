import wave
import sys

from vosk import KaldiRecognizer

# vosk의 Processor 대체 방안을 검토 중

# proc = KaldiRecognizer.AcceptWaveform("ru_itn_tagger.tst", "ru_itn_verbalizer.fst")
# print(proc.Result("у нас десять яблок"))
# print(proc.Result("у нас десять яблок и десять миллилитров воды точка"))
# print(proc.Result("мы пришли в восемь часов пять минут"))