from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)
openai.api_key = 'your-openai-key'
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json["message"]
    chat_history.append({"role": "user", "content": user_msg})
    if len(chat_history) > 6:
        chat_history.pop(0)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful AI chatbot."}] + chat_history
    )
    bot_reply = response.choices[0].message.content.strip()
    chat_history.append({"role": "assistant", "content": bot_reply})
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
