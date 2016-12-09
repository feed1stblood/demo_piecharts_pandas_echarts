from flask import Flask, render_template, jsonify
from data_proc import proc

app = Flask(__name__)


@app.route("/")
def entrance():
    return render_template('demo.html')


@app.route("/chart")
def chart():
    return jsonify(proc())


if __name__ == "__main__":
    app.run(port=9977, debug=True)