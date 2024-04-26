from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = '12345'

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            # Respond with the challenge token for verification
            return challenge
        else:
            # Verification failed
            return 'Verification failed', 403

    # Handle POST requests (incoming messages) here

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5000)
