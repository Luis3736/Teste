import os
import asyncio
import discord
import traceback
from pathlib import Path
from config.functions import *
from discord.ext import commands



# Basic definitions
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all(),
    case_insensitive=True,
    help_command=commands.MinimalHelpCommand()
)
bot._BotBase__cogs  = commands.core._CaseInsensitiveDict()
#bot.remove_command('help')  # remove default command help
main = os.path.dirname(os.path.abspath(__file__))  # current path
cogs_path = os.path.join(main, 'cogs')



# Beginning of the bot

# load or unload cogs_path
async def cogs_function(cogs = '', all_cog = False, load = True, dir_cog = cogs_path, return_out = ''):
    cogs_split = cogs.split()
    for index in range(len(cogs_split)):  # Turns cog into files
        if not cogs_split[index].endswith('.py'):
            cogs_split[index] += '.py'
    for item in os.listdir(dir_cog):  # See directory files
        file = Path(os.path.join(dir_cog, item))
        if file.is_dir():  # If it is directory, call function for that directory
            load_dir = False
            if item in cogs or all_cog:
                load_dir = True
            return_out = cogs_function(cogs, load_dir, load, os.path.join(dir_cog, item), return_out)
        elif item in cogs_split or all_cog:
            try:
                if item.endswith('.py'):  # Check if it's a cog
                    # change absolute path for relative
                    current_dir = dir_cog.replace(main, "").replace("\\", ".").replace("/", ".")[1:]
                    # (Un)load cog without .py
                    if load:
                        await bot.load_extension(f'{current_dir}.{item[:-3]}')
                    else:
                        await bot.unload_extension(f'{current_dir}.{item[:-3]}')
                    # Return sucess for this cog
                    return_out += f'Cog `{str(item)}` {"adicionado" if load else "removido"} com sucesso!\n'
            # Return failure for this cog
            except commands.errors.ExtensionAlreadyLoaded: 
                return_out += f'O cog `{str(item)}` já estava {"adiciondado" if load else "removido"}.\n'
            except commands.errors.ExtensionNotFound:
                return_out += f'O cog `{str(item)}` não existe.\n'
            except commands.errors.NoEntryPointError:
                return_out += f'O cog `{str(item)}` não tem uma função setup.\n'
            except Exception:
                return_out += f'Desculpe, não consegui {"adicionar" if load else "remover"}'\
                f' o cog `{str(item)}`.\n'
                traceback.print_exc()
    return return_out



# Check owner and (un)load cog(s)
async def load_or_unload(ctx, cog, load = True):
    if str(ctx.author.id) in fb('config', 'owns'):   
        if cog in ['all', 'tudo', 'cogs']:  # (Un)load all extenions
            return_out = await cogs_function(all_cog = True, load = load)
        else:  # (Un)load especific cog
            return_out = await cogs_function(cog, load = load)
        if return_out == '':
            return_out = 'Nada foi encontrado...'
        reply_msg = await ctx.send(return_out)
        await delete_time(reply_msg, ctx)



# Load cog command
@bot.command(aliases=['carregar'], brief='Carrega cog(s) determinado(s)',
    usage='<cog/option/dir> [cogs/dir]',
    help='Carrega cogs não carregados/descarregados. Pode ser usada a opção all/todos/cogs para '\
        'carregar todos os cogs existentes. Pode-se ainda usar o parâmetro dir com o nome de um '\
        'diretório, carregando, pois, todos os cogs existentes nele.\n'\
        'Para conferir os cogs carregados, execute `cogs`.')
async def load(ctx, *, cog):
    await load_or_unload(ctx, cog=cog)
        


# Unload cog command
@bot.command(aliases=['descarregar'], brief='Descarrega cog(s) determinado(s)',
    usage='<cog/option/dir> [cogs]',
    help='Descarrega cogs carregados. Pode ser usada a opção all/todos/cogs para '\
        'descarregar todos os cogs existentes. Pode-se ainda usar o parâmetro dir com o nome de um '\
        'diretório, descarregando, pois, todos os cogs existentes nele.\n'\
        'Para conferir os cogs carregados, execute `cogs`.')
async def unload(ctx, *, cog):
    await load_or_unload(ctx, cog=cog, load = False)



# Reload cog command
@bot.command(aliases=['recarregar'], brief='Recarrga cog(s) determinado(s)',
    usage='<cog/option/dir> [cogs]',
    help='Recarrega cogs carregados (descarrega e carrega novamente). '\
        'Pode ser usada a opção all/todos/cogs para recarregar todos os cogs existentes. '\
        'Pode-se ainda usar o parâmetro dir com o nome de um diretório, recarregando, '\
        'pois, todos os cogs existentes nele.\n'\
        'Para conferir os cogs carregados, execute `cogs`.')
async def reload(ctx, *, cog):
    await load_or_unload(ctx, cog=cog, load = False)
    await load_or_unload(ctx, cog=cog)



# Show cogs_path command
@bot.command(aliases=['cogs'], brief='Mostra pasta cogs', 
    help='Mostra árvore de arquivos da pasta cogs. Cogs carregados aparecerão em verde e com um "+" '\
        'no início da linha.\nPara (des/re)carregar um cog, execute `(des/re)carregar <cog>`.')
async def show_cogs(ctx):
    if str(ctx.author.id) in fb('config', 'owns'):
        cogs_ativos = []
        for cog in (list(bot.cogs.items()) + [('help', bot.help_command)]):
            current_cog = list(cog[1].__class__.__name__)
            for index in range(len(current_cog)):
                if current_cog[index].isupper() and index > 0:
                    current_cog[index - 1] += '_'
            current_cog = ''.join(current_cog)
            cogs_ativos.append((current_cog.lower()) + '.py')
        msg = tree(cogs_path)
        for cog in cogs_ativos:
            position = msg.find(cog)
            if position != -1:
                beginning_msg = msg[:position]
                last_enter_before_cog = len(beginning_msg) - beginning_msg[::-1].find('\n')
                end_msg = msg[position:]
                first_enter_after_cog = len(beginning_msg) + end_msg.find('\n')
                line = msg[last_enter_before_cog:first_enter_after_cog]
                new_line = '+' + msg[last_enter_before_cog + 1:first_enter_after_cog]
                if cog.count('help') > 0:
                    new_line += ' - (Não é um cog)'
                msg = msg.replace(line, (new_line))
        reply_msg = await ctx.send(('```diff\n' + msg + '\n```'))
        await delete_time(reply_msg, ctx)



# Init of all cogs
asyncio.run(cogs_function(all_cog = True))



# Avoid commands outside selected channels
@bot.event
async def on_message(message):
    if message.guild is not None:
        chats_comandos = fb('guilds', message.guild.id, 'config', 'command_channels')
        if chats_comandos is not None:
            if str(message.channel.id) not in chats_comandos:
                return
    
    await bot.process_commands(message)



# Bot init
bot.run(str(fb('config', 'token')).replace(f'==> ANTI-PRINT {"="*200}', ''))
