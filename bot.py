import discord, requests, asyncio

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Replace with your Discord bot token and IdentityMind API credentials
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
IDENTITYMIND_API_KEY = 'YOUR_API_KEY'
IDENTITYMIND_API_SECRET = 'YOUR_API_SECRET'
IDENTITYMIND_API_URL = 'https://api.identitymind.com/im/account/livetest'

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')
    # Schedule a task to check KYC status after 5 minutes
    await asyncio.sleep(300)  # Wait for 5 minutes
    await check_kyc_and_assign_role()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!kyc'):
        # Generate KYC link and send it as a DM
        user = message.author
        kyc_link = generate_kyc_link(user.id)  # Replace with actual link generation logic
        await user.send(f'Here is your KYC link: {kyc_link}')

async def check_kyc_and_assign_role():
    # Loop through all members in the guild
    for guild in client.guilds:
        for member in guild.members:
            if not await check_kyc(member.id):
                role = discord.utils.get(member.guild.roles, name='member')
                await member.add_roles(role)

async def check_kyc(user_id):
    # Make a request to IdentityMind API and return True if the user is verified, False otherwise
    headers = {
        'Authorization': f'Basic {IDENTITYMIND_API_KEY}:{IDENTITYMIND_API_SECRET}'
    }

    data = {
        'userId': user_id
    }

    response = requests.post(IDENTITYMIND_API_URL, data=data, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('kycStatus') == 'VERIFIED'
    return False

def generate_kyc_link(user_id):
    # Replace this with your actual link generation logic
    return f'https://example.com/kyc?user_id={user_id}'

client.run(TOKEN)
