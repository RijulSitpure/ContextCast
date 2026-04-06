import streamlit as st
import asyncio
import os
import torch
from pydub import AudioSegment
from rag_engine import get_context_from_pdf
from voice_engine import generate_voice
from image_engine import generate_image
from video_engine import create_video_segment
import ollama

# --- PAGE CONFIG ---
st.set_page_config(page_title="AI Duo-Podcast Gen", page_icon="🎙️", layout="wide")

st.title("🎙️ Agentic Duo-Host RAG Podcast")
st.markdown("### Upload a PDF to generate a debate between an **Optimist** and a **Critic**.")

# --- SIDEBAR: SYSTEM STATUS ---
with st.sidebar:
    st.header("System Status")
    if torch.backends.mps.is_available():
        st.success("GPU: Apple Silicon (MPS) Active ✅")
    else:
        st.warning("GPU: CPU Mode (Standard) ⚠️")
    st.info("LLM: Llama 3 (Ollama) Online ✅")
    st.info("Voices: Jenny (Optimist) & Ryan (Critic) ✅")

# --- MAIN UI: FILE UPLOAD ---
uploaded_file = st.file_uploader("Choose a PDF Research Paper", type="pdf")

if uploaded_file is not None:
    if not os.path.exists("data"): os.makedirs("data")
    pdf_path = "data/source.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{uploaded_file.name}' loaded for RAG Analysis!")

    topic = st.text_input("What should the hosts discuss from this paper?", 
                         placeholder="e.g., The Fidelity rates of the quantum gates")

    if st.button("🚀 Generate Duo-Podcast"):
        if not topic:
            st.error("Please enter a topic!")
        else:
            with st.status("🎬 Manufacturing Duo-Podcast...", expanded=True) as status:
                
                # 1. RAG
                st.write("🔍 Searching PDF Knowledge Base...")
                context = get_context_from_pdf(pdf_path, topic)
                
                # 2. BRAIN (Duo-Script)
                st.write("🧠 Llama 3 is scripting the dialogue...")
                dialogue_prompt = f"""
                Context: {context}
                Write a 4-line podcast dialogue about {topic} between 'Optimist' and 'Critic'.
                Format EXACTLY:
                Optimist: [speech]
                Critic: [speech]
                Optimist: [speech]
                Critic: [speech]
                """
                response = ollama.generate(model='llama3', prompt=dialogue_prompt)['response']
                st.session_state.script = response
                
                # 3. VOICE (Multi-Speaker Stitching)
                st.write("🎙️ Synthesizing and Stitching Voices...")
                lines = response.strip().split('\n')
                combined_audio = AudioSegment.empty()
                
                # Use a temporary loop to handle async voice gen
                for i, line in enumerate(lines):
                    if ":" in line and any(name in line for name in ["Optimist", "Critic"]):
                        speaker, text = line.split(":", 1)
                        temp_name = f"part_{i}.mp3"
                        # Run async function in streamlit
                        asyncio.run(generate_voice(text.strip(), speaker.strip(), temp_name))
                        combined_audio += AudioSegment.from_mp3(temp_name)
                        os.remove(temp_name)
                
                combined_audio.export("podcast_audio.mp3", format="mp3")
                
                # 4. EYES
                st.write("🎨 Generating Contextual Visuals...")
                v_req = f"Futuristic cinematic 4k scene for: {topic}. No people."
                v_desc = ollama.generate(model='llama3', prompt=v_req)['response']
                generate_image(f"{v_desc}, 8k, unreal engine 5, sharp", "podcast_visual.png")
                
                # 5. ASSEMBLY
                st.write("🎞️ Final Rendering...")
                create_video_segment("podcast_visual.png", "podcast_audio.mp3", "RAG_PODCAST_FINAL.mp4")
                
                status.update(label="✅ Video Ready!", state="complete", expanded=False)

            # --- DISPLAY RESULTS ---
            st.divider()
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("Final Production")
                st.video("RAG_PODCAST_FINAL.mp4")
            with c2:
                st.subheader("Script Transcript")
                st.text_area("Dialogue Log", value=st.session_state.script, height=200)
                with open("RAG_PODCAST_FINAL.mp4", "rb") as f:
                    st.download_button("Download Podcast", f, "AI_Duo_Podcast.mp4")