# assistant.py

from flask import Flask, render_template, request, jsonify
from query_answer import generate_answer
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# Explicitly set template folder path (to ../templates)
TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))
app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        query = request.form.get("query", "")
        answer = generate_answer(query)

        try:
            requests.post(
                "http://localhost:5000/api/speak",
                json={"text": answer},
                timeout=3
            )
            print(f"Sent to avatar: {answer}")
        except Exception as e:
            print(f"[Avatar Error] {e}")

    return render_template("chat.html", answer=answer)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "")
    answer = generate_answer(query)

    try:
        requests.post(
            "http://localhost:5000/api/speak",
            json={"text": answer},
            timeout=3
        )
        print(f"[Async Avatar Speak] {answer}")
    except Exception as e:
        print(f"[Avatar Error - Async] {e}")

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
