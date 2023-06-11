import os
from flask import Flask, request
from slack_bolt import App
from dotenv import load_dotenv
from helper_funcs import *

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Slack Bolt app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Route to handle Slack events
@app.route("/slack/events", methods=["POST"])
def handle_slack_events():
    payload = request.get_json()

    if "challenge" in payload:
        return payload["challenge"], 200
    if payload.get("event", {}).get("type") == "message":
        handle_message(payload)
    if payload.get("event", {}).get("type") == "app_mention":
        handle_mentions(payload, channel_messages)
    return "Event received", 200

# Handle message event
def handle_message(payload):
    event = payload["event"]
    channel_id = event["channel"]
    user_id = event["user"]
    text = event["text"]

    # Verify the poster is not the bot
    if not_bot(user_id):
        # Add the message to the channel
        add_message_to_channel(channel_id, user_id, text, channel_messages)
    # Debugging print
    print(channel_messages)
    return "Recieved Message", 200

# Handle app mention event
def handle_mentions(payload, channel_messages):
    who_asked = payload["event"]["user"]
    channel_id = payload["event"]["channel"]
    message = payload["event"]["text"]

    # Verify the poster is not the bot
    if not_bot(who_asked):
        # Handle the message
        handle_app_mention_message(message, channel_messages, channel_id, who_asked)
    return "Recieved Mention", 200
        

# Start application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(port=port, debug=True)