import discord
from discord.ext import commands

# Bot setup with command prefix "-"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)

# Replace this with your specific role ID
ROLE_ID = 1331524868834852904  # Put your role ID here
ROLE_ID2 = 1322671881232584835
channel_message_counts = {}
MESSAGE_LIMIT = 50
ROLE_ID3 = 1333257956493361153  # Replace with your desired role ID
DELETE_INTERVAL_HOURS = 20

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Initialize message counts for all channels
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                messages = [msg async for msg in channel.history(limit=None)]
                channel_message_counts[1333281332456849540] = len(messages)
                print(f'Initialized {channel.name} with {len(messages)} messages')
            except Exception as e:
                print(f'Error accessing channel {channel.name}: {e}')
@bot.event
async def on_member_join(member):
    """Automatically assign role to new members"""
    try:
        role = member.guild.get_role(ROLE_ID3)
        if role:
            await member.add_roles(role)
            print(f'Assigned role to {member.name}')
        else:
            print(f'Role with ID {ROLE_ID3} not found')
    except Exception as e:
        print(f'Error assigning role: {e}')

@tasks.loop(hours=DELETE_INTERVAL_HOURS)
async def delete_old_messages():
    """Delete messages from all channels every 20 hours"""
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                # Check if bot has permission to manage messages in this channel
                if channel.permissions_for(guild.me).manage_messages:
                    deleted = await channel.purge(
                        limit=None,  # No limit on number of messages to delete
                        check=lambda m: not m.pinned  # Don't delete pinned messages
                    )
                    print(f'Deleted {len(deleted)} messages from {channel.name}')
            except Exception as e:
                print(f'Error deleting messages in {channel.name}: {e}')

@delete_old_messages.before_loop
async def before_delete():
    """Wait until the bot is ready before starting the deletion loop"""
    await bot.wait_until_ready()

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    channel_id = message.channel.id
    
    # Initialize count if channel is not in dictionary
    if channel_id not in channel_message_counts:
        messages = [msg async for msg in message.channel.history(limit=None)]
        channel_message_counts[1333281332456849540] = len(messages)
    else:
        channel_message_counts[1333281332456849540] += 1


    # Check if channel has reached the message limit
    if channel_message_counts[1324254906894258217] > MESSAGE_LIMIT:
        try:
             async for oldest_message in message.channel.history(limit=1, oldest_first=True):
                await oldest_message.delete()
                channel_message_counts[1324254906894258217] -= 1
                print(f'Deleted oldest message in {message.channel.name}')
                break
        except Exception as e:
            print(f'Error deleting message: {e}')

    await bot.process_commands(message)

# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in {event}: {args[0]}')

@bot.command(name='d')
@commands.has_permissions(manage_roles=True)
async def assign_role(ctx, user: discord.Member):
    """
    Silently assigns the specified role to a user
    Usage: -assignrole @user
    """
    try:
        role = ctx.guild.get_role(ROLE_ID2)
        if role is not None:
            await user.add_roles(role)
    except:
        pass

@bot.command(name='fm')
@commands.has_permissions(manage_roles=True)
async def assign_role(ctx, user: discord.Member):
    """
    Silently assigns the specified role to a user
    Usage: -assignrole @user
    """
    try:
        role = ctx.guild.get_role(ROLE_ID)
        if role is not None:
            await user.add_roles(role)
    except:
        pass

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_user(ctx, user_id: int):
    """
    Silently bans a user using their user ID
    Usage: -ban user_id
    """
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.ban(user)
    except:
        pass

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run()