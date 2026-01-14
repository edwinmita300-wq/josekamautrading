from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# your existing agent logic (keep everything you already have)
from agent import handle_message   # or however you import it

@app.route('/webhook', methods=['POST'])
def webhook():
    data     = request.get_json(force=True)
    username = data.get('user_id')   # IG username string
    message  = data.get('message')

    reply = handle_message(username, message)   # your state-machine
    return jsonify({"user_id": username, "reply": reply}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
