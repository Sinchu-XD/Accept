from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsRequests
from telethon.tl.functions.messages import ImportChatInviteRequest

# Bot credentials
api_id = 6067591
api_hash = "94e17044c2393f43fda31d3afe77b26b"
bot_token = "7443259882:AAE8tgZbbhKVaYbWdfwCe6rwJt7ADSRicYM"

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

async def approve_user(channel, user_id):
    try:
        # Manual approval (undocumented method, works)
        await client(functions.messages.HideChatJoinRequestRequest(
            peer=channel,
            user_id=user_id,
            approved=True
        ))
        return True
    except Exception as e:
        print(f"Error approving user {user_id}: {e}")
        return False

async def accept_all_pending_requests(channel):
    total_approved = 0
    offset = 0

    while True:
        result = await client(GetParticipantsRequest(
            channel=channel,
            filter=ChannelParticipantsRequests(),
            offset=offset,
            limit=100,
            hash=0
        ))

        if not result.users:
            break

        for user in result.users:
            approved = await approve_user(channel, user.id)
            if approved:
                total_approved += 1

        offset += len(result.users)

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
