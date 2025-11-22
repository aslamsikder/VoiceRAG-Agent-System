# VoiceRAG Agent System

A voice-enabled AI agent capable of answering questions based on documents (RAG) and performing dynamic function calls (Weather, Stock Prices). Built with **FastAPI**, **Streamlit**, **LangChain**, **FAISS** and **OpenAI**.

## Features
- **Voice Interaction:** Supports real-time voice recording and file uploads.
- **Hybrid STT:** Uses OpenAI Whisper API with automatic fallback to Local Whisper model.
- **RAG Pipeline:** Embeds and retrieves documents using FAISS and OpenAI Embeddings.
- **Agentic Capabilities:** Dynamic function calling for real-time data (Weather, Finance).
- **Modular Design:** OOP-based structure with separate Backend (FastAPI) and Frontend (Streamlit).

---

## How to Run

### 1. Setup Environment

**Option A: Using Conda (Recommended)**
Create Environment and activate
```bash
conda create -n voiceAgent python=3.11 -y
conda activate voiceAgent
```

**Option B: Using Venv**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies
System Requirement (Important): You need ffmpeg installed for audio processing.
- Ubuntu: 
```bash
sudo apt install ffmpeg
```
- Mac: 
```bash 
brew install ffmpeg 
```
- Windows: Download from ffmpeg.org and add to PATH.

**Install Python Packages:**

```bash
pip install -r requirements.txt
```
To uninstall packages listed in a requirements.txt file, use
```bash
pip uninstall -r requirements.txt -y
```

### Configuration (Keep your all API in .env file)
Create a `.env` file in the project root and add your API key:
```bash
# OpenAI API Key (Required for LLM, Embeddings, and Whisper STT)
OPENAI_API_KEY = "Your API Key here"
```

---

## Usage Guide

### Step 1: Ingest Documents (Run once)
Place your PDF or Text documents inside the data/ folder. Create a temporary script `ingest.py` in the project root and then run the ingestion script to create the Vector Database.

```bash
# code of ingest.py (just copy and paste)
from agent.rag import RAGEngine

if __name__ == "__main__":
    print("Starting Document Ingestion...")
    
    # Initialize the RAG engine
    r = RAGEngine()
    
    # Run ingestion on the 'data' folder
    # Ensure you have created a folder named 'data' and put PDFs/txt files inside it
    r.ingest_documents("data")
    
    print("Ingestion Complete. Vector Database created.")
```

Open the terminal and run it: 
```bash
# Make sure you have files in data/ folder first!
python ingest.py
```

### Step 2: Start Backend (FastAPI)
Open a terminal and run the API server:

```bash
uvicorn api.main:app --reload --port 8000
```

### Step 3: Start Frontend (Streamlit)
Open a new terminal tab and run the UI:
```bash
streamlit run frontend/app.py
```
The app will open in your browser at `http://localhost:8501`.

---

## Project Structure

VoiceRAG_agent_System/    
│── .env                 # API Keys (OpenAI, etc.)    
│── config.py            # Central configuration    
│── requirements.txt     # Dependencies    
│── ingest.py            # Script to build FAISS index    
│── README.md            # Documentation    
│    
├── agent/               # Core Logic    
│   ├── __init__.py    
│   ├── rag.py           # Document Embedding & Retrieval    
│   ├── stt.py           # Speech-to-Text (Hybrid)    
│   ├── tools.py         # Dynamic Function Definitions    
│   ├── llm.py           # LLM & Function Calling Logic    
│   └── pipeline.py      # Main Orchestrator    
│    
├── api/                 # FastAPI Backend    
│   └── main.py          # API Endpoints    
|    
├── data/                # save your document here (you can add as much as you want)    
│   └── Attention.pdf    # (Example file)    
│    
└── frontend/            # Streamlit UI    
    └── app.py           # Chat Interface    

---

## ✍️ Author Information    
Developed by **Aslam Sikder**, 22<sup>nd</sup> November, 2025    
Email: [Aslam Sikder's Email](mailto:aslamsikder.edu@gmail.com)    
LinkedIn: [Aslam Sikder's - Linkedin Account](https://www.linkedin.com/in/aslamsikder)    
Kaggle: [Aslam Sikder's - Kaggle Account](https://www.kaggle.com/aslamsikder)    
HuggingFace: [Aslam Sikder's - Huggingface Account](https://huggingface.co/aslamsikder)    
Google Scholar: [Aslam Sikder's - Google Scholar Account](https://scholar.google.com/citations?hl=en&user=Ip1qQi8AAAAJ)    
