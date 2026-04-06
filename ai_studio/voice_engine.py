import edge_tts
import asyncio
import os

async def generate_voice(text: str, voice_id: str, filename: str):
    """
    Synthesizes text into speech using a specific Edge-TTS Neural Voice.
    
    Args:
        text (str): The dialogue line to speak.
        voice_id (str): The specific Neural Voice ID (e.g., 'en-GB-RyanNeural').
        filename (str): The temporary path to save the .mp3 segment.
    """
    try:
        # We pass the voice_id directly from server.py now
        communicate = edge_tts.Communicate(text, voice_id)
        await communicate.save(filename)
        
        # Validation: Ensure the file was actually created and has data
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"✅ Synthesized [{voice_id}]: {filename} ({os.path.getsize(filename)} bytes)")
        else:
            print(f"⚠️ Warning: Synthesis failed or file is empty for {filename}")
            
    except Exception as e:
        print(f"❌ Voice Engine Error for {voice_id}: {e}")
        # Create a silent placeholder so the video engine doesn't crash
        raise e