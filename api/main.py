from fastapi import FastAPI, UploadFile, File, HTTPException
from agent.stt import STTHandler
from agent.pipeline import AgentPipeline
import shutil
import os
import time

app = FastAPI(title="Sofof Voice Agent API")

# Initialize Components
# Initialize these once so it doesn't reload models on every request
stt_engine = STTHandler()
agent = AgentPipeline()

@app.get("/")
def health_check():
    return {"status": "active", "service": "Sofof AI Agent"}

@app.post("/process_voice/")
def process_voice(file: UploadFile = File(...)):
    """
    Receives audio file -> STT -> Agent (RAG/Tools) -> Response
    Note: defined as sync 'def' so FastAPI runs it in a threadpool (non-blocking).
    """
    # Create unique temp filename to avoid collision in concurrent requests
    temp_filename = f"temp_{int(time.time())}_{file.filename}"
    
    try:
        # Save uploaded file temporarily
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 1. STT (Speech to Text)
        stt_start = time.time()
        transcribed_text = stt_engine.transcribe(temp_filename)
        stt_time = time.time() - stt_start
        
        if not transcribed_text:
            raise HTTPException(status_code=400, detail="Could not transcribe audio.")
        
        # 2. Agent Logic (RAG or Tools)
        response_text, metrics = agent.process_query(transcribed_text)
        
        # Add STT metrics
        metrics['stt_time'] = round(stt_time, 3)
        
        return {
            "input_text": transcribed_text,
            "response": response_text,
            "metrics": metrics
        }

    except Exception as e:
        # Log the error to console for debugging
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup: Always remove temp file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)