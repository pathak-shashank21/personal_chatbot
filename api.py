from flask import Flask, request, jsonify, send_from_directory
from app.chatbot_logic import get_chatbot_response
import traceback
import os

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = get_chatbot_response(question)
        return jsonify({"answer": answer})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return send_from_directory("app", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
