from keep_alive import keep_alive
import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
from datetime import timedelta

client = discord.Client()
bot = commands.Bot(".")

## Logon
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

## Resolved Fun
@client.event
async def resolvedFun(message,ask_here_cat,answered_questions_cat,channelName):
    print('Running resolveFun, sending message and moving to answered, then sleeping!')
    pins = await message.channel.pins()
    if len(pins) > 0:
      msg_to_unpin = pins[0]
    else:
      msg_to_unpin = 'Err'
    print(pins)
    await message.channel.send("[WARN429] I can't update your question right now due to Discord's rate limit for bots, but I will as soon as I'm able!")
    if msg_to_unpin != 'Err':
      try:
        await msg_to_unpin.unpin()
      except:
        print("Couldn't find message to unpin.")
    ## If ratelimited, will pause here
    await message.channel.edit(topic='Claim this channel by typing a question!',name=channelName, category = answered_questions_cat, sync_permissions = True)
    await message.channel.send("""Have questions or need help with a problem or specific topic? Ask here and be patient for a response. Remember to: \n • Ask your question straight away, rather than asking \'can anyone help\' \n • State the general concept/topic/chapter numbers (if applicable) \n • Tell us what you\'ve tried so far, or what your thought process is\n • The channel will be turned into your question when you type\n • Remember to free-up the channel with :resolved: when done""")
    ## Wait 10 Minutes to  recycle channel.
    await asyncio.sleep(600)
    print('Done sleeping! Moving to ask_here_cat now!')
    await message.channel.edit(category = ask_here_cat, sync_permissions = True)

## Timeout Check
@client.event
async def timeoutCheck(guild,active_questions_cat):
  try:
    for channel in active_questions_cat.text_channels:
      last_message_id = channel.last_message_id
      last_message = await channel.fetch_message(last_message_id)
      last_message_time = last_message.created_at
      if ((datetime.now() - last_message_time) > timedelta(hours=3)) & (last_message.author != client.user):
        await channel.send(f"<@{int(channel.topic)}>, is your question resolved? If so, please close this channel by sending the message \":resolved:\"! If not, you can ignore this.")
  except:
    print("Error in timeout check, likely no active questions.")

@client.event
async def on_message(message):
    print('Running on_message \n')
    ## Check if bot
    if message.author == client.user and message.content.startswith('[WARN429]'):
        print('This was the bot sending a [WARN429], sleeping.')
        await asyncio.sleep(600)
        print('Done sleeping! Deleting the WARN now.')
        await message.delete()
        await bot.process_commands(message)
        return

    if message.author == client.user:
        print('This was the bot, returning. \n')
        return

    ## Not the bot- assign guild and check if setup
    guild = message.guild

    if message.content.startswith("jb!setup") & message.author.guild_permissions.administrator:
      await guild.create_role(name="Jonbot Commander")
      await guild.create_category(name='ACTIVE QUESTIONS')
      new_ask_here_cat = await guild.create_category(name='ASK HERE')
      await guild.create_category(name='ANSWERED QUESTIONS')
      for x in range (1,5):
        await guild.create_text_channel(topic='Claim this channel by typing a question!',name='👋ask-here', category = new_ask_here_cat)
      await message.channel.send("Categories, channels, and roles created. Assign users who can resolve questions the \"Jonbot Commander\" role. Feel free to also make your own custom :resolved: emoji, if you haven't already.")
    if(message.content.startswith("jb!setup") and not(message.author.guild_permissions.administrator)):
        await message.channel.send("Only an Admin is allowed to use this command!")

    ## Not setup either, assign everything else to memory
    ask_here_cat = discord.utils.get(guild.categories, name='ASK HERE')
    tutor_here_cat = discord.utils.get(guild.categories, name='ASK TUTOR HERE')
    active_questions_cat = discord.utils.get(guild.categories, name='ACTIVE QUESTIONS')
    answered_questions_cat = discord.utils.get(guild.categories, name='ANSWERED QUESTIONS')
    try:
      active_tutor_cat = discord.utils.get(guild.categories, name='TUTORING')
      answered_tutor_cat = discord.utils.get(guild.categories, name='ANSWERED TUTOR QUESTIONS')
    except:
      print("No tutor cats found.\n")  
    commander_role = discord.utils.get(guild.roles, name="Jonbot Commander")
    resolved_emoji = discord.utils.get(guild.emojis, name="resolved")
    print('Not the bot, assigned guild, askHereCat, and activeQuestionsCat \n')
    if type(message.channel.topic) == str:
      if str.isdigit(message.channel.topic):
        authorID = int(message.channel.topic)
      else:
        authorID = 'Err'  
    else:
      authorID = 'Err'

    ## New question opened
    if message.channel.category == ask_here_cat:
        print('Message in askHereCat, moving on. \n')
        asker_name = message.author.name
        await message.pin()
        await message.channel.edit(topic=message.author.id,name='💬{}\'s-question.'.format(asker_name),category = active_questions_cat,sync_permissions = True)

    ## New tutor question opened
    if message.channel.category == tutor_here_cat:
        print('Message in tutorHereCat, moving on. \n')
        asker_name = message.author.name
        await message.pin()
        await message.channel.edit(topic=message.author.id,name='💬{}\'s-question.'.format(asker_name),category = active_tutor_cat,sync_permissions = True)
        await message.channel.set_permissions(message.author, read_messages = True, send_messages = True)

    ## Old question closed
    if ((message.content.startswith(f'<:resolved:{resolved_emoji.id}>') or message.content.startswith(':resolved:')) and (message.channel.category_id == active_questions_cat.id) and ((message.author.id == authorID or (commander_role in message.author.roles)))):
      print('Message is resolved in activeQuestionsCat, running resolvedfun. \n')
      await resolvedFun(message,ask_here_cat,answered_questions_cat,'👋ask-students-here')

    ## Old tutor question closed
    if ((message.content.startswith(f'<:resolved:{resolved_emoji.id}>') or message.content.startswith(':resolved:')) and (message.channel.category_id == active_tutor_cat.id) and ((message.author.id == authorID or (commander_role in message.author.roles)))):
      print('Message is resolved in activeTutorsCat, running resolvedfun for tutors. \n')
      await message.channel.purge(bulk=True)
      await resolvedFun(message,tutor_here_cat,answered_tutor_cat,'👋ask-tutor-here')
      
    ## Old question closed, but userID was stored incorrectly.
    if ((message.content.startswith(f'<:resolved:{resolved_emoji.id}>') or message.content.startswith(':resolved:')) and ((message.channel.category_id == active_questions_cat.id) or (message.channel.category_id == active_tutor_cat.id))and ((authorID == 'Err') and not(commander_role in message.author.roles))):
        await message.channel.send('Hmm. I\'m sorry- I messed up somewhere and can\'t seem to tell who the original author of this message was! Please tell a Bot Manager to resolve this question for you.')
        return

    ## Old question attempted to close, but not enough perms
    if (message.content.startswith(f'<:resolved:{resolved_emoji.id}>') or message.content.startswith(':resolved:')) and ((message.channel.category_id == active_questions_cat.id) or (message.channel.category_id == active_tutor_cat.id)) and message.author.id != authorID:
        print('Message is resolved and not the author. \n')
        await message.channel.send('Only the question author or an approved bot manager can close an open question.')
    
    ## Done with everything important, throw in a check to see if any questions are dormant
    await timeoutCheck(guild,active_questions_cat)
    await timeoutCheck(guild,active_tutor_cat)  

# Put your bot token in a poetry lock
keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)


