import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VECTOR_DB_PATH = "faiss_index"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = "text-embedding-3-small"
    LLM_MODEL = "gpt-4o"
    
    # --- Audio Settings (Hybrid) ---
    STT_MODEL_API = "whisper-1"       # OpenAI API Model
    STT_MODEL_LOCAL = "base"          # Local Model (base, small, medium)
    ENABLE_LOCAL_FALLBACK = True      # If API fails, use Local
    
    # We allow the app to run without a key if Local Fallback is enabled
    if not OPENAI_API_KEY and not ENABLE_LOCAL_FALLBACK:
         raise ValueError("OPENAI_API_KEY not found. Set it or enable local fallback.")