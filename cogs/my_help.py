import discord
from random import choice
from config.functions import *
from discord.ext import commands





class MyHelp(commands.HelpCommand):

    # Beautify command aliases
    def adjust_aliases(self, command):
        aliases_value = ''
        len_aliases = len(command.aliases)
        for index in range(len_aliases):
            aliases_value += command.aliases[index]
            if index < len_aliases - 2:
                aliases_value += ', '
            elif index == len_aliases - 2:
                aliases_value += ' e '
        return aliases_value



    # Beautify command signature
    def adjust_command_signature(self, command, current_prefix):
        if str(command) == f'{self.context.prefix}ajuda [command]':
            return None
        new_command = command
        pos_init = command.find('[')
        if pos_init != -1:
            pos_end = command.find(']') + 1
            list_aliases_str = command[pos_init:pos_end]
            list_aliases = list_aliases_str.split('|')
            new_txt = list_aliases[1].replace(']', '')
            new_txt = new_txt.replace('[', '')
            new_command = command.replace(list_aliases_str, new_txt)
        # Remove prefix
        new_command = new_command.replace(current_prefix, '', 1).strip()
        split = new_command.split()
        c = 0
        for index in range(len(split)):
            try:
                current_com = ''
                for i in range(index + 1):
                    current_com += split[i] + ' '
                untranslated_com = self.context.bot.get_command(current_com.strip())
                split[index] = untranslated_com.aliases[0]
                c += 1
            except: break
        for i in range(c - 1):
            del split[0]
        new_command = ' '.join(split)
        return new_command



    # Beautify group/command
    async def adjust_commands(self, current_prefix, list_init=[]):
        value_cog=''
        #filtered = await self.filter_commands(list_init, sort=True)
        command_signatures = [self.get_command_signature(c) for c in list_init]
        command_brief = [c.brief for c in list_init]
        if command_signatures:
            # Returns only the first aliase
            for index in range(len(command_signatures)):
                command_signatures[index] = self.adjust_command_signature(
                    command_signatures[index], current_prefix)
            # Add return per line
            for signature, brief in zip(command_signatures, command_brief):
                if signature == None: continue
                value_cog += f'`{signature}`: {str(brief).strip()}\n'
        return value_cog



    # !help
    async def send_bot_help(self, mapping):
        ctx = self.context
        m = ctx.message
        a = ctx.author
        c = self.get_destination()
        current_prefix = ctx.prefix

        # Init emby
        emby = discord.Embed(
            title=f'Meu prefixo é: `{current_prefix}`',
            description='Para ter mais informações sobre o grupo de comandos ou comando, digite: '\
                f'{current_prefix}help <grupo/comando>.\n',
            color=discord.Color(int(choice(fb('/config/help_color')[len(m.content.split()) - 1]), 16)))
        emby.add_field(name='Informações úteis:\n',
            value='Argumento obrigatório: <>; argumento opcional: []')        
        
        # Separate command group from commands
        groups_list = []
        commands_list = []
        for cog, commands in mapping.items():
            if (cog is None or cog.__class__.__name__ == 'Owner') and int(a.id) not in list(map(int, fb('config', 'owns'))):
                continue
            for com in commands:
                if type(com) == discord.ext.commands.Group:
                    groups_list.append(com)
                elif type(com) == discord.ext.commands.Command:
                    commands_list.append(com)
        
        if groups_list:
            groups_value = await self.adjust_commands(current_prefix, groups_list)  # Beautifies group
            emby.add_field(name='Grupos', value=groups_value, inline=False)
        if commands_list:
            commands_value = await self.adjust_commands(current_prefix, commands_list)  # Beautifies commands
            emby.add_field(name='Comandos', value=commands_value, inline=False)

        emby.set_author(name=a.display_name, icon_url=a.display_avatar.url)

        reply_msg = await c.send(embed=emby)
        await delete_time(reply_msg, ctx)
        


    # !help <command>
    async def send_command_help(self, command):
        if str(command) == 'ajuda':
            return
        
        ctx = self.context
        m = ctx.message
        a = ctx.author
        c = self.get_destination()

        if command.cog_name in [None, 'Owner'] and int(a.id) not in list(map(int, fb('config', 'owns'))):
            return

        emby = discord.Embed(title=str(command).capitalize(),
            color=discord.Color(int(choice(fb('/config/help_color')[len(m.content.split()) - 1]), 16)))
        
        command_signature = self.adjust_command_signature(
            self.get_command_signature(command), ctx.prefix)

        emby.add_field(name='Usage (como usar)', value=command_signature, inline=False)
        emby.add_field(name='Help', value=command.help, inline=False)
        emby.add_field(name='Aliases (sinônimos)', value=self.adjust_aliases(command), inline=False)

        emby.set_author(name=a.display_name, icon_url=a.display_avatar.url)

        await c.send(embed=emby)



    # !help command_doesn't_exist
    def command_not_found(self, string):
        return f'O comando `{string}` não existe ou não está ativo... '\
            f'Para conferir os comandos/grupos ativos, use `{self.context.prefix}help`.'



    # !help <group>
    async def send_group_help(self, group):
        ctx = self.context
        m = ctx.message
        a = ctx.author
        c = self.get_destination()
        current_prefix = ctx.prefix

        if group.cog_name in [None, 'Owner'] and int(a.id) not in list(map(int, fb('config', 'owns'))):
            return

        emby = discord.Embed(title=str(group).capitalize(),
            description=group.description,
            color=discord.Color(int(choice(fb('/config/help_color')[len(m.content.split()) - 1]), 16)))
        
        if group.help:
            command_signature = self.adjust_command_signature(
                self.get_command_signature(group), ctx.prefix)

            emby.add_field(name='Usage (como usar)', value=command_signature, inline=False)
            emby.add_field(name='Help', value=group.help, inline=False)
        
        # Separate command group from commands
        groups_list = []
        commands_list = []
        for com in group.commands:
            if type(com) == discord.ext.commands.Group:
                groups_list.append(com)
            elif type(com) == discord.ext.commands.Command:
                commands_list.append(com)

        if groups_list:
            groups_value = await self.adjust_commands(current_prefix, groups_list)  # Beautifies group
            emby.add_field(name='Grupos', value=groups_value, inline=False)
        if commands_list:
            commands_value = await self.adjust_commands(current_prefix, commands_list)  # Beautifies commands
            emby.add_field(name='Comandos', value=commands_value, inline=False)
        
        emby.add_field(name='Aliases (sinônimos)', value=self.adjust_aliases(group), inline=False)

        emby.set_author(name=a.display_name, icon_url=a.display_avatar.url)

        await c.send(embed=emby)



    def subcommand_not_found(self, command, string):    
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f'O grupo "{command.qualified_name}" Não tem um subcomando com nome {string}.'\
                'Para conferir os comandos desse grupo, '\
                f'use `{self.context.prefix}help {command.qualified_name}`.'
        return f'O grupo "{command.qualified_name}" não tem subcomandos.'





attributes = {
   'name': "help",
   'aliases': ["ajuda"]
}

def setup(bot):
    bot.help_command = MyHelp(command_attrs=attributes)
