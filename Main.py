from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.messages import ApproveChatJoinRequest
from telethon.tl.types import ChannelParticipantsRequests

# Your API details
api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM"

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

async def accept_all_pending_requests(channel):
    total_approved = 0
    offset = 0

    while True:
        participants = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsRequests(),
            offset=offset,
            limit=100,
            hash=0
        ))

        if not participants.users:
            break

        for user in participants.users:
            try:
                await client(ApproveChatJoinRequest(channel=channel, user_id=user.id))
                total_approved += 1
            except Exception as e:
                print(f"Failed to approve {user.id}: {e}")

        offset += len(participants.users)

    return total_approved

@client.on(events.NewMessage(pattern='/accept_requests'))
async def handler(event):
    try:
        channel = await client.get_entity(-1002461664947)  # Replace with your group ID or @username
        accepted = await accept_all_pending_requests(channel)
        await event.reply(f"✅ Approved {accepted} pending join requests!")
    except Exception as e:
        await event.reply(f"❌ Error: {e}")

client.run_until_disconnected()
