from flask import Flask, request, jsonify
from app.chatbot_logic import get_chatbot_response
import traceback
import os

app = Flask(__name__, static_folder="app", static_url_path="")

@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    question = data.get("question") or data.get("query")
    humor = data.get("humor", 0)
    professional = data.get("professional", 100)
    inspirational = data.get("inspirational", 0)

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = get_chatbot_response(
            question,
            humor=humor,
            professional=professional,
            inspirational=inspirational
        )
        return jsonify({"answer": answer})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, host="0.0.0.0", port=port)
