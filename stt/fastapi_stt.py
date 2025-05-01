from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from vosk import Model, KaldiRecognizer

import wave
import json
import os
import shutil
import requests
from pydantic import BaseModel


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # 실제 배포 시 Vue 앱 주소로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vosk 모델 경로 지정
MODEL_PATH = "models/vosk-model-small-ko-0.22"
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"❌ 모델 경로가 존재하지 않습니다: {MODEL_PATH}")
model = Model(MODEL_PATH)


@app.post("/stt/")
async def speech_to_text(audio: UploadFile=File(...)):
    audio_path = "temp.wav"

    try:
        # 파일 저장
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # wav 파일 열기
        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
            raise HTTPException(status_code=400,
                                detail="지원되지 않는 오디오 형식입니다. (mono 16-bit PCM")

        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)

        full_result = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                full_result += rec.Result()

        full_result += rec.FinalResult()

        result_josn = json.loads(full_result)
        text = result_josn.get("text", "")

        print(f"🎙️ 인식된 텍스트: {text}")

        # Backend 서버로 전송
        try:
            response = requests.post("http://localhost:3000/save_stt/", json={"text": text})
            print("✅ 백엔드로 STT 결과 전송 완료:", response.status_code)
        except requests.RequestException as e:
            print("⚠️ 백엔드로 STT 결과 전송 실패:", e)

        return {"text": text}

    except Exception as e:
        print("❌ STT 처리 중 오류:", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # 임시 파일 삭제
        if os.path.exists(audio_path):
            os.remove(audio_path)