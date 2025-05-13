#!/bin/bash

echo "🔍 Starting atomic commits..."

# Commit updated chatbot logic
git add app/chatbot_logic.py
git commit -m "Refactor chatbot logic to use tone_instructions and improve tone response control"

# Commit updated API
git add api.py
git commit -m "Update API to pass humor, professional, and inspirational tone values to logic"

# Commit updated frontend
git add app/index.html
git commit -m "Enhance frontend UI with tone sliders and dark mode toggle"

# Commit updated README
git add README.md
git commit -m "Update README with latest project setup and usage instructions"

# Commit deletions of old scripts
git rm chatbot.py chatbot_basic.py
git commit -m "Remove outdated chatbot entry scripts (chatbot.py, chatbot_basic.py)"

# Commit new intent classifier
git add intent_classifier.py
git commit -m "Add intent classifier to support short, list, and detailed query styles"

# Commit run script
git add run_chatbot.sh
git commit -m "Add run_chatbot.sh to start Flask + Ollama chatbot with dynamic rebuild"

# Commit Dockerfile
git add Dockerfile
git commit -m "Add Dockerfile for building chatbot API with Ollama and LangChain"

# Commit __init__.py to app/
git add app/__init__.py
git commit -m "Add __init__.py to mark app directory as a Python package"

echo "✅ All atomic commits complete."
