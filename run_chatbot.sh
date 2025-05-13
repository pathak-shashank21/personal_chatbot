#!/bin/bash

echo "🚀 Starting Personal Chatbot Docker Setup..."

# Ensure Ollama is up first
if ! curl -s http://localhost:11434 > /dev/null; then
  echo "❌ Ollama is not running. Start it with:"
  echo "   OLLAMA_HOST=0.0.0.0 ollama serve"
  exit 1
fi

# ✅ Set correct Ollama base URL
OLLAMA_URL="http://192.168.0.244:11434"
echo "🌐 Using Ollama base URL: $OLLAMA_URL"

# 🔧 Patch base_url in chatbot_logic.py inside ./app/
echo "🔧 Patching base_url in app/chatbot_logic.py..."
sed -i "s|base_url *= *[\"'].*[\"']|base_url = \"$OLLAMA_URL\"|g" app/chatbot_logic.py

# 🧼 Clean previous container if exists
echo "🧼 Removing old Docker container..."
docker rm -f chatbot-api 2>/dev/null

# 🐳 Build Docker image
echo "🐳 Building Docker image..."
docker build -t chatbot-api .

# 🚀 Run container (map 5050 to 5050)
echo "🚀 Running chatbot on http://localhost:5050 ..."
docker run -d --name chatbot-api -p 5050:5050 chatbot-api

# ⏳ Wait for Flask server to start
echo "⏳ Waiting for Flask server to become reachable..."
for i in {1..30}; do
  sleep 1
  if curl -s http://localhost:5050 > /dev/null; then
    echo "✅ Flask server is up!"
    break
  else
    echo "⌛ Still waiting..."
  fi
done

# 🚨 Final check
if ! curl -s http://localhost:5050 > /dev/null; then
  echo "❌ Flask failed to start. Run this to debug:"
  echo "   docker logs chatbot-api"
  exit 1
fi

# 🧪 Test query
echo "🧪 Sending test query..."
curl -X POST http://localhost:5050/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Shashank Pathak’s thesis about?"}'

echo -e "\n✅ Done. Chatbot is ready at http://localhost:5050"
