from config.functions import *
from discord.ext import commands




class HBasic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    


    # Ping
    @commands.hybrid_command(name='ping', description='Tempo de resposta do bot')
    async def ping(self, ctx):
        reply_msg = await ctx.send(
            f'Pong :ping_pong:: A latência da API é de {int(self.bot.latency*1000)}ms')
        await reply_msg.edit(content=f'Pong :ping_pong:: A minha latência é de '\
            f'{int((reply_msg.created_at-ctx.message.created_at).microseconds/1000)}ms e '\
            f'a da API é de {int(self.bot.latency*1000)}ms.')
        await delete_time(reply_msg, ctx)



def setup(bot):
    bot.add_cog(HBasic(bot))
