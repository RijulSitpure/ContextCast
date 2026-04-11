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
            yield f"data: {json.dumps({'step': 'uploading', 'msg': 'Saving PDF...'})}\n\n"
            pdf_path = os.path.join("data", file.filename)
            with open(pdf_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # 2. RAG
            yield f"data: {json.dumps({'step': 'vectorizing', 'msg': 'Retrieving Context...'})}\n\n"
            context = get_context_from_pdf(pdf_path, topic)
            
            # 3. LLM
            yield f"data: {json.dumps({'step': 'thinking', 'msg': 'Generating 2-minute script...'})}\n\n"
            
            prompt = f"""
            SYSTEM: You are a professional podcast writer.
            CONTEXT: {context}
            TOPIC: {topic}
            TASK: Write a 10-line debate between 'Optimist' and 'Critic'.
            Each line MUST be a long paragraph (at least 5 sentences) explaining technical details.
            
            STRICT FORMAT:
            Optimist: [Text]
            Critic: [Text]
            (Repeat for 10 lines total)
            
            DO NOT use labels like 'Speaker 1' or 'Host'. Use ONLY 'Optimist' and 'Critic'.
            DO NOT include any intro or conversational filler.
            """

            response_data = ollama.generate(
                model='llama3', 
                prompt=prompt,
                options={
                    "temperature": 0.8,
                    "num_predict": 3000, 
                    "seed": int(time.time())
                }
            )
            response = response_data['response']
            print(f"DEBUG SCRIPT:\n{response[:500]}...") # Print first 500 chars

            # 4. RENDERING (With Auto-Alternate Fallback)
            yield f"data: {json.dumps({'step': 'rendering', 'msg': 'Synthesizing Neural Voices...'})}\n\n"
            
            selected_voices = PERSONA_MAP.get(persona, PERSONA_MAP["expert-skeptic"])
            voice_list = list(selected_voices.values()) # [Optimist_Voice, Critic_Voice]
            
            raw_lines = [l.strip() for l in response.strip().split('\n') if ":" in l]
            combined_audio = AudioSegment.empty()
            
            for i, line in enumerate(raw_lines):
                parts = line.split(":", 1)
                if len(parts) < 2: continue
                
                # 1. CLEAN SPEAKER LABEL
                speaker_label = parts[0].replace("*", "").strip()
                raw_text = parts[1].strip()
                clean_text = re.sub(r'[\(\[].*?[\)\]]', '', raw_text)
                
                # 2. VOICE ASSIGNMENT (SMART FALLBACK)
                # If LLM uses the wrong name, we alternate voices based on line number (Even/Odd)
                if "Optimist" in speaker_label:
                    voice_id = voice_list[0]
                elif "Critic" in speaker_label:
                    voice_id = voice_list[1]
                else:
                    # Fallback: Line 0, 2, 4 = Voice 1 | Line 1, 3, 5 = Voice 2
                    voice_id = voice_list[i % 2]
                
                print(f"DEBUG: Processing Line {i} | Speaker: {speaker_label} | Voice: {voice_id}")
                
                temp_name = f"temp_{i}.mp3"
                await generate_voice(clean_text, voice_id, temp_name)
                
                if os.path.exists(temp_name) and os.path.getsize(temp_name) > 100:
                    segment = AudioSegment.from_mp3(temp_name)
                    combined_audio += segment + AudioSegment.silent(duration=600)
                    os.remove(temp_name)

            combined_audio.export("podcast_audio.mp3", format="mp3")
            print(f"✅ Final Audio Length: {len(combined_audio)/1000}s")

            # 5. IMAGE & VIDEO
            yield f"data: {json.dumps({'step': 'rendering', 'msg': 'Imaging and Rendering...'})}\n\n"
            generate_image(f"Cinematic futuristic tech podcast studio, {topic}, 8k", "podcast_visual.png")
            
            timestamp = int(time.time())
            final_video_name = f"output_{timestamp}.mp4"
            create_video_segment("podcast_visual.png", "podcast_audio.mp3", final_video_name)
            
            video_url = f"http://127.0.0.1:8000/video/{final_video_name}"
            yield f"data: {json.dumps({'step': 'complete', 'msg': 'Success!', 'video_url': video_url})}\n\n"

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