from datetime import datetime
from config.functions import *
from discord.ext import commands, tasks





class Tasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.update_last_update.start()
     


    @tasks.loop(seconds=20.0)
    async def update_last_update(self):
        fb_up(now_formated(), 'config', 'last_update')
    
    @update_last_update.before_loop
    async def before_update_last_update(self):
        await self.bot.wait_until_ready()





def setup(bot):
    bot.add_cog(Tasks(bot))
