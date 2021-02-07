#------------------------------------------------------------------------------------------#
#Written by chivenos
#Source code https://github.com/chivenos/beanbot
#Discord chivenos#5890
#E-mail chivenosthedev@gmail.com
#Feel free to use for any purpose
#------------------------------------------------------------------------------------------#


import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import asyncio
from themes import ReturnRandomTheme
import psycopg2


token = YOUR TOKEN #Replace your token
defaultPrefix = "bb"
statusLoopInterval = 30
beanJamNotificationsLoopInterval = 60
statusUpdateLoopInterval = 5
embedColor = discord.Colour.green()
botCredits = "chivenos#5890\nDiscord Server: https://discord.gg/8jcNWqeQgQ"
beanJamStartDate = [6,14,0] #week day, hour, minute (GMT)
beanJamThemeDate = [6,13,40] #week day, hour, minute (GMT)
beanJamReminderDate = [6,13,0] #week day, hour, minute (GMT)
beanJamEndDate = [6,17,30]  #week day, hour, minute (GMT)
beanJamRoleDate = [1,14,0] #week day, hour, minute (GMT)
version = "v1.1"
winnerYellowColor = 0xe4b400
chivenosUserid = "" #CHANGE

db = "" #CHANGE
dbUser = "" #CHANGE
dbPassword = "" #CHANGE
dbHost = "" #CHANGE
dbPort = "" #CHANGE
con = psycopg2.connect(database=db, user=dbUser, password=dbPassword, host=dbHost, port=dbPort)
cur = con.cursor()
print("--DATABASE OPENED--")


#---------Database Functions---------
def selectAllTable(table : str):
    cur.execute(f"SELECT * FROM {table};")
    data = cur.fetchall()

    return data

def selectDbByUserid(table : str, userid : str):
    cur.execute(f"SELECT * FROM {table} WHERE userid = '{userid}';")
    data = cur.fetchall()

    if (data == []):
        return None

    return data[0]

def selectDbByName(table : str, name : str):
    cur.execute(f"SELECT * FROM {table} WHERE name = '{name}';")
    data = cur.fetchall()

    if (data == []):
        return None

    return data[0]

def selectDbByGuildid(table : str, guildid : str):
    cur.execute(f"SELECT * FROM {table} WHERE guildid = '{guildid}';")
    data = cur.fetchall()
    if (data == []):
        return None

    return data[0]

def selectDbByMsgid(table : str, msgid : str):
    cur.execute(f"SELECT * FROM {table} WHERE msgid = '{msgid}';")
    data = cur.fetchall()

    if (data == []):
        return None

    return data[0]

def deleteDbByGuildid(table : str, guildid : str):
    cur.execute(f"DELETE FROM {table} WHERE guildid = '{guildid}';")
    con.commit()

def deleteDbByMsgid(table : str, msgid : str):
    cur.execute(f"DELETE FROM {table} WHERE msgid = '{msgid}';")
    con.commit()

def deleteDbByName(table : str, name : str):
    cur.execute(f"DELETE FROM {table} WHERE name = '{name}';")
    con.commit()

def insertDbCoins(userid : str, coin : str):
    cur.execute(f"INSERT INTO coins (userid, coin) VALUES ('{userid}', '{coin}');")
    con.commit()

def updateDbCoins(userid : str, coin : str):
    cur.execute(f"UPDATE coins SET coin = '{coin}' WHERE userid = '{userid}';")
    con.commit()

def increseCoins(userid, amount):
    data = selectDbByUserid("coins", str(userid))
    if(data == None):
        insertDbCoins(str(userid), "0")
        coins = 0
    else:
        coins = int(data[1])

    coins += amount
    updateDbCoins(str(userid), str(coins))

def decreaseCoins(userid, amount, giveChivenos : bool = True):
    data = selectDbByUserid("coins", str(userid))
    if(data == None):
        insertDbCoins(str(userid), "0")
        coins = 0
    else:
        coins = int(data[1])

    coins -= amount
    if(coins >= 0):
        updateDbCoins(str(userid), str(coins))
        if(giveChivenos):
            increseCoins(chivenosUserid, amount)
        return True

    return False

def insertDbVariables(name : str, value : str):
    cur.execute(f"INSERT INTO variables (name, value) VALUES ('{name}', '{value}');")
    con.commit()

def updateDbVariables(name : str, value : str):
    cur.execute(f"UPDATE variables SET value = '{value}' WHERE name = '{name}';")
    con.commit()

