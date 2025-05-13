import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipant, PeerChannel
from telethon.tl.functions.channels import EditBannedRequest
import time

# Replace with your own API details
api_id = 6067591  # Replace with your API ID
api_hash = "94e17044c2393f43fda31d3afe77b26b"  # Replace with your API Hash
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM" # Replace with your Bot Token

# Initialize Telethon client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRequests

async def accept_all_pending_requests(channel):
    participants = await client(GetParticipantsRequest(
        channel=channel,
        filter=ChannelParticipantsRequests(),
        offset=0,
        limit=100,
        hash=0
    ))

    for user in participants.users:
        await client.approve_join_request(channel, user.id)


@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    # Replace 'channel_username' with the actual username or ID of your channel
    channel = await client.get_entity(PeerChannel(-1002461664947))

    
    # Accept all pending requests
    accepted = await accept_all_pending_requests(channel)
    
    await event.reply(f"Successfully accepted {accepted} pending requests!")

client.run_until_disconnected()
