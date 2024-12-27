import discord
from discord.ext import commands
import random
import requests
import os
import string
import time
import asyncio

prefix = '$'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, self_bot=True, intents=intents)

snipe_messages = {}
skull_mode = False
mimic_users = {}
stream_url = 'https://www.twitch.tv/Gay_Nigger?tt_content=channel&tt_medium=mobile_web_share'
reacting_to = {}

@bot.remove_command('help')
@bot.event
async def on_ready():
    print(f'{bot.user.name}, cmd is "$basics" type it in any dms or server to see everything')
    
@bot.event
async def on_message(message):
    global skull_mode
    global reacting_to
    global mimic_users

    if message.author == bot.user:
        if skull_mode:
            await message.add_reaction("☠️")
    elif message.author.id in mimic_users.values():
        await message.channel.send(f'{message.clean_content}')
    elif message.author.id in reacting_to:
        try:
            await message.add_reaction(reacting_to[message.author.id])
        except discord.Forbidden:
            print(f"Cannot react to {message.author.name}'s message in {message.channel.name} (no permission)")
        except discord.HTTPException as e:
            print(f"Error reacting to {message.author.name}'s messages: {e.text}")
    await bot.process_commands(message)
    
@bot.event
async def on_message_delete(message):
    snipe_messages[message.channel.id] = message
    
@bot.command(aliases=["skullreact"])
async def autoskullon(ctx):
    global skull_mode
    skull_mode = True
    await ctx.send("autoskull now on")

@bot.command(aliases=["stopskullreact"])
async def autoskulloff(ctx):
    global skull_mode
    skull_mode = False
    await ctx.send("autoskull now off")
    
@bot.command()
async def pcstatus(ctx):
    await bot.change_presence(status=discord.Status.online)
    await ctx.send('Changed To **Pc Online Status**')
    
