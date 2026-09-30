from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import edge_tts
import io

app = FastAPI()

@app.get("/tts")
async def text_to_speech(text: str, voice: str = "hi-IN-SwaraNeural"):
    # edge-tts लाइब्रेरी की मदद से Microsoft Edge से लाइव वॉयस स्ट्रीम जनरेट करना
    communicate = edge_tts.Communicate(text, voice)
    audio_stream = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_stream.write(chunk["data"])
            
    audio_stream.seek(0)
    # सीधे ऑडियो बाइट्स को ESP32-S3 की तरफ लाइव स्ट्रीम करना
    return StreamingResponse(audio_stream, media_type="audio/mpeg")
