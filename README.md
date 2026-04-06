
# 🎙️ ContextCast AI: Multimodal RAG-to-Video Pipeline

**ContextCast** is an advanced AI-driven platform that transforms static, complex PDF documents into engaging, 2-minute video podcasts. By leveraging a state-of-the-art **RAG (Retrieval-Augmented Generation)** architecture, the system synthesizes technical debates between distinct AI personas, complete with neural voices and generative visuals.



## 🚀 Core Features

* **Deep-Dive RAG Engine:** Utilizes **ChromaDB** and **Sentence-Transformers** to perform semantic search, ensuring every line of dialogue is grounded in the source PDF.
* **Multimodal Synthesis:**
    * **LLM:** Llama 3 (via Ollama) for structured, intellectual scriptwriting.
    * **TTS:** Edge-TTS Neural voices for high-fidelity, multi-accent host personas.
    * **CV:** Stable Diffusion XL (SDXL) for generating contextually relevant cinematic backgrounds.
* **Persona-Driven Dialogue:** Choose between different host pairs (e.g., *Expert & Skeptic* or *Storyteller & Scientist*) with unique vocal characteristics and debate styles.
* **Real-Time Progress Tracking:** A React-based dashboard with a Streaming SSE (Server-Sent Events) backend to monitor every stage of the pipeline.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | React, Vite, Tailwind CSS, Framer Motion |
| **Backend** | FastAPI (Python), Uvicorn |
| **Orchestration** | LangChain / Custom RAG Logic |
| **Database** | ChromaDB (Vector Store) |
| **Inference** | Ollama (Llama 3), Stable Diffusion XL |
| **Processing** | FFmpeg, Pydub, Edge-TTS |

---

## ⚙️ Architecture Flow

1.  **Ingestion:** User uploads a PDF; the document is split into chunks and embedded into **ChromaDB**.
2.  **Retrieval:** Based on the "Discussion Focus," the system retrieves the most relevant technical context.
3.  **Scripting:** Llama 3 generates a 10 line dialogue, debating the nuances of the retrieved context.
4.  **Audio Synthesis:** Each line is converted to speech using specific **Neural Voice IDs**.
5.  **Visual Generation:** A cinematic prompt is sent to SDXL to create the podcast's visual environment.
6.  **Composition:** **FFmpeg** stitches the audio segments and background into a final `.mp4` deliverable.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.10+
* Node.js & NPM
* [Ollama](https://ollama.com/) (with `llama3` model pulled)
* FFmpeg (`brew install ffmpeg`)

### 1. Backend Setup

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn pydub edge-tts ollama chromadb sentence-transformers

# Run the server
python server.py

### 2. Frontend Setup

# Install dependencies
cd frontend
npm install
npm run dev

---

## 📸 Screenshots

> *Tip: Once you have the app running, take a high-res screenshot and replace this placeholder with `![Dashboard](./screenshot.png)`*

---

## 👨‍💻 Author

**Rijul Sitpure**
* B.Tech Data Science @ Manipal University

---