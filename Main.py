from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRequests
from telethon.tl.functions.messages import ApproveChatJoinRequest

# Replace with your credentials
api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM"

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
            await client(ApproveChatJoinRequest(channel=channel, user_id=user.id))
            count += 1
        except Exception as e:
            print(f"Failed to approve {user.id}: {e}")
    return count

@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    try:
        channel = await client.get_entity(-1002461664947)  # Replace with your group/channel ID or @username
        accepted = await accept_all_pending_requests(channel)
        await event.reply(f"✅ Approved {accepted} pending join requests.")
    except Exception as e:
        await event.reply(f"❌ Error occurred: {e}")

client.run_until_disconnected()
