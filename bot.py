import discord
import responses

async def send_message(message: discord.Message):
    try: 
        respond = responses.handle_response(message.content)
        await message.channel.send(respond)
    except Exception as e:
        print(e)

def run_discord_bot(token: str | None = None):
    if token is None:
        raise Exception("run_discord_bot needs an api token")

    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return
        username = str(message.author)
        channel = str(message.channel)
        print(f'{username} said {message.content} in {channel}')
        await send_message(message)
    
    client.run(token)

