import os
from discord.ext import commands

import utils.func as utils

config = utils.jload(file='./config', mode='r', encoding='utf8')

bot = commands.Bot(
    command_prefix = config['commands.prefix'],
    Intents = utils.get_intents(config['commands.intents'])
    )

@bot.event
async def on_ready():
    print('> Bot is Ready')
    for filename in os.listdir('./cogs'):
        if filename[-3:] == '.py':
            bot.load_extension(f'cogs.{filename}')

bot.run(utils.load_file_name(file='./token'))
