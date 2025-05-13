# 🧠 Personal Document Chatbot (LLM + FAISS + Flask + Ollama)

This is a personal, offline chatbot that answers questions using your own documents (CV, thesis, letters, etc.) with the help of:
- Local LLMs via [Ollama](https://ollama.com/)
- Vector search via FAISS
- A Flask API + frontend UI
- Dockerized deployment

---

## 🚀 Quick Start (One Command)

```bash
./run_chatbot.sh
```

This script will:
1. Detect your machine's IP
2. Check that Ollama is running
3. Update the chatbot to use correct `base_url`
4. Build the Docker image
5. Start the chatbot server on [http://localhost:5050](http://localhost:5050)
6. Test a sample query like:  
   _“What is Shashank Pathak’s thesis about?”_

---

## 📦 Prerequisites

Make sure you have the following installed:

- [Python 3.10+](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/)
- [Ollama](https://ollama.com/) — for local LLMs like `llama3`
- [ngrok (optional)](https://ngrok.com/) — to expose your chatbot to the internet

---

## 🔌 Step-by-Step Setup Guide

### ✅ 1. Start Ollama

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
```

> 🔁 If you see "Error: address already in use", run:
>
> ```bash
> sudo lsof -i :11434
> kill -9 <PID>
> ```

### ✅ 2. Pull the LLM model

```bash
ollama pull llama3
```

You can change the model name later in `chatbot_logic.py`.

---

### ✅ 3. Run the chatbot

```bash
./run_chatbot.sh
```

If you want to run manually:

```bash
docker build -t chatbot-api .
docker run -it --rm -p 5050:5050 chatbot-api
```

> You can also override the port with:
>
> ```bash
> docker run -it --rm -e PORT=5050 -p 5050:5050 chatbot-api
> ```

---

### ✅ 4. Ask Questions

In your terminal:

```bash
curl -X POST http://localhost:5050/query   -H "Content-Type: application/json"   -d '{"question": "What is Shashank Pathak’s thesis about?"}'
```

Or visit [http://localhost:5050](http://localhost:5050) to use the simple chat UI.

---

## 🌐 Expose the chatbot online (optional)

```bash
ngrok http 5050
```

You’ll get a public URL like:

```
https://f3a1-xxx.ngrok-free.app
```

Use it like:

```bash
curl -X POST https://f3a1-xxx.ngrok-free.app/query   -H "Content-Type: application/json"   -d '{"question": "Show me recommendation letters."}'
```

---

## 🧠 Adding / Updating Knowledge

1. **Place your documents** (PDFs, `.json`, `.txt`) into a folder called `data/`:
   ```
   personal_chatbot/
   └── data/
       ├── CV.pdf
       ├── thesis.pdf
       ├── publications.json
       └── references.txt
   ```

2. Run the index builder:

```bash
python build_index.py
```

This will:
- Load and chunk the documents from `data/`
- Create embeddings using `HuggingFaceEmbeddings`
- Save the FAISS vector index to `faiss_index/`

> 📝 If `data/` doesn't exist, create it manually:
>
> ```bash
> mkdir data
> ```

---

## 🧰 Project Structure

```
personal_chatbot/
├── app/
│   ├── chatbot_logic.py     # LangChain + Ollama logic
│   ├── index.html           # Frontend UI
│   └── __init__.py
├── api.py                   # Flask backend (note: OUTSIDE the app folder)
├── data/                    # Your documents go here (PDF, TXT, JSON)
├── faiss_index/
│   └── index.faiss
├── build_index.py
├── run_chatbot.sh
├── Dockerfile
├── requirements.txt
├── knowledge_structured.json
├── knowledge_vectors.json
└── README.md
```

---

## 💻 Development Tips

- All LLM prompts are in `chatbot_logic.py`
- You can switch models (`llama2`, `mistral`, etc.) by changing:
  
  ```python
  OllamaLLM(model="llama3", ...)
  ```

- To reset everything cleanly:

```bash
docker system prune -a
```

---

## ☁️ Push to GitLab and GitHub

Add both remotes:

```bash
git remote add github git@github.com:yourname/personal_chatbot.git
git remote add gitlab git@gitlab.com:yourname/personal_chatbot.git
```

Then push:

```bash
git add .
git commit -m "🔥 Added full LLM chat pipeline with Docker and FAISS"
git push github main
git push gitlab main
```

---

## 📜 License

MIT License — build and customize freely!