@bot.command()
async def radd(ctx, user: discord.User=None, emoji: str=None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(f'[Invalid]: {bot.command_prefix}radd <user> <emoji>')
        return
        if emoji is None:
            await ctx.send(f'[Invalid]: {bot.command_prefix}radd <user> <emoji>')
            return
    global reacting_to
    reacting_to[user.id] = emoji
    await ctx.send(f'Reacting to {user.name}\'s messages with {emoji}')

@bot.command()
async def rstop(ctx, user: discord.User=None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(f'[Invalid]: {bot.command_prefix}rstop <user>')
        return
    global reacting_to
    if user.id in reacting_to:
        del reacting_to[user.id]
    await ctx.send(f'Reaction stopped for {user.name}')
    
@bot.command()
async def mimicon(ctx, user: discord.User=None):
    if user is None:
        await ctx.send(f'[Invalid]: {bot.command_prefix}mimicon <user>')
        return
    mimic_users[ctx.author.id] = user.id
    await ctx.send(f'mimicking {user.name}')

@bot.command()
async def mimicoff(ctx):
    if ctx.author.id in mimic_users:
        del mimic_users[ctx.author.id]
        await ctx.send('stopped mimicking bru')
    else:
        await ctx.send('youre not mimicking any1 rn')
        
@bot.command()
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Pinging...")
    ping = (time.monotonic() - before) * 1000
    lol = ["north korea", "gay", "bangladesh", "your ass", "pink pussy", "fan", "jotaro", "dio the lord", "dogs", "fucking nigger", "hell", "kim jong un", "putin", "osama", "terror1sts", "nothing", "smd", "mcdonalds employee (you)", "fat dick", "black nigga", "fat buffed guys", "gay mfs", "your grandma", "jesus", "ping", "rapers", "rappers", "sybau"]
    await message.edit(content=f"`{int(ping)}ms to ping {random.choice(lol)}`")
      
@bot.command(name='say')
async def say(ctx, times: int=None, *, message=None):
    await ctx.message.delete()
    if times is None:
        await ctx.send(f'[Invalid]: Command: {bot.command_prefix}say <times> <message>')
        return
        if message is None:
            await ctx.send(f'[Invalid]: Command: {bot.command_prefix}say <times> <message>')
            return
    for _ in range(times):
        await ctx.send(message)  
        
@bot.command(aliases=['s'])
async def snipemsg(ctx):
    channel_id = ctx.channel.id
    if channel_id in snipe_messages:
        deleted_message = snipe_messages.pop(channel_id)
        await ctx.send(f"**{deleted_message.author.name}** deleted a message: `{deleted_message.clean_content}`")
        if deleted_message.attachments:
            attachment_links = "\n".join([f"[{a.filename}]({a.url})" for a in deleted_message.attachments])
            await ctx.send(f"Deleted attachments:\n{attachment_links}")
    else:
        await ctx.send(f'No Deleted Messages Lol')
        
@bot.command(name='basics')
async def basics(ctx):
        basics = "```Partly runs ts shi```" "```1 - prefix (changes prefix ex prefix any special character)\n\n2 - say, repeats the word with a number of times\n\n3 - pack, give random insults mentioned user\n\n4 - stream, streams a twitch status in your profile (stopstream for stopping your current stream.)\n\n5 - mdm, - mass dm a message in your choice.\n\n6 - massgc, send message in every group chat that youre in.\n\n7 - autoskull, react on your messages with a skull emoji (on or off)\n\n8 - mimic, copy mentioned users message (on or off)\n\n9 - others for other cmds```"
        await ctx.send(basics)
        
@bot.command(name='others')
async def others(ctx):
        others = "```Partly runs this.```" "```1 - nitro, generate random nitro code (99percent wont give a working nitro)\n\n2 - cum\n\n3 - dick, shows mentioned user dick size\n\n4 - nine_11, starts 9/11\n\n5 - hack, hacks any mentioned user\n\n6 - playing, makes your status playing any game\n\n7 - watching, make you watch anything in your status\n\n8 - listening, changes your status to listening.\n\n9 - purge, clears messages\n\n10 - gctrap, trap any1 in a gc\n\n11 - stopstatus, stops your current status\n\n12 - av, shows avatar\n\n13 - snipemsg, snipes deleted messages\n\n14 - ping, pings sb\n\n15 - radd, reacts on any1s message\n\n16 - rstop, stop reacting on mentioned users msg```"
        await ctx.send(others)
        
@bot.command(name='pack', help='throws random insults on mentioned user')
async def pack(ctx, member: discord.Member=None):
    await ctx.message.delete()
    if member is None:
        await ctx.send(f'[Invalid]: mention a user')
        return
    insults = ["# SHUT THE FUCKUP YOU NASTY NIGGA ", "# UR MY BITCH", "# LOL WHY THIS NN TALKING TM", "# SHUT YO LAME ASS UP NIGGA", "# DONT TALK", "DORK ASS CUNT", "BLA BLA BLA GTFO NIGGA", "SHUT THE FUCK UP YOU NASTY BITCH YOUR MY SON I RUN YOU FAT ASS WHORE GO KYS DUMB ASS FAGGG LMFOAOAOO", "UR MY BITCH", "DUMB ASS NIGGA", "?", "UR MY WHORE", "NIGGA GETTING SMOKED:rofl:", "NIGGA U DIED TO ME", "I PUTTED ON YO MOTHER AND CUMMED INSIDE HER AND U WAS BORN SON", "UR A NERD", "🤓", "YAPPER:rofl:", "NIGGA FOLDED TO ME", "PIPE THE FUCK DOWN", "I OWN U SON", "YOUR SLOW ASFUCK BITCH", "UR MY DOG", "LMFAO", "I DONT KNOW U, NO ONE KNOWS YOU UNKNOWNWNWNNWNWN ASS NIGGA", "FAT ASS CUNT ", "NIGGA TRIED STEPPING", "HOW DID U GET HOED LIKE THAT", "FAT ASS PIG LMFAOAOO", "I DONT FOLD", "SHUT THE FUCK UP", "TRY STEPPING AGAIN", "UR A BITCH", "DUMB ASS NIGGA", "YOU GOT IN HERE TO GET FUCKED BY ME BITCHASS NIGGA", "SHUT THE FUCKUP YOU NASTY NIGGA ", "UR MY BITCH", "LOL", "SHUT YO LAME ASS UP NIGGA", "DONT TALK", "DORK ASS CUNT", "BLA BLA BLA GTFO NIGGA", "SHUT THE FUCK UP YOU NASTY BITCH YOUR MY SON I RUN YOU FAT ASS WHORE GO KYS DUMB ASS FAGGG LMFOAOAOO", "UR MY BITCH", "DUMB ASS NIGGA", "?", "UR MY WHORE", "NIGGA GETTING SMOKED:rofl:", "NIGGA SMD", "GAY ASS FAG:skull:", "I OWN YO MOTHER", "🤓", "YAPPER:Laughing:", "NIGGA STOP THIS YAP", "LMAOFAOO WHY YOU YAPPING", "I OWN U", "SON", "YOUR GETTING SONNED LMFAOO", "🤣", "GAY ASS BITCH", "FAT FUCK", "DONT TALK BACK YOU LOSIN", "IMAGINE BEING YOU (DONT WANNA IMAGINE)", "# R U GONNA LET DAT SLIDE ASSHOLE?", "# LMAOOO YOUR GETTING SMOKED REAL HARD", "DONT TYPE PUSSY", "# YAP?", "# MY WHORE", "# OK BITCH", "# STFU ASSHOLE"]
    for _ in range(100):
        await ctx.send(f'# {member.mention} {random.choice(insults)}')

@bot.command(aliases=["twitch"])
async def stream(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[invalid]: bro this is the command: {bot.command_prefix}stream <message>')
        return
    stream = discord.Streaming(name=message, url=stream_url)
    await bot.change_presence(activity=stream)
    await ctx.send(f"now streaming **{message}**")
    
@bot.command(aliases=["stopstreaming"])
async def stopstream(ctx):
        
    await bot.change_presence(activity=None)
    await ctx.send("Streaming stopped.")

@bot.command(name='prefix')
async def prefix(ctx, new_prefix=None):
    await ctx.message.delete()
    if new_prefix is None:
        await ctx.send(f'[Invalid]: nigga Its {bot.command_prefix}prefix <prefix>')
        return
    bot.command_prefix = str(new_prefix)
    await ctx.send(f'Prefix changed to {new_prefix}')

@bot.command()
async def hosttest(ctx):
    await ctx.send(f"```@{bot.user.name} selfbot succesfully hosted, type {bot.command_prefix}help to preview all the commands.```")

@bot.command()
async def nitro(ctx, amount: int=None):
    await ctx.message.delete()
    if amount is None:
        await ctx.send(f'[Invalid]: dawg Its {bot.command_prefix}nitro <amount>')
        return
    for _ in range(amount):
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        await ctx.send(f'https://discord.gift/{code}')
        await asyncio.sleep(0.50)
        
@bot.command()    
async def dick(ctx, *, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    size = random.randint(1, 15)
    dong = ""
    for _i in range(0, size):
        dong += "="
    await ctx.send(f"**{user}**'s Dick size\n8{dong}D")
    
@bot.command(aliases=['clear', 'c'])
async def purge(ctx, amount: int=None):
    await ctx.message.delete()
    if amount is None:
        await ctx.send(f'[invalid]: Command: {bot.command_prefix}purge <amount>')
        return
    async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == bot.user).map(
            lambda m: m):
        try:
            await message.delete()
        except:
            pass
            
@bot.command(aliases=['watch'])
async def watching(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[invalid]: Command: {bot.command_prefix}watch <message>')
        return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=message))
    await ctx.send(f'now watching **{message}**')
    
@bot.command(aliases=['listen'])
async def listening(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[invalid]: Command: {bot.command_prefix}listening <message>')
        return
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message))
    await ctx.send(f'now listening to **{message}**')
    
@bot.command(aliases=['play'])
async def playing(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[invalid>: Command: {bot.command_prefix}playing <message>')
        return
    game = discord.Game(name=message)
    await bot.change_presence(activity=game)
    await ctx.send(f'now playing **{message}**')
  
@bot.command(aliases=['stopstatus'])
async def stopactivity(ctx):
        await ctx.message.delete()
        await bot.change_presence(activity=None)
        await ctx.send(f'stopped your current activity')
        
@bot.command()
async def gctrap(ctx, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(f'[Invalid]: Command: {bot.command_prefix}gctrap <user>')
        return
    count = 0
    while True:
        count += 1
        await ctx.channel.edit(name=f"{user.display_name} got owned {count}")
        await asyncio.sleep(0.50)
   
@bot.command(aliases=["av"])
async def avatar(ctx, member: discord.Member = None):
    await ctx.message.delete()
    if member is None:
        member = ctx.author

    avatar_url = member.avatar_url
    await ctx.send(avatar_url)
        
@bot.command(name='massgc')
async def massgc(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[Invalid]: Nuh, Command: {bot.command_prefix}massgc <message>')
        return
    await ctx.send('Sending message to all group chats...')
    for channel in bot.private_channels:
        if isinstance(channel, discord.GroupChannel):
            try:
                await channel.send(message)
                print(f'Message sent to {channel.name}')
            except discord.Forbidden:
                print(f'Forbidden to send message to {channel.name}')
            except discord.HTTPException as e:
                print(f'Error sending message to {channel.name}: {e.text}')
    await ctx.send('Message sent to all group chats!')
    await asyncio.sleep(0.50)
    
@bot.command()
async def mdm(ctx, *, message=None):
    await ctx.message.delete()
    if message is None:
        await ctx.send(f'[Invalid]: It\'s, {bot.command_prefix}mdm <message>')
        return  
    for friend in bot.user.friends:
        try:
            await friend.send(message)
            print(f"message sent to {friend.name}#{friend.discriminator}")
        except discord.Forbidden:
            print(f"Failed to send message to {friend.name}#{friend.discriminator} (blocked or dms are off)")
        except Exception as e:
            print(f"error sending message to {friend.name}#{friend.discriminator}: {e}")
        await asyncio.sleep(7)
        
@bot.command() 
async def nine_11(ctx):
    await ctx.message.delete()
    invis = ""  # char(173)
    message = await ctx.send(f'''
{invis}:man_wearing_turban::airplane:    :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis} :man_wearing_turban::airplane:   :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}  :man_wearing_turban::airplane:  :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}   :man_wearing_turban::airplane: :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}    :man_wearing_turban::airplane::office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
        :boom::boom::boom:    
        ''')
        
@bot.command()
async def cum(ctx):
    await ctx.message.delete()
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:   
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant: 
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:    
             ''')
    await asyncio.sleep(0.5)
    await message.edit(contnet='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:        
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
     
bot.command()
async def hack(ctx, user: discord.Member=None):
    await ctx.message.delete()
    gender = ["Male", "Female", "Trans", "Other", "Retard"]
    age = str(random.randrange(10, 25))
    height = ['4\'6\"', '4\'7\"', '4\'8\"', '4\'9\"', '4\'10\"', '4\'11\"', '5\'0\"', '5\'1\"', '5\'2\"', '5\'3\"',
              '5\'4\"', '5\'5\"',
              '5\'6\"', '5\'7\"', '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '6\'0\"', '6\'1\"', '6\'2\"', '6\'3\"',
              '6\'4\"', '6\'5\"',
              '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"', '6\'10\"', '6\'11\"']
    weight = str(random.randrange(60, 300))
    hair_color = ["Black", "Brown", "Blonde", "White", "Gray", "Red"]
    skin_color = ["White", "Pale", "Brown", "Black", "Light-Skin"]
    religion = ["Christian", "Muslim", "Atheist", "Hindu", "Buddhist", "Jewish"]
    sexuality = ["Straight", "Gay", "Homo", "Bi", "Bi-Sexual", "Lesbian", "Pansexual"]
    education = ["High School", "College", "Middle School", "Elementary School", "Pre School",
                 "Retard never went to school LOL"]
    ethnicity = ["White", "African American", "Asian", "Latino", "Latina", "American", "Mexican", "Korean", "Chinese",
                 "Arab", "Italian", "Puerto Rican", "Non-Hispanic", "Russian", "Canadian", "European", "Indian"]
    occupation = ["Retard has no job LOL", "Certified discord retard", "Janitor", "Police Officer", "Teacher",
                  "Cashier", "Clerk", "Waiter", "Waitress", "Grocery Bagger", "Retailer", "Sales-Person", "Artist",
                  "Singer", "Rapper", "Trapper", "Discord Thug", "Gangster", "Discord Packer", "Mechanic", "Carpenter",
                  "Electrician", "Lawyer", "Doctor", "Programmer", "Software Engineer", "Scientist"]
    salary = ["Retard makes no money LOL", "$" + str(random.randrange(0, 1000)), '<$50,000', '<$75,000', "$100,000",
              "$125,000", "$150,000", "$175,000",
              "$200,000+"]
    location = ["Retard lives in his mom's basement LOL", "America", "United States", "Europe", "Poland", "Mexico",
                "Russia", "Pakistan", "India",
                "Some random third world country", "Canada", "Alabama", "Alaska", "Arizona", "Arkansas", "California",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
                "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
                "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    email = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@protonmail.com", "@disposablemail.com",
             "@aol.com", "@edu.com", "@icloud.com", "@gmx.net", "@yandex.com"]
    dob = f'{random.randrange(1, 13)}/{random.randrange(1, 32)}/{random.randrange(1950, 2021)}'
    name = ['James Smith', "Michael Smith", "Robert Smith", "Maria Garcia", "David Smith", "Maria Rodriguez",
            "Mary Smith", "Maria Hernandez", "Maria Martinez", "James Johnson", "Catherine Smoaks", "Cindi Emerick",
            "Trudie Peasley", "Josie Dowler", "Jefferey Amon", "Kyung Kernan", "Lola Barreiro",
            "Barabara Nuss", "Lien Barmore", "Donnell Kuhlmann", "Geoffrey Torre", "Allan Craft",
            "Elvira Lucien", "Jeanelle Orem", "Shantelle Lige", "Chassidy Reinhardt", "Adam Delange",
            "Anabel Rini", "Delbert Kruse", "Celeste Baumeister", "Jon Flanary", "Danette Uhler", "Xochitl Parton",
            "Derek Hetrick", "Chasity Hedge", "Antonia Gonsoulin", "Tod Kinkead", "Chastity Lazar", "Jazmin Aumick",
            "Janet Slusser", "Junita Cagle", "Stepanie Blandford", "Lang Schaff", "Kaila Bier", "Ezra Battey",
            "Bart Maddux", "Shiloh Raulston", "Carrie Kimber", "Zack Polite", "Marni Larson", "Justa Spear"]
    phone = f'({random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)})-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}'
    if user is None:
        user = ctx.author
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```")
    else:
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`")
        await asyncio.sleep(1)
        await message.edit(
    content=f"```Successfully hacked {user}\n"
            f"Name: {random.choice(name)}\n"
            f"Gender: {random.choice(gender)}\n"
            f"Age: {age}\n"
            f"Height: {random.choice(height)}\n"
            f"Weight: {weight}\n"
            f"Hair Color: {random.choice(hair_color)}\n"
            f"Skin Color: {random.choice(skin_color)}\n"
            f"DOB: {dob}\n"
            f"Location: {random.choice(location)}\n"
            f"Phone: {phone}\n"
            f"E-Mail: {user.name + random.choice(email)}\n"
            f"Passwords: {', '.join(random.choices(password, k=3))}\n"
            f"Occupation: {random.choice(occupation)}\n"
            f"Annual Salary: {random.choice(salary)}\n"
            f"Ethnicity: {random.choice(ethnicity)}\n"
            f"Religion: {random.choice(religion)}\n"
            f"Sexuality: {random.choice(sexuality)}\n"
            f"Education: {random.choice(education)}\n"
            "```"
)
        
 
bot.run("OTY1NTc3MTE2OTQ1MDk2NzI0.GtRMsC.kzHwmGGB9l_D2mKiBLBKTC8mwfKyDIN0Zv87vY", bot=False)