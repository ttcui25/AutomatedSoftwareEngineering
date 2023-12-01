import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

# Set your Slack API token
SLACK_API_TOKEN = "YOUR_SLACK_API_TOKEN"
CHANNEL_ID = "YOUR_CHANNEL_ID"

# Initialize the Slack client
client = WebClient(token=SLACK_API_TOKEN)

# Function to post stand-up messages
def post_standup_messages(channel_id, messages):
    try:
        for user, message in messages.items():
            user_message = f"Stand-up for {user}:\n{message}"
            client.chat_postMessage(channel=channel_id, text=user_message)
    except SlackApiError as e:
        print(f"Error posting messages: {e.response['error']}")

# Function to gather stand-up responses
def gather_standup_responses(users):
    standup_responses = {}
    for user in users:
        response = input(f"Enter stand-up message for {user}: ")
        standup_responses[user] = response
    return standup_responses

# Get list of users in the channel
def get_channel_members(channel_id):
    try:
        response = client.conversations_members(channel=channel_id)
        return response["members"]
    except SlackApiError as e:
        print(f"Error getting channel members: {e.response['error']}")
        return []

# Main function to run the stand-up bot
def main():
    channel_members = get_channel_members(CHANNEL_ID)
    if not channel_members:
        print("Error retrieving channel members.")
        return

    # Run stand-up for each user
    for member_id in channel_members:
        member_info = client.users_info(user=member_id)
        member_name = member_info["user"]["real_name"]
        standup_responses = gather_standup_responses([member_name])
        post_standup_messages(CHANNEL_ID, standup_responses)

if __name__ == "__main__":
    main()

