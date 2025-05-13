from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipant, PeerChannel
from telethon.tl.functions.messages import ImportChatInviteRequest
import time

# Replace with your own API details
api_id = 6067591  # Replace with your API ID
api_hash = "94e17044c2393f43fda31d3afe77b26b"  # Replace with your API Hash
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM"  # Replace with your Bot Token

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Function to manually approve requests
async def approve_user(channel, user_id):
    try:
        # Use ImportChatInviteRequest for manual approval
        await client(ImportChatInviteRequest(
            channel=channel,
            user_id=user_id
        ))
        return True
    except Exception as e:
        print(f"Error approving user {user_id}: {e}")
        return False

# Function to accept pending join requests
async def accept_all_pending_requests(channel):
    total_approved = 0
    offset = 0
    while True:
        result = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipant(),
            offset=offset,
            limit=100,
            hash=0
        ))

        if not result.users:
            break

        for user in result.users:
            if user.status == "PENDING":  # If the user is pending
                approved = await approve_user(channel, user.id)
                if approved:
                    total_approved += 1

        offset += len(result.users)

    return total_approved

@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    try:
        # Replace with your channel ID or username
        channel = await client.get_entity(-1002461664947)
        accepted = await accept_all_pending_requests(channel)
        await event.reply(f"✅ Approved {accepted} pending join requests!")
    except Exception as e:
        await event.reply(f"❌ Error: {e}")

client.run_until_disconnected()
