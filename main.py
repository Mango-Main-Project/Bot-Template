import discord
from discord.ext import commands
from discord.ext.commands import Command, Context

import os
import dotenv

dotenv.load_dotenv()
    
class MyBot(commands.Bot):
    def __init__(self, command_prefix="mb.", intents=discord.Intents.all()) -> None:
        super().__init__(command_prefix=command_prefix, intents=intents)
        self._add_command()

        # For Pylance
        self.bot: commands.Bot

    @property
    def unpreload(self):
        return set()

    async def on_ready(self):
        print(f"Python >> Bot is Ready, Login: {self.user}")
        for dir_cog in os.listdir("./cogs"):
            for cog in os.listdir(f"./cogs/{dir_cog}"):
                if cog.endswith(".py") and cog not in self.unpreload:
                    self.load_extension(f"cogs.{dir_cog}.{cog.removesuffix('.py')}")
                    print(f">>> Load Cog: cogs.{dir_cog}.{cog.removeprefix('.py')}")
    
    def _add_command(self):
        @self.command()
        async def cogs(ctx:Context, cog_name:str, mode:str="load") -> Command:
            path = cog_name.removesuffix(".py").replace("/", ".").replace("\\", ".")
            match mode.lower():
                case "load" | "l":
                    self.load_extension(path)
                    mode = "load"
                case "unload" | "u":
                    self.unload_extension(path)
                    mode = "unload"
                case "reload" | "r":
                    self.reload_extension(path)
                    mode = "reload"
                case _:
                    return await ctx.send(f"> ERROR: mode {mode} is undefined")
            await ctx.send(f"> SUCCESS: cog {cog_name} is has succeeded {mode}")

myBot = MyBot()
myBot.run(os.getenv("TOKEN"))