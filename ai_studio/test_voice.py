# In a new temporary file test_voice.py
import edge_tts
import asyncio

async def test():
    # 'Jenny' is a high-quality Neural voice, not a robot
    communicate = edge_tts.Communicate("I am a neural AI, not a robot.", "en-US-JennyNeural")
    await communicate.save("test_neural.mp3")

asyncio.run(test())