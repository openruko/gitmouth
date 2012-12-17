from flask import Flask, request

app = Flask(__name__)


@app.route("/internal/lookupUserByPublicKey")
def check_key():
    # FIXME: 'fingerprint' is assigned to but never used
    fingerprint = request.args.get('fingerprint')
    return "testing:aaa-bbb-ccc-ddd-eee"

app.run(debug=False)
