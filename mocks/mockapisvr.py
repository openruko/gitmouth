from flask import Flask, request
app = Flask(__name__)

@app.route("/internal/lookupUserByPublicKey")
def check_key():
    fingerprint=request.args.get('fingerprint')
    return "testing:aaa-bbb-ccc-ddd-eee"

app.run(debug=False)