def insertDbReactiontorole(msgid : str, roleid : str, roleid1 : str = None, name : str = None):
    cur.execute(f"INSERT INTO reactiontorole (msgid, roleid, roleid1, name) VALUES ('{msgid}', '{roleid}', '{roleid1}', '{name}');")
    con.commit()

def updateDbReactiontorole(msgid : str, roleid : str, roleid1 : str = None):
    cur.execute(f"UPDATE reactiontorole SET roleid = '{roleid}', roleid1 = '{roleid1}' WHERE msgid = '{msgid}';")
    con.commit()

def insertDbAutorole(guildid : str, roleid : str):
    cur.execute(f"INSERT INTO autorole (guildid, roleid) VALUES ('{guildid}', '{roleid}');")
    con.commit()

def updateDbAutorole(guildid : str, roleid : str):
    cur.execute(f"UPDATE autorole SET roleid = {roleid} WHERE guildid = '{guildid}';")
    con.commit()

def insertDbBeanjamnotificationchannels(guildid : str, channelid : str):
    cur.execute(f"INSERT INTO beanjamnotificationchannels (guildid, channelid) VALUES ('{guildid}', '{channelid}');")
    con.commit()

def updateDbBeanjamnotificationchannels(guildid : str, channelid : str):
    cur.execute(f"UPDATE beanjamnotificationchannels SET channelid = '{channelid}' WHERE guildid = '{guildid}';")
    con.commit()

def insertDbPrefixes(guildid : str, prefix : str = "bb"):
    cur.execute(f"INSERT INTO prefixes (guildid, prefix) VALUES ('{guildid}', '{prefix}');")
    con.commit()

def updateDbPrefixes(guildid : str, prefix : str = "bb"):
    cur.execute(f"UPDATE prefixes SET prefix = '{prefix}' WHERE guildid = '{guildid}';")
    con.commit()

#--------------------


def get_prefix(client, message):
    prefix = selectDbByGuildid("prefixes", str(message.guild.id))
    pfx = prefix[1]
    return [pfx, str.upper(pfx), str.lower(pfx)]


def GetAvatarLink(link):
    return link[0:(len(link)-15)]


def increaseBeanJamCount():
    updateDbVariables("beanJamCount", str(client.beanJamCount + 1))
    client.beanJamCount += 1


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
client.beanJamCount = int(selectDbByName("variables", "beanJamCount")[1])
status = ["Bean Jam #" + str(client.beanJamCount), "bbhelp | by Bean Devs"]
iteratingBool = False
client.status = status
client.version = version
client.iteratingBool = iteratingBool
checkMarkEmoji = "✅"
coinsEmoji = ":coin:"
beanBotInviteLink = "https://top.gg/bot/803206150572081152"


@client.event
async def on_ready(): #When bot is on
    await client.change_presence(status=discord.Status.online, activity=discord.Game(client.status[0]))
    print("--BOT IS ONLINE--")


async def update_status():
    await asyncio.sleep(statusLoopInterval)
    while True:
        await client.change_presence(status=discord.Status.online, activity=discord.Game(client.status[int(client.iteratingBool)]))
        client.iteratingBool = not client.iteratingBool
        await asyncio.sleep(statusLoopInterval)

client.loop.create_task(update_status())


@client.event
async def on_guild_join(guild):  #When joins a guild
    insertDbPrefixes(str(guild.id))


@client.event
async def on_guild_remove(guild):  #When removes from a guild
    deleteDbByGuildid("prefixes", str(guild.id))


@client.event
async def on_member_join(member):
    guild = member.guild
    autoRole = selectDbByGuildid("autorole",str(guild.id))
    if(autoRole != None):
        role = get(guild.roles, id=int(autoRole[1]))
        await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    data = selectDbByMsgid("reactiontorole", str(payload.message_id))
    if(data != None):
        if(payload.emoji.name == checkMarkEmoji):
            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            role0 = get(guild.roles, id=int(data[1]))
            if (role0 != None):
                await user.add_roles(role0)

            if(data[2] != None):
                role1 = get(guild.roles, id=int(data[2]))
                if(role1 != None):
                    await user.add_roles(role1)

            increseCoins(str(payload.user_id), int(data[3]))



