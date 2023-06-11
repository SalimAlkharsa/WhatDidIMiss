import os
from slack_bolt import App
from dotenv import load_dotenv

# Create slack connection
# Initialize Slack Bolt app
load_dotenv()
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


####################
# Helpers for adding messages to channel
# Dictionary to track messages for each channel
channel_messages = {} # This is just when the app initializes
# Helper functions

# Helper function to check if channel capacity is reached
def channel_at_capacity(channel_messages, channel_id, MAX_MESSAGES=25):
    # Returns 1 if channel is at capacity, 0 otherwise
    # Case: Too many messages in the channel
    if len(channel_messages[channel_id]) > MAX_MESSAGES:
        return 1
    else:
        return 0
    
# Helper function to check if total capacity is reached
def total_at_capacity(channel_messages, MAX_CHANNELS=5):
    # Returns 1 if total is at capacity, 0 otherwise
    # Case: Too many channels
    if len(channel_messages) > MAX_CHANNELS:
        return 1
    else:
        return 0

# Helper function to reset channel messages
def verify_capacity(channel_id, channel_messages, MAX_MESSAGES=25, MAX_CHANNELS=5):
    # Reset if too many messages or too many channels
    # Case 1: Too many messages in the channel
    if channel_at_capacity(channel_messages, channel_id, MAX_MESSAGES):
        channel_messages[channel_id] = []
    # Case 2: Too many channels, clear the oldest channel which is the first key
    if total_at_capacity(channel_messages, MAX_CHANNELS):
        channel_messages.popitem(last=False)
    return channel_messages


# Helper function to add message to channel
def add_message_to_channel(channel_id, user_id, text, channel_messages):
    if not_bot:
        # Check if channel exists
        if channel_id not in channel_messages:
            # If not, create it
            channel_messages[channel_id] = []
        # Check Capacity;  If capacity is reached, reset the channel
        channel_messages = verify_capacity(channel_id, channel_messages)
        # Now, add the message to the channel
        channel_messages[channel_id].append({user_id: text})
        # Done
        return channel_messages


# Helper function to verify poster is not the bot
def not_bot(user_id, bot_user_id = slack_app.client.auth_test()["user_id"]):
    return user_id != bot_user_id

####################
# Helpers for handling app mentions

# Helper function to handle app mention message content
def handle_app_mention_message(message, channel_messages, channel_id, who_asked):
    # To Do: Make it understand the message, for now we will just refer to ints
    # Step 1: Get the message content after the mention
    message = message.split(" ", 1)[1]
    # Case 1: Message is mention and an integer
    if message.isdigit():
        handle_valid_app_mention_message_content(message, channel_messages, channel_id, who_asked)
        pass
    else:
        handle_app_mention_message_error(who_asked)
        pass

# Helper function to handle valid app mention message content
def handle_valid_app_mention_message_content(message, channel_messages, channel_id, who_asked):
    # Step 1: Convert the message to an integer
    num_messages = int(message)
    # Step 2: Validate the number of messages
    num_messages = validate_num_messages(num_messages, channel_id, channel_messages, MAX_MESSAGES=25)
    # Step 3: Debug output to slack
    slack_app.client.chat_postMessage(channel=channel_id, text=f"Howdy @{who_asked}! Here are the last {num_messages} messages:")
    # Now pop remove the channel_id from the list
    channel_messages = channel_messages[channel_id].pop()

    return channel_messages


# Helper function to validate the number of messages
def validate_num_messages(num_messages, channel_id, channel_messages, MAX_MESSAGES=25):
    # Case 1: Too many messages
    if num_messages > MAX_MESSAGES:
        num_messages = MAX_MESSAGES
        # In case the channel has less than the max messages
        if num_messages > len(channel_messages[channel_id]):
            num_messages = len(channel_messages[channel_id])
    # Case 2: Too few messages or no messages
    elif num_messages < 1:
        num_messages = 2
    # Case 3: Requested more messages than are available
    elif num_messages > len(channel_messages[channel_id]):
        num_messages = len(channel_messages[channel_id])
    else:
        num_messages = len(channel_messages[channel_id])
    return num_messages-1 # Subtract 1 to account for the message asking for the messages

# Helper function to handle untelligible app mention message content
def handle_app_mention_message_error(who_asked):
    # DM the user to tell them how to ask
    # Send a message back to the user
    slack_app.client.chat_postMessage(channel=who_asked, text="Please provide ask using the format @whatdidimiss 5.")
    pass
####################