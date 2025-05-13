import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipant
from telethon.tl.functions.channels import EditBannedRequest
import time

# Replace with your own API details
api_id = 'API_ID'  # Replace with your API ID
api_hash = 'API_HASH'  # Replace with your API Hash
bot_token = 'BOT_TOKEN'  # Replace with your Bot Token

# Initialize Telethon client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def accept_all_pending_requests(channel):
    # Fetch all participants of the channel
    participants = await client(GetParticipantsRequest(channel, filter=ChannelParticipant.PENDING, limit=1500))
    
    accepted = 0
    for participant in participants.users:
        try:
            # Accept the pending request (if it's a user awaiting approval)
            print(f'Accepting request from {participant.username}...')
            await client(EditBannedRequest(channel, participant.id, BANNED_RIGHTS))
            accepted += 1
            await asyncio.sleep(2)  # Delay to avoid hitting rate limits (adjust as needed)
        except Exception as e:
            print(f'Error accepting request from {participant.username}: {e}')
            await asyncio.sleep(5)  # Delay in case of error (e.g., rate limit)

    return accepted

@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    # Replace 'channel_username' with the actual username or ID of your channel
    channel = await client.get_entity('channel_username')
    
    # Accept all pending requests
    accepted = await accept_all_pending_requests(channel)
    
    await event.reply(f"Successfully accepted {accepted} pending requests!")

client.run_until_disconnected()
