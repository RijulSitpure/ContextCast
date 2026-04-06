import asyncio
import ollama
import os
import torch
from pydub import AudioSegment
from rag_engine import get_context_from_pdf
from voice_engine import generate_voice
from image_engine import generate_image
from video_engine import create_video_segment

async def main():
    print("\n🚀 --- ADVANCED DUO-HOST RAG SYSTEM ---")
    
    # --- 1. HARDWARE & ENVIRONMENT CHECK ---
    print("--- System Status ---")
    if torch.backends.mps.is_available():
        print("GPU: Apple Silicon (MPS) Active ✅")
    else:
        print("GPU: CPU Mode (Standard) ⚠️")
    print(f"LLM: Llama 3 (Ollama) Online ✅")
    print("----------------------\n")

    # Ensure folders exist
    if not os.path.exists("data"): 
        os.makedirs("data")
        print("Created /data folder. Please place 'source.pdf' inside.")
        return

    pdf_path = "data/source.pdf"
    if not os.path.exists(pdf_path):
        print(f"❌ Error: {pdf_path} not found. Please add your PDF to the data folder.")
        return

    topic = input("Enter a topic or question based on your PDF: ")

    # --- 2. RAG: SEMANTIC RETRIEVAL ---
    context = get_context_from_pdf(pdf_path, topic)

    # --- 3. BRAIN: DUO-SCRIPT GENERATION ---
    print("\n[1/4] Brain: Writing a Podcast Dialogue...")
    dialogue_prompt = f"""
    Context from Research Paper: {context}
    
    Write a short 4-line podcast dialogue about {topic} between two hosts: 'Optimist' and 'Critic'.
    'Optimist' is enthusiastic and explains a breakthrough. 
    'Critic' is British, skeptical, and asks a sharp follow-up question.
    
    Format your response EXACTLY like this (NO INTRO TEXT):
    Optimist: [speech]
    Critic: [speech]
    Optimist: [speech]
    Critic: [speech]
    """
    
    response_data = ollama.generate(model='llama3', prompt=dialogue_prompt)
    script_response = response_data['response']
    print(f"--- Dialogue Generated ---\n{script_response}\n")

    # --- 4. VOICE: NEURAL SYNTHESIS & STITCHING ---
    print("\n[2/4] Voice: Synthesizing Duo-Voices...")
    lines = script_response.strip().split('\n')
    combined_audio = AudioSegment.empty()
    
    if os.path.exists("podcast_audio.mp3"): os.remove("podcast_audio.mp3")

    for i, line in enumerate(lines):
        # FIX: Check if line has a colon AND contains one of our speaker names
        if ":" in line and any(name in line for name in ["Optimist", "Critic"]):
            try:
                speaker_name, speech_text = line.split(":", 1)
                temp_filename = f"part_{i}.mp3"
                
                # Generate individual MP3
                await generate_voice(speech_text.strip(), speaker_name.strip(), temp_filename)
                
                # Append and cleanup
                combined_audio += AudioSegment.from_mp3(temp_filename)
                os.remove(temp_filename) 
            except Exception as e:
                print(f"⚠️ Skipping line: {line[:30]}... Reason: {e}")

    # Final export
    combined_audio.export("podcast_audio.mp3", format="mp3")
    print("--- Master Audio Combined: podcast_audio.mp3 ---")

    # --- 5. EYES: CONTEXT-AWARE VISUALS ---
    print("\n[3/4] Eyes: Llama 3 is imagining the scene...")
    visual_req = f"Describe a cinematic, futuristic 4k visual scene for this script: '{script_response}'. Max 15 words, no people."
    visual_desc = ollama.generate(model='llama3', prompt=visual_req)['response']
    
    final_img_prompt = f"{visual_desc}, intricate circuitry, cinematic lighting, hyper-realistic, 8k, unreal engine 5, sharp focus"
    generate_image(final_img_prompt, "podcast_visual.png")

    # --- 6. ASSEMBLY: FINAL RENDERING ---
    print("\n[4/4] Assembly: Stitching Final MP4...")
    if os.path.exists("RAG_PODCAST_FINAL.mp4"): os.remove("RAG_PODCAST_FINAL.mp4")
    create_video_segment("podcast_visual.png", "podcast_audio.mp3", "RAG_PODCAST_FINAL.mp4")

    print("\n✅ MISSION SUCCESS: Check RAG_PODCAST_FINAL.mp4")

if __name__ == "__main__":
    asyncio.run(main())