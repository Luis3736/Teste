bot_name = 'test'


import os
import json
import discord
import firebase_admin
from pathlib import Path
from discord.ext import commands
from datetime import datetime, timedelta
from firebase_admin import credentials, db





# Basic definitions
firebase_json_path = f'{os.path.dirname(os.path.abspath(__file__))}/firebase.json'
with open(firebase_json_path, 'r') as f:
    firebase_json = json.load(f)

# Conect to firebase
firebase_admin.initialize_app(
    credentials.Certificate(firebase_json_path),
    {"databaseURL": firebase_json["databaseURL"]}
)





# Functions

def now_brasilia():  # Time with Brasília time zone
    return datetime.utcnow() - timedelta(hours=3)



def now_formated():  # Brasília time in str
    return datetime.strftime(now_brasilia(), '%d/%m/%Y %H:%M:%S')



def fb(*path):  # Get value from firebase
    return db.reference('/' + '/'.join(list(map(str, path)))).get()



def fb_up(new_value, *path):  # Update firebase
    path = list(map(str, path))
    k = path[-1]
    path.pop(-1)
    db.reference('/' + '/'.join(path)).update({k: new_value})



def get_prefix(bot, message=None, channel=None, guild=None):  # Get apropriate prefix
    default_prefix = str(fb('config', 'prefix'))
    # Define variables for possible calls
    if channel is not None and guild is not None:
        c = channel
        gi = guild.id
    elif message is not None:
        c = message.channel
        if str(c.type) != 'private':
            gi = message.guild.id
    if str(c.type) != 'private':  # If private channel, use default prefix
        # Try to get specific prefix
        prefix = fb('guilds', str(gi), 'config', 'prefix')
        if prefix is None: return default_prefix
        else: return str(prefix)
    else: return default_prefix



def has_any_permission(*perms):  # Check perms
    def check_perms(ctx):
        for perm in perms:  # Check permission(s)
            if getattr(ctx.author.guild_permissions, perm, None):
                return True
        # Returns only required permission(s)
        error = str(commands.MissingPermissions(perms)).replace('You are missing ', '')
        error = error.replace(' permission(s) to run this command.', '')
        error = error.replace('and', 'or')
        raise commands.MissingPermissions(error)
    return commands.check(check_perms)
    


# Delete msg with apropriate time
async def delete_time(reply_msg, ctx = None, guild = None, message = None):
    # Define variables for possible calls
    if ctx is not None:
        guild = ctx.guild
        message = ctx.message
    if guild is not None:  # Only for guilds
        delete_time = fb('guilds', guild.id, 'config', 'delete_time')  # Time to delete in guild
        if delete_time is not None:
            delete_time = fb('config', 'delete_time')  # Time to delete default
        delete_command = fb('guilds', guild.id, 'config', 'delete_command')  # Delete command or no
        if delete_command:
            try: await message.delete()
            except: pass
        if delete_time is not None:
            try: await reply_msg.delete(delay=int(delete_time))
            except: pass



def tree(path, identacion = 1, return_out = None):  # Show file tree
    if return_out == None:
        return_out = f'{os.path.basename(path)}\n'
    for item in os.listdir(path):  # See directory files
        if str(item) == '__pycache__': continue
        return_out += " "*3*identacion + item + '\n'
        file = Path(os.path.join(path, item))
        if file.is_dir():  # If it is directory, call function for that directory
            return_out = tree(os.path.join(path, item), identacion + 1, return_out)
    return return_out



def msg_ready(bot, bot_name=''):  
    c = 0
    for i in bot.guilds:
        c += i.member_count
    msg = f'\n\n{"="*47}\n\nHello world! '
    msg += f'(Bot {bot_name})\n' if bot else '\n'
    msg += f'Name: {bot.user}\n'
    msg += f'Id: {bot.user.id}\n'
    msg += f'Start time: {fb("config", "start_time")}\n'
    msg += f'Last update: {fb("config", "last_update")}\n'
    msg += f"I'm on {len(bot.guilds)} guilds, seeing {c} members!\n"
    msg += f'\n{"="*47}\n\n'
    return msg


errors_to_disregard = (
    commands.CommandNotFound
)
