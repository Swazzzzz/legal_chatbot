'''
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load Excel file
qa_df = pd.read_excel("S:\\Learning\\Coding\\Code_Here\\legal_chatbot\\data\\laws.xlsx")

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    query = request.form["query"].lower()

    # Search for keyword in Column A
    answer = "❌ Sorry, I could not find an answer for that."

    for _, row in qa_df.iterrows():
        keyword = str(row["title"]).lower()
        if keyword in query:  # simple keyword match
            answer = row["description"]
            break

    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
'''
from flask import Flask, render_template, request, jsonify
import pandas as pd
from datetime import datetime
import time

app = Flask(__name__)

# Load Excel file
qa_df = pd.read_excel("S:\\Learning\\Coding\\Code_Here\\legal_chatbot\\data\\laws.xlsx")

def current_time():
    return datetime.now().strftime("%H:%M:%S")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    query = data.get("query", "").strip().lower()

    # Greeting handling
    if query in ["hi", "hello", "hey"]:
        answer = "Hello! 👋 How can I assist you legally today?"
    elif query in ["bye", "goodbye", "see you"]:
        answer = "Goodbye! 👋 Stay safe and know your rights."
    else:
        # Delay 2 seconds (simulate "thinking...")
        time.sleep(2)

        # Match keywords in Excel
        answer = "❌ Sorry, I could not find an answer for that."
        for _, row in qa_df.iterrows():
            keyword = str(row["title"]).lower()
            if keyword in query:
                answer = row["description"]
                break

    return jsonify({"answer": answer, "time": current_time()})

@app.route("/clear", methods=["POST"])
def clear():
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
