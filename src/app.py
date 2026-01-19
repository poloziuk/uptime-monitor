from flask import Flask, render_template_string
from src.db import get_results, init_db

app = Flask(__name__)


@app.route("/")
def index():
    results = get_results()
    html = """
    <!doctype html>
    <html>
    <head><title>Uptime Monitor</title></head>
    <body>
        <h1>Uptime results</h1>
        <table border="1" cellpadding="5">
            <tr><th>ID</th><th>URL</th><th>Status</th><th>Checked At</th></tr>
            {% for r in results %}
              <tr>
                <td>{{ r.id }}</td>
                <td>{{ r.url }}</td>
                <td>{{ r.status }}</td>
                <td>{{ r.checked_at }}</td>
              </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, results=results)


if __name__ == "__main__":
    init_db()  # переконайся, що база створена
    app.run(host="0.0.0.0", port=5000)
