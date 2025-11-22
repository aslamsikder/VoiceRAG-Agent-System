import openai
import os
import warnings
from config import Config

class STTHandler:
    def __init__(self):
        # 1. Setup OpenAI Client
        if Config.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        else:
            self.client = None
            print("No OpenAI Key found. STT will default to Local Whisper.")

        # 2. Local Model Placeholder (Lazy Loading)
        # We don't load the heavy local model unless we actually need it (to save RAM)
        self.local_model = None

    def _load_local_model(self):
        """Loads the local Whisper model only when needed."""
        if not self.local_model:
            print("Loading Local Whisper Model (this may take a moment)...")
            import whisper
            # 'base' is a good balance of speed/accuracy for CPU
            self.local_model = whisper.load_model(Config.STT_MODEL_LOCAL)
            print("Local Model Loaded.")

    def transcribe(self, audio_file_path: str) -> str:
        """
        Hybrid Transcription Strategy:
        1. Try OpenAI API (Fastest, Best Quality).
        2. If Error or No Key -> Fallback to Local Whisper (Robust).
        """
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

        # --- Attempt 1: OpenAI API ---
        if self.client:
            try:
                with open(audio_file_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=Config.STT_MODEL_API, 
                        file=audio_file
                    )
                return transcript.text
            except Exception as e:
                print(f"OpenAI API STT Failed: {e}")
                if not Config.ENABLE_LOCAL_FALLBACK:
                    return ""
                print("Switching to Local Whisper Fallback...")
        
        # --- Attempt 2: Local Fallback ---
        if Config.ENABLE_LOCAL_FALLBACK:
            try:
                self._load_local_model()
                # Local whisper expects path string, not file object
                result = self.local_model.transcribe(audio_file_path)
                return result["text"]
            except Exception as e:
                print(f"Local STT Failed: {e}")
                return ""
        
        return ""