import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
import json
import os
import shutil
import ollama
import time
import re
from pydub import AudioSegment

from rag_engine import get_context_from_pdf
from voice_engine import generate_voice
from image_engine import generate_image
from video_engine import create_video_segment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persona to Voice Mapping
PERSONA_MAP = {
    "expert-skeptic": {
        "Optimist": "en-US-GuyNeural", 
        "Critic": "en-GB-RyanNeural"
    },
    "storyteller-scientist": {
        "Optimist": "en-US-JennyNeural", 
        "Critic": "en-IN-PrabhatNeural"
    },
    "analyst-creative": {
        "Optimist": "en-AU-NatashaNeural",
        "Critic": "en-US-ChristopherNeural"
    }
}

@app.post("/generate")
async def generate_podcast(
    file: UploadFile = File(...), 
    topic: str = Form(...), 
    persona: str = Form(...) 
):
    async def event_generator():
        try:
            if not os.path.exists("data"): os.makedirs("data")
            
            # 1. UPLOAD
            yield f"data: {json.dumps({'step': 'uploading', 'msg': 'Saving PDF to Vector Store...'})}\n\n"
            pdf_path = os.path.join("data", file.filename)
            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 2. RAG
            yield f"data: {json.dumps({'step': 'vectorizing', 'msg': 'Performing Semantic Retrieval...'})}\n\n"
            context = get_context_from_pdf(pdf_path, topic)
            
            # 3. LLM (Deep Dive Prompt with Randomness)
            yield f"data: {json.dumps({'step': 'thinking', 'msg': 'Llama 3 is composing a fresh 2-minute deep dive...'})}\n\n"
            
            prompt = f"""
            SYSTEM: You are a professional podcast producer.
            CONTEXT: {context}
            TOPIC: {topic}
            TASK: Write a lengthy, detailed 10-line technical debate between an 'Optimist' and a 'Critic'.
            The dialogue should be intellectual, debating specific nuances of the context provided.
            Line 1: Optimist
            Line 2: Critic
            ... (exactly 10 lines total)
            FORMAT: Speaker: Text. 
            STRICT RULE: Do not include intros, outros, or stage directions.
            """

            # UPDATED: Added 'options' for randomness and context
            response_data = ollama.generate(
                model='llama3', 
                prompt=prompt,
                options={
                    "temperature": 0.8,    # Increases creativity/length
                    "num_predict": 1000,   # Ensures it doesn't cut off early
                    "top_p": 0.9,          # Diversity of word choice
                    "seed": int(time.time()) # Forces a fresh response every time
                }
            )
            response = response_data['response']

            # 4. RENDERING
            yield f"data: {json.dumps({'step': 'rendering', 'msg': 'Synthesizing Neural Dialogue...'})}\n\n"
            
            selected_voices = PERSONA_MAP.get(persona, PERSONA_MAP["expert-skeptic"])
            lines = [l for l in response.strip().split('\n') if ":" in l]
            combined_audio = AudioSegment.empty()
            
            for i, line in enumerate(lines):
                # SPLIT & STRIP: Remove the 'Optimist:' label from the audio text
                parts = line.split(":", 1)
                if len(parts) < 2: continue
                
                speaker_label = parts[0].strip()
                raw_text = parts[1].strip()
                
                # CLEANING: Remove stage directions like (laughs) or [thinks]
                clean_text = re.sub(r'[\(\[].*?[\)\]]', '', raw_text)
                
                # Map labels to the specific Persona Voice
                voice_id = selected_voices.get(speaker_label, "en-US-AriaNeural")
                
                temp_name = f"temp_{i}.mp3"
                await generate_voice(clean_text, voice_id, temp_name)
                
                if os.path.exists(temp_name) and os.path.getsize(temp_name) > 100:
                    combined_audio += AudioSegment.from_mp3(temp_name)
                    os.remove(temp_name)

            combined_audio.export("podcast_audio.mp3", format="mp3")

            yield f"data: {json.dumps({'step': 'rendering', 'msg': 'Imaging the Scene...'})}\n\n"
            generate_image(f"Cinematic futuristic lab, {topic}, hyperrealistic, 8k", "podcast_visual.png")
            
            yield f"data: {json.dumps({'step': 'rendering', 'msg': 'Assembling Full Render...'})}\n\n"
            
            timestamp = int(time.time())
            final_video_name = f"output_{timestamp}.mp4"
            create_video_segment("podcast_visual.png", "podcast_audio.mp3", final_video_name)
            
            # 5. COMPLETE
            video_url = f"http://127.0.0.1:8000/video/{final_video_name}"
            yield f"data: {json.dumps({'step': 'complete', 'msg': 'Deep Dive Production Complete!', 'video_url': video_url})}\n\n"

        except Exception as e:
            print(f"ERROR: {e}")
            yield f"data: {json.dumps({'step': 'error', 'msg': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/video/{video_name}")
async def get_video(video_name: str):
    return FileResponse(video_name, media_type="video/mp4")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)