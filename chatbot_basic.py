from sentence_transformers import SentenceTransformer, util
import os

# Load your personal knowledge base
with open("data/about_me.md", "r", encoding="utf-8") as file:
    raw_text = file.read()

# Break it into meaningful chunks
documents = [chunk.strip() for chunk in raw_text.split("\n\n") if chunk.strip()]

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')
document_embeddings = model.encode(documents, convert_to_tensor=True)

# Start assistant-style chatbot
print("🤖 You are now talking to Shashank Pathak's personal assistant. (Type 'exit' to quit)")

while True:
    query = input("\nYou: ")
    if query.lower() in {"exit", "quit"}:
        break

    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, document_embeddings)[0]
    best_match_idx = scores.argmax().item()
    best_response = documents[best_match_idx]

    # Wrap the response in a third-person, assistant tone
    print("\n🧠 Assistant:")
    print(f"As Shashank’s assistant, I can tell you this:\n{best_response}")