@client.event
async def on_raw_reaction_remove(payload):
    data = selectDbByMsgid("reactiontorole", str(payload.message_id))
    if (data != None):
        if (payload.emoji.name == checkMarkEmoji and data[4]):
            guild = client.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)

            role0 = get(guild.roles, id=int(data[1]))
            if (role0 != None):
                await user.remove_roles(role0)

            if (data[2] != None):
                role1 = get(guild.roles, id=int(data[2]))
                if (role1 != None):
                    await user.remove_roles(role1)

            decreaseCoins(str(payload.user_id), int(data[3]))


@client.command()
async def invite(ctx):
    await ctx.send(beanBotInviteLink)


@client.command()
async def coins(ctx):
    userid = ctx.author.id
    data = selectDbByUserid("coins", str(userid))
    if(data == None):
        insertDbCoins(str(userid), "0")
        coins = 0
    else:
        coins = data[1]

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Coins", value=f"You have {coins}{coinsEmoji}.", inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def giveCoins(ctx, member : discord.Member, amount : int):
    userid = str(member.id)
    data = selectDbByUserid("coins", userid)
    if(data == None):
        insertDbCoins(userid,"0")

    increseCoins(userid, amount)

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Give Coins", value=f"{member.mention} got {amount}{coinsEmoji}. He has {int(data[1]) + amount}{coinsEmoji}.", inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def takeCoins(ctx, member : discord.Member, amount : int):
    userid = str(member.id)
    data = selectDbByUserid("coins", userid)
    if(data == None):
        insertDbCoins(userid,"0")

    if(decreaseCoins(userid, amount)):
        sentence = f"{member.mention} lost {amount}{coinsEmoji}. He has {int(data[1])  - amount}{coinsEmoji}."
    else:
        sentence = f"{member.mention}'s coins are not enough. He has {data[1]}{coinsEmoji}."

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Take Coins", value=sentence, inline=False)
    await ctx.send(embed=embed)


@client.command()
async def sendCoins(ctx, member : discord.Member, amount : int):
    memberUserid = str(member.id)
    memberCoins = 0
    memberData = selectDbByUserid("coins", memberUserid)
    if(memberData == None):
        insertDbCoins(memberUserid,"0")
    else:
        memberCoins = int(memberData[1])

    senderUserid = str(ctx.author.id)
    senderCoins = 0
    senderData = selectDbByUserid("coins", senderUserid)
    if(senderData == None):
        insertDbCoins(senderUserid,"0")
    else:
        senderCoins = int(senderData[1])

    if(senderCoins - amount >= 0):
        increseCoins(memberUserid, amount)
        decreaseCoins(senderUserid, amount, False)
        sentence = f"{ctx.author.mention} sent {amount}{coinsEmoji} to {member.mention}."
    else:
        sentence = f"You don't have enough coins to sent."

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Send Coins", value=sentence, inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def autoRole(ctx, role:discord.Role):
    guild = ctx.guild
    result = selectDbByGuildid("autorole", str(guild.id))

    if (result == None):
        insertDbAutorole(str(guild.id), str(role.id))
    else:
        updateDbAutorole(str(guild.id), str(role.id))

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Auto Role", value=f"{role.mention} role assigned as Auto Role.", inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def disableAutoRole(ctx):
    guild = ctx.guild
    deleteDbByGuildid("autorole", str(guild.id))

    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Disable Auto Role", value=f"Auto Role has been disabled successfully.", inline=False)
    await ctx.send(embed=embed)


@client.command()
async def version(ctx):
    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Version", value=client.version, inline=False)
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def changePrefix(ctx, prefix=None): #changes prefix
    guild = ctx.guild
    data = selectDbByGuildid("prefixes", str(guild.id))

    if(data != None):
        oldPrefix = data[1]
        if(prefix):
            updateDbPrefixes(str(guild.id), str(prefix))
        else:
            updateDbPrefixes(str(guild.id), defaultPrefix)
            prefix = defaultPrefix

        embed = discord.Embed(
            colour=embedColor
        )
        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="Prefix Changed", value=f"Prefix has been changed \"{oldPrefix}\" to \"{prefix}\".", inline=False)

        await ctx.send(embed=embed)


@client.command()
async def time(ctx):  #sends today's date
    now = datetime.utcnow()
    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Today's Date (GMT)",value=f"{now.year}-{now.month}-{now.day}\n{now.hour}:{now.minute}:{now.second}", inline=False)

    await ctx.send(embed=embed)



@client.command()
async def localTime(ctx):  #sends today's date
    now = datetime.now()
    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Today's Date (Local)",value=f"{now.year}-{now.month}-{now.day}\n{now.hour}:{now.minute}:{now.second}", inline=False)

    await ctx.send(embed=embed)


