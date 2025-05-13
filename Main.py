import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest, ApproveAllJoinRequestsRequest
from telethon.tl.types import ChannelParticipantsRequests

# Replace with your own API details
api_id = 6067591  # Your API ID
api_hash = "94e17044c2393f43fda31d3afe77b26b"  # Your API Hash
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM"  # Your Bot Token

# Initialize Telethon client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def accept_all_pending_requests(channel):
    participants = await client(GetParticipantsRequest(
        channel=channel,
        filter=ChannelParticipantsRequests(),
        offset=0,
        limit=100,
        hash=0
    ))

    count = 0
    for user in participants.users:
        try:
            await client(ApproveAllJoinRequestsRequest(channel, [user.id]))
            count += 1
        except Exception as e:
            print(f"Failed to approve {user.id}: {e}")
    return count

@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    try:
        # Use correct entity ID or username
        channel = await client.get_entity(-1002461664947)  # Or use @channel_username
        accepted = await accept_all_pending_requests(channel)
        await event.reply(f"✅ Successfully accepted {accepted} pending requests!")
    except Exception as e:
        await event.reply(f"❌ Error: {e}")

client.run_until_disconnected()
