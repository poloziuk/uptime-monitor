from flask import Flask, render_template
from src.db import get_results, init_db

app = Flask(__name__)


@app.route("/")
def index():
    results = get_results()
    return render_template("index.html", results=results)


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000)
