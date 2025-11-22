from agent.rag import RAGEngine

if __name__ == "__main__":
    print("Starting Document Ingestion...")
    
    # Initialize the RAG engine
    r = RAGEngine()
    
    # Run ingestion on the 'data' folder
    # Ensure you have created a folder named 'data' and put PDFs/txt files inside it
    r.ingest_documents("data")
    
    print("Ingestion Complete. Vector Database created.")