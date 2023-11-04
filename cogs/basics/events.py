from datetime import datetime
from config.functions import *
from discord.ext import commands
from discord.ext.commands.help import HelpCommand



class Events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    


    @commands.Cog.listener()
    async def on_ready(self):
        fb_up(now_formated(), 'config', 'start_time')
        ready = msg_ready(self.bot, bot_name)
        print(ready)
        if bot_name != 'test':
            for user in fb('config', 'owns'):
                await self.bot.get_user(int(user)).send(ready)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, original_error):  # Show possible errors
        error = getattr(original_error, 'original', original_error)  # Get error
        if isinstance(error, errors_to_disregard): return  # Disregarded errors
        elif isinstance(error, commands.MissingPermissions):  # Without permission
            # Translate error into pt-br
            error2 = str(error).replace('You are missing ', '')
            error2 = error2.replace(' permission(s) to run this command.', '')
            if error2.count(', ') > 5:
                error2 = error2.replace(', ', '')
            error2 = f'`{error2.lower()}`'
            if len(error2.split()) == 2:
                error2 = error2.replace('and ', '')
            if error2.count(' or') > 0 and error2.count('and ') > 0:
                error2 = error2.replace('and ', '')
            error2 = f'Você deve ter as permissões de {error2} para executar esse comando.'
            reply_msg = await ctx.send(error2)  # Send error
            await delete_time(reply_msg, ctx)
        elif isinstance(error, commands.MissingRequiredArgument):  # Needs arguments
            error2 = str(error).replace('is a required argument that is missing.',
                'é um argumento necessário.')  # Translate error into pt-br
            reply_msg = await ctx.send(error2)  # Send error
            await delete_time(reply_msg, ctx)
        elif isinstance(error, commands.NoPrivateMessage):  # Only guilds
            reply_msg = await ctx.send('Esse comando só pode ser executado em servidores.')
            await delete_time(reply_msg, ctx)
        elif isinstance(error, commands.MemberNotFound):  # Member does not exist
            # Translate error into pt-br
            reply_msg = str(error).replace('Member "', '')
            reply_msg = reply_msg.replace('" not found.', '')
            reply_msg = await ctx.send(f'Membro "{reply_msg}" não encontrado.')
            await delete_time(reply_msg, ctx)
        else:
            # Send error to owner
            try: 
                for user in fb('config', 'owns'):
                    await self.bot.get_user(user).send(f'Erro registrado - {now_formated()} - {str(error)}')
            except: pass
            raise error



    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        g = ctx
        gi = g.id
        ban_guilds = fb('config', 'ban_guilds')
        if ban_guilds is not None:  # Check ban guilds
            if str(gi) in ban_guilds:
                await g.leave()
                return
        # Notify owner of new entry
        await self.bot.get_user(own).send(f'Join in {g.name} ({gi})')
        if fb('guilds', gi) is not None: return  # Check configurate guild
        for channel in g.channels:  # find commands chat
            # Instructs configuration
            if str(channel.name).count('comando') > 0 or str(channel.name).count('command') > 0:
                reply_msg = await channel.send(
                    'Olá! Obrigado por me adicionar. '\
                    'Para que eu possa responder apenas nos canais desejados, favor digitar '\
                    f'{get_prefix(bot=self.bot, channel=channel, guild=g)}'\
                    'set canais <id(s) do(s) channel(is)>'
                )
                await delete_time(reply_msg, ctx)
                return
                


    @commands.Cog.listener()
    async def on_message(self, message):  # Respond to mentions
        g = message.guild
        if message.content in [f'<@{self.bot.user.id}>', f'<@!{self.bot.user.id}>']:
            prefix = get_prefix(self.bot, message)
            reply_msg = await message.channel.send('Meu prefixo '\
                f'{"neste servidor " if g is not None else ""}'\
                f'é `{prefix}`. Para mais informações, use `{prefix}help`')
            await delete_time(reply_msg, guild=g, message=message)





def setup(bot):
    bot.add_cog(Events(bot))
