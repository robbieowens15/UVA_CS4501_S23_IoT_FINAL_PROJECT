from flask import Flask, request

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def receiver():
    print("Data: "+request.json)
    return "Received"