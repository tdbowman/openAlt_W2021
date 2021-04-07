from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello world!"
if __name__ == "__main__":
    app.run(host = '172.17.0.2', port=5000, debug=True)
