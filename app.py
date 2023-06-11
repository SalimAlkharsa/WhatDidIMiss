import os
from flask import Flask, request
from slack_bolt import App
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Slack Bolt app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Get bot user ID
bot_user_id = slack_app.client.auth_test()["user_id"]

# Route to handle Slack events
@app.route("/slack/events", methods=["POST"])
def handle_slack_events():
    payload = request.get_json()

    if "challenge" in payload:
        return payload["challenge"], 200
    if payload.get("event", {}).get("type") == "message":
        handle_message(payload)
    if payload.get("event", {}).get("type") == "app_mention":
        handle_mentions(payload)
    return "Event received", 200

    return "", 200

# Dictionary to track messages for each channel
channel_messages = {}
# Maximum number of messages or channels before reset
MAX_MESSAGES = 25 ## Change as necessary
MAX_CHANNELS = 5
# Handle message event
def handle_message(payload):
    event = payload["event"]
    channel_id = event["channel"]
    user_id = event["user"]
    text = event["text"]

    if bot_user_id != user_id:
        # Increment message count
        if channel_id not in channel_messages:
            channel_messages[channel_id] = []

        message_cnt = len(channel_messages[channel_id]) + 1

        # Check if reset is needed based on message count or channels engaged
        if message_cnt > MAX_MESSAGES or len(channel_messages) > MAX_CHANNELS:
            reset_channel_messages(channel_id)

        # Track user_id and text in the dictionary
        channel_messages[channel_id].append({
            "user_id": user_id,
            "text": text
        })

        # Debugging message
        print(channel_messages)
    else:
        pass


def handle_mentions(payload):
    who_asked = payload["event"]["user"]
    channel_id = payload["event"]["channel"]
    message = payload["event"]["text"]

    # Intentional bug: Check if the message is not an integer
    if not message.isdigit():
        # Send a message back to the user
        slack_app.client.chat_postMessage(channel=who_asked, text="Please provide ask using the format @whatdidimiss 5. This is a bug.")

    # If the message is an integer, follow the process
    else:
        num_messages = int(message)
        if num_messages > MAX_MESSAGES:
            num_messages = MAX_MESSAGES
        elif num_messages < 1:
            num_messages = 1
        # Get the messages from the channel
        messages = channel_messages[channel_id][-num_messages:]
        # Send a message back to the user this here is for test
        slack_app.client.chat_postMessage(channel=channel_id, text="Hey @{} The last {} messages are being summarized".format(who_asked, num_messages))
        # Hypothetically summarize the messages
        pass

    


# Helper functions
# Reset channel messages
def reset_channel_messages(channel_id):
    if channel_id in channel_messages:
        channel_messages[channel_id] = []

# Start application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(port=port, debug=True)
