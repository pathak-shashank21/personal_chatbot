from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
import re

# 🔗 Load LLM
llm = OllamaLLM(
    model="llama3",
    base_url = "http://192.168.0.244:11434",
    temperature=0.2
)

# 🧠 Embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 📁 Vectorstore
vectorstore = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8, "fetch_k": 25})

# 📜 Custom prompt template
prompt = ChatPromptTemplate.from_template("""
You are an intelligent, helpful assistant answering on behalf of Shashank Pathak.
You use ONLY the context provided below, which comes from documents like his CV, thesis, recommendation letters, and publications.

Adapt your answer based on the following tone and formatting instructions:
{tone_instructions}

Context:
{context}

Question:
{query}

Answer:
""")

# 🔗 QA chain
qa_chain = (
    RunnableMap({
        "context": lambda x: retriever.get_relevant_documents(x["query"]),
        "query": lambda x: x["query"],
        "tone_instructions": lambda x: x["tone_instructions"]
    })
    | prompt
    | llm
)

# 🔍 Intent classifier
def classify_intent(text: str) -> str:
    q = text.lower()
    if any(k in q for k in ["quick", "short", "brief", "summary"]):
        return "short"
    if any(k in q for k in ["list", "points", "bullet"]):
        return "list"
    return "detailed"

# 🎯 Main response generator
def get_chatbot_response(query: str, humor=0, professional=0, inspirational=0) -> str:
    print("📡 Ollama LLM is connecting to:", llm.base_url)

    intent = classify_intent(query)
    print("📊 Detected intent:", intent)

    tone_instructions = []

    if humor > 40:
        tone_instructions.append("Make the response witty, lighthearted, or amusing.")
    if professional > 40:
        tone_instructions.append("Use a formal, precise, and informative tone.")
    if inspirational > 40:
        tone_instructions.append("Make the response motivating, encouraging, or visionary.")
    if not tone_instructions:
        tone_instructions.append("Use a neutral and informative tone.")

    if intent == "short":
        tone_instructions.append("Keep the answer short and concise.")
    elif intent == "list":
        tone_instructions.append("Format the answer as a bullet-point list.")
    else:
        tone_instructions.append("Give a detailed, well-structured explanation.")

    full_tone_instruction = " ".join(tone_instructions)
    print("🧠 Final tone instruction:", full_tone_instruction)

    try:
        response = qa_chain.invoke({
            "query": query,
            "tone_instructions": full_tone_instruction
        })
        return response.strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"