@client.command()
async def latency(ctx): #sends latency
    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Latency", value=f"{round(client.latency * 1000)}ms", inline=False)

    await ctx.send(embed=embed)


@client.command()
async def credits(ctx): #sends credits
    embed = discord.Embed(
        colour=embedColor
    )
    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Credits", value=botCredits, inline=False)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(kick_members=True) #User must have kick members permission
async def kick(ctx,member:discord.Member,*,reason=None): #kicks
    await member.kick(reason=reason)
    if(reason):
        embed = discord.Embed(
            colour=embedColor
        )

        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="User Kicked", value=f"{member} has been kicked successfully. The reason is \"{reason}\".", inline=False)

        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            colour=embedColor
        )

        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="User Kicked", value=f"{member} has been kicked successfully.",inline=False)

        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True) #User must have ban members permission
async def ban(ctx,member:discord.Member,*,reason=None): #bans
    await member.ban(reason=reason)
    if(reason):
        embed = discord.Embed(
            colour=embedColor
        )

        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="User Banned", value=f"{member} has been banned successfully. The reason is \"{reason}\".", inline=False)

        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            colour=embedColor
        )

        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="User Banned", value=f"{member} has been banned successfully.",inline=False)

        await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(ban_members=True) #User must have ban members permission
async def unban(ctx, *, member): #unbans
    banned_users = await ctx.guild.bans()

    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)

            embed = discord.Embed(
                colour=embedColor
            )

            avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
            embed.set_author(name=ctx.author.name,
                             icon_url=avatarUrl)
            embed.add_field(name="User Unbanned", value=f"{member} has been unbanned successfully.", inline=False)

            await ctx.send(embed=embed)
            return True

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="User Already Unbanned", value=f"Couldn't unban {member} because user is already unbanned.", inline=False)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True) #User must have manage messages permission
async def clean(ctx,amount="1"):
    if(amount.isnumeric() and int(amount) > 0):
        amount = int(amount)
        amount += 1
        await ctx.channel.purge(limit=amount)


@client.command()
@commands.has_permissions(manage_roles=True) #User must have manage role permission
async def giveRole(ctx, member:discord.Member, role:discord.Role):
    await member.add_roles(role)

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Give Role", value=f"{member.mention} got the {role.mention} role.", inline=False)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_roles=True) #User must have manage role permission
async def removeRole(ctx, member:discord.Member, role:discord.Role):
    await member.remove_roles(role)

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Remove Role", value=f"{role.mention} role removed from {member.mention}.", inline=False)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def changeNickname(ctx, member:discord.Member, newName):
    oldName = member.display_name

    await member.edit(nick=newName)

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Change Nickname", value=f"Nickname of {member.mention} has been changed **\"{oldName}\"** to **\"{newName}\"**.", inline=False)

    await ctx.send(embed=embed)


""" #TOP.GG DOESN'T ACCEPT DM COMMANDS
@client.command()
async def dm(ctx,user:discord.User,*,msg):
    embedDM = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embedDM.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embedDM.add_field(name="DM",
                    value=msg,
                    inline=False)

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="DM",
                    value=f"Directly messaged to {user.mention}. Message will be delivered if the user accepts direct messages.",
                    inline=False)

    await ctx.send(embed=embed)
    await user.send(embed=embedDM)


@client.command()
async def anonymDm(ctx,user:discord.User,*,msg):
    embedDM = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(client.user.avatar_url))
    embedDM.set_author(name=client.user.name,
                       icon_url=avatarUrl)
    embedDM.add_field(name="DM",
                      value=msg,
                      inline=False)

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="DM",
                    value=f"Directly and anonymously messaged to {user.mention}. Message will be delivered if the user accepts direct messages.",
                    inline=False)

    await ctx.send(embed=embed)
    await user.send(embed=embedDM)
"""


@client.event
async def on_command_error(ctx,error):
    if(isinstance(error, commands.CommandNotFound)): #When a command not found
        embed = discord.Embed(
            colour=embedColor
        )

        avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
        embed.set_author(name=ctx.author.name,
                         icon_url=avatarUrl)
        embed.add_field(name="Command Not Found", value=f"Are you sure there is a command like this?",inline=False)

        await ctx.send(embed=embed)


@client.command()
async def generateTheme(ctx):
    theme = ReturnRandomTheme()

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Theme", value=theme, inline=False)

    await ctx.send(embed=embed)


