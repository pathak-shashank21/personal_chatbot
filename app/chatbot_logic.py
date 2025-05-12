from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
import socket


llm = OllamaLLM(
    model="llama3",
    base_url = "http://192.168.0.244:11434"  # ← replace with YOUR actual IP
)



embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Load FAISS Index ===
vectorstore = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 8, "fetch_k": 25}
)

# === Prompt Template ===
template = """
You are an intelligent, helpful assistant speaking on behalf of Shashank Pathak. You are answering questions using context retrieved from documents such as his CV, thesis, recommendation letters, and publications.

Your job is to:
- Use ONLY the provided context below.
- Write clearly, like a real person would speak when explaining someone’s background in a technical but friendly way.
- If multiple people are involved, summarize them carefully and mention names with roles.
- If the answer is not in the context, say: "I'm sorry, I couldn't find that in the documents."
- Always refer to Shashank in third person.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = ChatPromptTemplate.from_template(template)

# === Create QA Chain ===
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

# === Optional: Rewrite queries smartly ===
def rewrite_query(query):
    q = query.lower().strip()
    if q in {"and", "what else", "what more", "continue"}:
        return "Continue the previous answer in more technical depth and include additional examples if available."
    if any(w in q for w in ["result", "outcome", "findings", "conclusion"]):
        return "Summarize the results and key findings of Shashank Pathak’s Master's thesis."
    if any(w in q for w in ["recommend", "reference", "endorse"]):
        return "List all individuals who recommended Shashank and summarize what they said."
    if any(w in q for w in ["compare", "difference", "vs"]):
        return "Compare Shashank’s work experience or tools used at DiGOS and GFZ."
    return query

def get_chatbot_response(query: str) -> str:
    print("📡 Ollama LLM is connecting to:", llm.base_url)  # <-- Add this line
    final_query = rewrite_query(query)
    result = qa_chain.invoke({"query": final_query})
    return result["result"]

