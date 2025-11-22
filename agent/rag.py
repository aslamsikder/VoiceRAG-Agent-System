import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from config import Config

class RAGEngine:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDING_MODEL, 
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.vector_store = None

    def ingest_documents(self, doc_dir: str):
        """
        Loads PDFs/Text from directory, chunks them, and builds FAISS index.
        """
        if not os.path.exists(doc_dir):
            raise FileNotFoundError(f"Directory {doc_dir} not found.")

        # Load documents (Support PDF and Text)
        loaders = [
            DirectoryLoader(doc_dir, glob="**/*.pdf", loader_cls=PyPDFLoader),
            DirectoryLoader(doc_dir, glob="**/*.txt", loader_cls=TextLoader)
        ]
        
        documents = []
        for loader in loaders:
            try:
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading files with {loader}: {e}")
        
        if not documents:
            print(f"No documents found in '{doc_dir}'. Index not created.")
            return

        print(f"Loaded {len(documents)} documents.")

        # Chunking strategy for context preservation
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(documents)
        
        if not splits:
            print("No text chunks created. Documents might be empty.")
            return

        # Create Vector Store
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        self.vector_store.save_local(Config.VECTOR_DB_PATH)
        print(f"Index saved to {Config.VECTOR_DB_PATH}")

    def load_index(self):
        """Loads the existing FAISS index."""
        if os.path.exists(Config.VECTOR_DB_PATH):
            self.vector_store = FAISS.load_local(
                Config.VECTOR_DB_PATH, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            print("No index found. Please run ingest_documents first.")

    def retrieve(self, query: str, k: int = 3) -> str:
        """Retrieves top-k relevant context."""
        if not self.vector_store:
            self.load_index()
        
        if not self.vector_store:
            return ""

        docs = self.vector_store.similarity_search(query, k=k)
        
        # Combine content for the LLM
        context = "\n\n".join([doc.page_content for doc in docs])
        return context