@client.command()
async def beanJamDate(ctx):
    text = "Every Sunday 14:00 (GMT)"

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Bean Jam Date", value=text, inline=False)

    await ctx.send(embed=embed)


@client.command()
async def joinBeanJam(ctx):
    text = "To join Bean Jam join our Discord Server: https://discord.gg/8jcNWqeQgQ"

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Join Bean Jam", value=text, inline=False)

    await ctx.send(embed=embed)


@client.command()
async def about(ctx):
    text = "Simple bot for Bean Jam and small tasks. Use the **\"help\"** command for help."

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="About", value=text, inline=False)

    await ctx.send(embed=embed)


@client.command()
async def source(ctx):
    text = "Source Code: https://github.com/chivenos/beanbot."

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Source", value=text, inline=False)

    await ctx.send(embed=embed)


async def bean_jam_notifications(): #Bean Jam notifications
    while True:
        now = datetime.utcnow()
        if(now.weekday() == beanJamStartDate[0] and now.hour == beanJamStartDate[1] and now.minute == beanJamStartDate[2]): #bean jam started
            data = selectAllTable("beanjamnotificationchannels")

            for i in data:
                guildid = i[0]
                channelid = i[1]
                guild = client.get_guild(int(guildid))
                role = get(guild.roles, name=f"#BeanJam{client.beanJamCount}")
                if(role == None):
                    role = await guild.create_role(name=f"#BeanJam{client.beanJamCount}")

                channel = client.get_channel(int(channelid))

                embed = discord.Embed(
                    colour=embedColor
                )

                avatarUrl = GetAvatarLink(str(client.user.avatar_url))
                embed.set_author(name=client.user.name,
                                 icon_url=avatarUrl)
                embed.add_field(name="Bean Jam Notification",
                                value=f"**Bean Jam #{client.beanJamCount}** has been started!", inline=False)

                await guild.create_role(name=f"#BeanJam{client.beanJamCount + 1}")
                winnerRole = await guild.create_role(name=f"#BeanJam{client.beanJamCount + 1}Winner")
                await winnerRole.edit(server=guild,role=winnerRole,colour=discord.Colour(winnerYellowColor))

                await channel.send(role.mention)
                await channel.send(embed=embed)

        elif(now.weekday() == beanJamReminderDate[0] and now.hour == beanJamReminderDate[1] and now.minute == beanJamReminderDate[2]): #bean jam starting in an hour
            data = selectAllTable("beanjamnotificationchannels")

            for i in data:
                guildid = i[0]
                channelid = i[1]
                guild = client.get_guild(int(guildid))
                role = get(guild.roles, name=f"#BeanJam{client.beanJamCount}")
                if(role == None):
                    role = await guild.create_role(name=f"#BeanJam{client.beanJamCount}")

                channel = client.get_channel(int(channelid))

                embed = discord.Embed(
                    colour=embedColor
                )

                avatarUrl = GetAvatarLink(str(client.user.avatar_url))
                embed.set_author(name=client.user.name,
                                 icon_url=avatarUrl)
                embed.add_field(name="Bean Jam Notification",
                                value=f"**Bean Jam #{client.beanJamCount}** is starting in an hour!", inline=False)

                await channel.send(role.mention)
                await channel.send(embed=embed)

        elif (now.weekday() == beanJamThemeDate[0] and now.hour == beanJamThemeDate[1] and now.minute == beanJamThemeDate[2]):  #bean jam theme announced
            theme = ReturnRandomTheme()
            data = selectAllTable("beanjamnotificationchannels")

            for i in data:
                guildid = i[0]
                channelid = i[1]
                guild = client.get_guild(int(guildid))
                role = get(guild.roles, name=f"#BeanJam{client.beanJamCount}")
                if(role == None):
                    role = await guild.create_role(name=f"#BeanJam{client.beanJamCount}")

                channel = client.get_channel(int(channelid))

                embed = discord.Embed(
                    colour=embedColor
                )

                avatarUrl = GetAvatarLink(str(client.user.avatar_url))
                embed.set_author(name=client.user.name,
                                 icon_url=avatarUrl)
                embed.add_field(name="Bean Jam Notification",
                                value=f"The theme of **Bean Jam #{client.beanJamCount}** is **\"{theme}\"**!", inline=False)

                await channel.send(role.mention)
                await channel.send(embed=embed)

        elif (now.weekday() == beanJamEndDate[0] and now.hour == beanJamEndDate[1] and now.minute == beanJamEndDate[2]):  # bean jam ended
            data = selectAllTable("beanjamnotificationchannels")

            for i in data:
                guildid = i[0]
                channelid = i[1]
                guild = client.get_guild(int(guildid))

                role = get(guild.roles, name=f"#BeanJam{client.beanJamCount}")
                if (role == None):
                    role = await guild.create_role(name=f"#BeanJam{client.beanJamCount}")

                channel = client.get_channel(int(channelid))

                embed = discord.Embed(
                    colour=embedColor
                )

                avatarUrl = GetAvatarLink(str(client.user.avatar_url))
                embed.set_author(name=client.user.name,
                                 icon_url=avatarUrl)
                embed.add_field(name="Bean Jam Notification",
                                value=f"**Bean Jam #{client.beanJamCount}** is over! Thanks to who joined!", inline=False)

                await channel.send(role.mention)
                await channel.send(embed=embed)

            increaseBeanJamCount()
            client.status[0] = f"Bean Jam #{client.beanJamCount}"

        elif (now.weekday() == beanJamRoleDate[0] and now.hour == beanJamRoleDate[1] and now.minute == beanJamRoleDate[2]):  #bean jam role released
            data = selectAllTable("beanjamnotificationchannels")

            for i in data:
                guildid = i[0]
                channelid = i[1]
                guild = client.get_guild(int(guildid))
                channel = client.get_channel(int(channelid))

                role = get(guild.roles, name=f"#BeanJam{client.beanJamCount}")
                if (role == None):
                    role = await guild.create_role(name=f"#BeanJam{client.beanJamCount}")

                role0 = get(guild.roles, name="#BeanJam")
                if (role0 == None):
                    role0 = await guild.create_role(name="#BeanJam")

                embed = discord.Embed(
                    colour=embedColor
                )

                avatarUrl = GetAvatarLink(str(client.user.avatar_url))
                embed.set_author(name=client.user.name,
                                 icon_url=avatarUrl)
                embed.add_field(name="Bean Jam Notification",
                                value=f"Grab your {role.mention} role and coins!", inline=False)

                await channel.send(guild.default_role)
                msg = await channel.send(embed=embed)
                await msg.add_reaction(checkMarkEmoji)
                deleteDbByName("reactiontorole", f"#BeanJam{client.beanJamCount - 1}")
                insertDbReactiontorole(str(msg.id), str(role.id), str(role0.id), f"#BeanJam{client.beanJamCount}")

        await asyncio.sleep(beanJamNotificationsLoopInterval)

