from langchain_ollama import OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
import warnings

# === Load LLM and Embeddings ===
llm = OllamaLLM(model="llama3")
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# === Load FAISS Index ===
vectorstore = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever(
    search_type="mmr",  # Better diversity
    search_kwargs={"k": 8, "fetch_k": 25}
)

# === Smart Query Rewriting ===
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

# === RetrievalQA Chain ===
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

# === Main Loop ===
print("🤖 [CONVERSATIONAL MODE 2.0] Ask anything about Shashank. Type 'exit' to quit.")

while True:
    query = input("\nYou: ").strip()
    if query.lower() in {"exit", "quit"}:
        print("👋 Exiting.")
        break

    try:
        final_query = rewrite_query(query)
        response = qa_chain.invoke({"query": final_query})
        print(f"\n🧠 Assistant:\n{response['result']}")
    except Exception as e:
        print(f"⚠️ Error: {e}")
