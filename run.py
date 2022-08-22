from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template('pages/index.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)