client.loop.create_task(bean_jam_notifications())


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def setBeanJamNotificationsChannel(ctx, channel : discord.TextChannel):
    guild = ctx.guild
    result = selectDbByGuildid("beanjamnotificationchannels", str(guild.id))

    if(result == None):
        insertDbBeanjamnotificationchannels(str(guild.id), str(channel.id))
    else:
        updateDbBeanjamnotificationchannels(str(guild.id), str(channel.id))

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Bean Jam Notification", value=f"Bean Jam Notification Channel Has Been Set As {channel.mention}", inline=False)

    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True) #User must have administrator permission
async def disableBeanJamNotifications(ctx):
    guild = ctx.guild
    deleteDbByGuildid("beanjamnotificationchannels", str(guild.id))

    embed = discord.Embed(
        colour=embedColor
    )

    avatarUrl = GetAvatarLink(str(ctx.author.avatar_url))
    embed.set_author(name=ctx.author.name,
                     icon_url=avatarUrl)
    embed.add_field(name="Bean Jam Notification",
                    value=f"Bean Jam notifications has been disabled.", inline=False)

    await ctx.send(embed=embed)



"""#EMBED TEMPLATE
    embed = discord.Embed(
        title="Title",
        description="This is a description",
        colour=embedColor
    )

    embed.set_footer(text="This is a footer.")
    embed.set_image(url="https://cdn.discordapp.com/attachments/520265639680671747/533389224913797122/rtgang.jpeg")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/520265639680671747/533389224913797122/rtgang.jpeg")
    embed.set_author(name="Author Name",
                     icon_url="https://cdn.discordapp.com/attachments/520265639680671747/533389224913797122/rtgang.jpeg")
    embed.add_field(name="Field Name", value="Field Value", inline=False)
    embed.add_field(name="Field Name", value="Field Value", inline=True)
    embed.add_field(name="Field Name", value="Field Value", inline=True)

    await ctx.send(embed=embed)
"""

# ----
client.run(token)
