import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = "data"
INDEX_DIR = "faiss_index"

# === Load PDF files ===
documents = []
for filename in os.listdir(DATA_DIR):
    if filename.lower().endswith(".pdf"):
        path = os.path.join(DATA_DIR, filename)
        print(f"📘 Loading {filename}...")

        loader = PyPDFLoader(path)
        raw_docs = loader.load()

        for doc in raw_docs:
            # Add metadata
            doc.metadata["source"] = filename

            # Bias key documents
            if "thesis" in filename.lower():
                doc.page_content = "[THESIS]\n" + doc.page_content
            elif "recommend" in filename.lower() or "reference" in filename.lower():
                doc.page_content = "[REFERENCE]\n" + doc.page_content

            documents.append(doc)

# === Split documents ===
print("✂️ Splitting text into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# === Load embeddings ===
print("🔍 Embedding and indexing...")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embedding)

# === Save FAISS index ===
vectorstore.save_local(INDEX_DIR)
print("✅ Done. FAISS index saved.")
