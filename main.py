from config import OPENAI_API_KEY
from chatbot import create_youtuber_chatbot
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_id = request.form.get("video_id")
        youtuber_name = request.form.get("youtuber_name")
        question = request.form.get("question")

        chatbot = create_youtuber_chatbot(video_id, youtuber_name, OPENAI_API_KEY)
        answer = chatbot.ask(question)

        return render_template("index.html", answer=answer)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
