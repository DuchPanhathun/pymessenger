from flask import Flask, request, jsonify
from pymessenger.bot import Bot

# Create a Flask app instance
app = Flask(__name__)

# Replace these with your actual token and app secret
PAGE_ACCESS_TOKEN = 'EAAQXPDV1XqkBOyddsObpMtG6POEhgbwd7pV52OSq1bXGV6m0EeOijDXYbNpWZCeZCX6qZBDo9ZCrAZBG44o0dVyg9BhMZBPqLZC2QJZCstOcrv2iYEXzLiJvgcUy1IJsZC4Jked6wOv5a387lS53wrc3AJlZCnjPhswtZAUHP6gqNRWarTMVVH8JYDvZBp1HwypCfGjWohsk1S3GA6ICN7fG6AZDZD'
APP_SECRET = 'd22af43dcf4eac983eef2fe854b61843'
VERIFY_TOKEN = '12345'  # Use the same token set in the Facebook Developer Dashboard

# Create a Bot instance
bot = Bot(PAGE_ACCESS_TOKEN, app_secret=APP_SECRET)

# Define the webhook endpoint to handle incoming messages

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # Parse incoming JSON data
    data = request.get_json()

    # Process each entry in the incoming data
    for entry in data.get('entry', []):
        messaging_events = entry.get('messaging', [])
        for event in messaging_events:
            sender_id = event['sender']['id']
            if 'message' in event:
                # Get the text of the incoming message
                message_text = event['message']['text']
                # Generate a response based on the incoming message
                response = generate_response(message_text)
                # Send the response back to the user
                bot.send_text_message(sender_id, response)
    
    # Return a status response
    return jsonify({'status': 'ok'})

# Define a function to generate a response based on the user's message
def generate_response(message_text):
    # Lowercase the message for case-insensitive processing
    message_text = message_text.lower()

    # Define basic commands and their responses
    commands = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hi there! What can I do for you?",
        "help": "You can ask me about the weather, news, or other services.",
        "bye": "Goodbye! Have a great day!",
    }

    # Check if the message matches any predefined commands
    if message_text in commands:
        return commands[message_text]

    # Default response if the message is not recognized
    return "I'm sorry, I didn't understand that. Can you please rephrase your question?"

# Verify the webhook during the initial setup with Facebook
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Get the mode and token from the query parameters
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    # Check if the mode and token are correct
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        # Respond with the challenge token
        return str(challenge)

    # Return an error response if the verification fails
    return jsonify({'status': 'error'}), 403

# Run the Flask app on port 5000
if __name__ == '__main__':
    # Set the persistent menu before running the Flask app
    
    app.run(port=5000)
