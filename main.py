teste = True

import math
import os
import discord
import json
import asyncio
import zipfile
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from discord import File
from discord.utils import get
from math import floor

dono = 747198241979760782
fox = 802681231811674185

# Funções

def ler(arquivo):
    if arquivo[-5] != '.':
        arquivo = f'{arquivo}.json'
    try:
        with open(arquivo, 'r', encoding='utf8') as f:
            return json.load(f)
    except:
        return f'Arquivo "{arquivo}" não encontrado!'

    
def ler_elemento(nome_arquivo: str, k, k2=None, k3=None, k4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    k = str(k)
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    if k2 is not None:
        k2 = str(k2)
        if k3 is not None:
            k3 = str(k3)
            if k4 is not None:
                k4 = str(k4)
                try:
                    return banco_de_dados[k][k2][k3][k4]
                except:
                    return f'Chave {k4} não encontrada!'
            else:
                try:
                    return banco_de_dados[k][k2][k3]
                except:
                    return f'Chave {k3} não encontrada!'
        else:
            try:
                return banco_de_dados[k][k2]
            except:
                return f'Chave {k2} não encontrada!'
    else:
        try:
            return banco_de_dados[k]
        except:
            return f'Chave {k} não encontrada!'


def escrever(nome_arquivo, k=None, v=None, b=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    banco_de_dados = ler(nome_arquivo)
    if v is not None:
        if str(v).lower() == 'true':
            v = True
        if str(v).lower() == 'false':
            v = False
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    try:
        banco_de_dados[k] = v
    except:
        pass
    if b != None:
        banco_de_dados = b

    with open(nome_arquivo, 'w', encoding='utf8') as arquivo:
        json.dump(banco_de_dados, arquivo, ensure_ascii=False,
                  sort_keys=True, indent=4, separators=(',', ':'))


def escrever_elemento(nome_arquivo, k, v=None, k2=None, k3=None, k4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    k = str(k)
    if v is not None:
        if str(v).lower() == 'true':
            v = True
        if str(v).lower() == 'false':
            v = False
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    if k2 is not None:
        k2 = str(k2)
        if k3 is not None:
            k3 = str(k3)
            if k4 is not None:
                k4 = str(k4)
                try:
                    banco_de_dados[k][k2][k3][k4] = v
                except:
                    try:
                        banco_de_dados[k][k2][k3] = {k4: v}
                    except:
                        try:
                            banco_de_dados[k][k2] = {k3: {k4: v}}
                        except:
                            banco_de_dados[k] = {k2:{k3:{k4:v}}}
                escrever(nome_arquivo, b=banco_de_dados)
                return ler_elemento(nome_arquivo, k, k2, k3, k4)
            else:
                try:
                    banco_de_dados[k][k2][k3] = v
                except:
                    try:
                        banco_de_dados[k][k2] = {k3: v}
                    except:
                        banco_de_dados[k] = {k2:{k3:v}}
                escrever(nome_arquivo, b=banco_de_dados)
                return ler_elemento(nome_arquivo, k, k2, k3)
        else:
            try:
                banco_de_dados[k][k2] = v
            except:
                banco_de_dados[k] = {k2:v}
            escrever(nome_arquivo, b=banco_de_dados)
            return ler_elemento(nome_arquivo, k, k2)
    else:
        banco_de_dados[k] = v
        escrever(nome_arquivo, b=banco_de_dados)
        return ler_elemento(nome_arquivo, k)


def escrever_elemento_lista(nome_arquivo, k, v=None, k2=None, k3=None, k4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    k = str(k)
    if v is not None:
        if str(v).lower() == 'true':
            v = True
        if str(v).lower() == 'false':
            v = False
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    if k2 is not None:
        k2 = str(k2)
        if k3 is not None:
            k3 = str(k3)
            if k4 is not None:
                k4 = str(k4)
                try:
                    banco_de_dados[k][k2][k3][k4].append(v)
                except:
                    try:
                        banco_de_dados[k][k2][k3][k4] = [v]
                    except:
                        try:
                            banco_de_dados[k][k2][k3] = {k4: [v]}
                        except:
                            try:
                                banco_de_dados[k][k2] = {k3:{k4:[v]}}
                            except:
                                banco_de_dados[k] = {k2:{k3:{k4:[v]}}}
                escrever(nome_arquivo, b=banco_de_dados)
                return ler_elemento(nome_arquivo, k, k2, k3, k4)
            else:
                try:
                    banco_de_dados[k][k2][k3].append(v)
                except:
                    try:
                        banco_de_dados[k][k2][k3] = [v]
                    except:
                        try:
                            banco_de_dados[k][k2] = {k3: [v]}
                        except:
                            banco_de_dados[k] = {k2:{k3:[v]}}
                escrever(nome_arquivo, b=banco_de_dados)
                return ler_elemento(nome_arquivo, k, k2, k3)
        else:
            try:
                banco_de_dados[k][k2].append(v)
            except:
                try:
                    banco_de_dados[k][k2] = [v]
                except:
                    banco_de_dados[k] = {k2:[v]}
            escrever(nome_arquivo, b=banco_de_dados)
            return ler_elemento(nome_arquivo, k, k2)
    else:
        try:
            banco_de_dados[k].append(v)
        except:
            banco_de_dados[k] = [v]
        escrever(nome_arquivo, b=banco_de_dados)
        return ler_elemento(nome_arquivo, k)


def deletar_item(nome_arquivo, i, i2=None, i3=None, i4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    i = str(i)
    if i2 is not None:
        i2 = str(i2)
        if i3 is not None:
            i3 = str(i3)
            if i4 is not None:
                i4 = str(None)
                try:
                    banco_de_dados[i][i2][i3].pop(i4)
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'"{i4}" deletado com sucesso!'
                except:
                    return f'Item "{i4}" não encontrado!'
            else:
                try:
                    banco_de_dados[i][i2].pop(i3)
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'"{i3}" deletado com sucesso!'
                except:
                    return f'Item "{i3}" não encontrado!'
        else:
            try:
                banco_de_dados[i].pop(i2)
                escrever(nome_arquivo, b=banco_de_dados)
                return f'Item "{i2}" deletado com sucesso!'
            except:
                return f'Item "{i2}" não encontrado!'
    else:
        try:
            banco_de_dados.pop(i)
            escrever(nome_arquivo, b=banco_de_dados)
            return f'Item "{i}" deletado com sucesso!'
        except:
            return f'Item "{i}" não encontrado!'


def deletar_valor_lista(nome_arquivo, k, v, k2=None, k3=None, k4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    if v is not None:
        if str(v).lower() == 'true':
            v = True
        if str(v).lower() == 'false':
            v = False
    k = str(k)
    if k2 is not None:
        k2 = str(k2)
        if k3 is not None:
            k3 = str(k3)
            if k4 is not None:
                k4 = str(k4)
                try:
                    banco_de_dados[k][k2][k3][k4].remove(v)
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'Valor "{v}" deletado com sucesso!'
                except:
                    return f'Valor "{v}" não encontrado!'
            else:
                try:
                    banco_de_dados[k][k2][k3].remove(v)
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'Valor "{v}" deletado com sucesso!'
                except:
                    return f'Valor "{v}" não encontrado!'
        else:
            try:
                banco_de_dados[k][k2].remove(v)
                escrever(nome_arquivo, b=banco_de_dados)
                return f'Valor "{v}" deletado com sucesso!'
            except:
                return f'Valor "{v}" não encontrado!'
    else:
        try:
            banco_de_dados[k].remove(v)
            escrever(nome_arquivo, b=banco_de_dados)
            return f'Valor "{v}" deletado com sucesso!'
        except:
            return f'Valor "{v}" não encontrado!'



def trocar_chave(nome_arquivo, trocar, k, k2=None, k3=None, k4=None):
    if nome_arquivo[-5] != '.':
        nome_arquivo = f'{nome_arquivo}.json'
    banco_de_dados = ler(nome_arquivo)
    if banco_de_dados == f'Arquivo "{nome_arquivo}" não encontrado!':
        return banco_de_dados
    trocar = str(trocar)
    if k2 is not None:
        k2 = str(k2)
        if k3 is not None:
            k3 = str(k3)
            if k4 is not None:
                k4 = str(k4)
                try:
                    temp = banco_de_dados[k][k2][k3][k4]
                    banco_de_dados[k][k2][k3].pop(k4)
                    banco_de_dados[k][k2][k3][trocar] = temp
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'Chave "{k4}" trocada com sucesso para "{trocar}"!'
                except:
                    return f'Chave {k4} não encontrada!'
            else:
                try:
                    temp = banco_de_dados[k][k2][k3]
                    banco_de_dados[k][k2].pop(k3)
                    banco_de_dados[k][k2][trocar] = temp
                    escrever(nome_arquivo, b=banco_de_dados)
                    return f'Chave "{k3}" trocada com sucesso para "{trocar}"!'
                except:
                    return f'Chave {k3} não encontrada!'
        else:
            try:
                temp = banco_de_dados[k][k2]
                banco_de_dados[k].pop(k2)
                banco_de_dados[k][trocar] = temp
                escrever(nome_arquivo, b=banco_de_dados)
                return f'Chave "{k2}" trocada com sucesso para "{trocar}"!'
            except:
                return f'Chave {k2} não encontrada!'
    else:
        try:
            temp = banco_de_dados[k]
            banco_de_dados.pop(k)
            banco_de_dados[trocar] = temp
            escrever(nome_arquivo, b=banco_de_dados)
            return f'Chave "{k}" trocada com sucesso para "{trocar}"!'
        except:
            return f'Chave {k} não encontrada!'



# Início do bot
client = discord.Client(intents=discord.Intents.all())
def agora():
    return datetime.utcnow() - timedelta(hours=3)


def sub_data(data1, data2):
    '''
    data1 - data2
    '''
    y1, m1, d1, h1, mn1, s1, mc1 = data1.year, data1.month, data1.day, data1.hour, data1.minute, data1.second, data1.microsecond
    data1 = datetime.strptime(f'{d1}/{m1}/{y1}-{h1}:{mn1}:{s1}.{mc1}', '%d/%m/%Y-%H:%M:%S.%f')
    y2, m2, d2, h2, mn2, s2, mc2 = data2.year, data2.month, data2.day, data2.hour, data2.minute, data2.second, data2.microsecond
    data2 = datetime.strptime(f'{d2}/{m2}/{y2}-{h2}:{mn2}:{s2}.{mc2}', '%d/%m/%Y-%H:%M:%S.%f')
    return  data1 - data2
    

@client.event
async def on_ready():
    c = 0
    for i in client.guilds:
        c += i.member_count
    msg_ready = f'\n\n{"="*50}\nOlá mundo!\n'\
    	f'Nome: {client.user}\n'\
    	f'Id: {client.user.id}\n'\
    	f'Ligamento: {datetime.strftime(agora(), "%d/%m/%Y %H:%M")}\n'\
    	f'Estou em {len(client.guilds)} servidores, vendo {c} membros!\n'\
    	f'{"="*50}\n\n'
    print(msg_ready)
    await client.get_user(dono).send(msg_ready)
    if not teste:
        await client.get_user(fox).send(msg_ready)
        await client.get_channel(ler_elemento('config', 'ids_importantes', 'logs_bot')).send(msg_ready)

    # Loop
    async def loop_on_ready():
        while True:
            async def avisar():
                for lembrete in ler_elemento('usuarios', 'lembretes'):
                    minutos = sub_data(agora(), datetime.strptime(lembrete[1], "%d/%m/%Y-%H:%M")).days * 24 * 60 * 60
                    minutos += sub_data(agora(), datetime.strptime(lembrete[1], "%d/%m/%Y-%H:%M")).seconds
                    minutos /= 60
                    if int(minutos) > 60:
                        chat_div = client.get_channel(ler_elemento('config', 'ids_importantes', 'chat_comando_div'))
                        await chat_div.send(f'<@{lembrete[0]}>, hora de divulgar')
                        deletar_valor_lista('usuarios', 'lembretes', lembrete)
                await asyncio.sleep(60)
            await avisar()
    
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(loop_on_ready())
        loop.run_forever()
    except:
        pass
    


@client.event
async def on_member_join(membro):
    # Chegada no Div aqui
    if int(membro.guild.id) == 688409928473378931:
        criacao_conta = sub_data(agora(), membro.created_at).days
        if criacao_conta < 0:
            criacao_conta = 0
        plural = ''
        if criacao_conta != 1:
            plural = 's'
        if criacao_conta < 2:
            ed = ed = discord.Embed(
            	title='Restrição',
                description=f'Sua conta foi criada a {criacao_conta} dia{plural}. ' \
                	f'Por motivos de segurança, sua conta foi banida do "{membro.guild.name}"',
                color=discord.Colour.purple()
            )
            try:
                await membro.send(embed=ed)
            except:
                pass
            ed = discord.Embed(
            	title='Membro banido',
                description=f'Conta criada a {criacao_conta} dia{plural}',
                color=discord.Colour.purple()
            )
            ed.add_field(
            	name='Conta',
                value=f'{membro.name} ({membro.id})'
            )
            await client.get_channel(ler_elemento('config', 'ids_importantes', 'logs_bot')).send(embed=ed)
            await membro.ban(reason=f'Conta criada a menos de 3 dias ({criacao_conta})')
            return
        elif criacao_conta < 4:
            ed = discord.Embed(
            	title='Restrição',
                description=f'Sua conta foi criada a {criacao_conta} dia{plural}. ' \
                	f'O "{membro.guild.name}" exige 5 dias de criação. Por favor, seja compreensivo',
                color=discord.Colour.purple()
            )
            try:
                await membro.send(embed=ed)
            except:
                pass
            ed = discord.Embed(
            	title='Membro kickado',
                description=f'Conta criada a {criacao_conta} dia{plural}',
                color=discord.Colour.purple()
            )
            ed.add_field(
            	name='Conta',
                value=f'{membro.name} ({membro.id})'
            )
            await client.get_channel(ler_elemento('config', 'ids_importantes', 'logs_bot')).send(embed=ed)
            count_kick = ler_elemento('usuarios', membro.id, 'count_kick')
            print(count_kick)
            if count_kick != 'Chave count_kick não encontrada!':
                escrever_elemento('usuarios', membro.id, (int(count_kick)+1), 'count_kick')
                count_kick = ler_elemento('usuarios', membro.id, 'count_kick')
                if int(count_kick) == 3:
                    ed = ed = discord.Embed(
                        title='Restrição',
                        description=f'Sua conta foi kickada 3 vezes. ' \
                            f'Por motivos de segurança, sua conta foi banida do "{membro.guild.name}"',
                        color=discord.Colour.purple()
                    )
                    try:
                        await membro.send(embed=ed)
                    except:
                        pass
                    ed = discord.Embed(
                        title='Membro banido',
                        description=f'Conta kickada 3 vezes',
                        color=discord.Colour.purple()
                    )
                    ed.add_field(
                        name='Conta',
                        value=f'{membro.name} ({membro.id})'
                    )
                    await client.get_channel(ler_elemento('config', 'ids_importantes', 'logs_bot')).send(embed=ed)
                    deletar_item('usuarios', membro.id)
                    await membro.ban(reason=f'Conta kickaa 3 vezes')
                    return
                else:
                    await membro.kick(reason=f'Conta criada a menos de 7 dias ({criacao_conta})')
                    return
            else:
                escrever_elemento('usuarios', membro.id, 1, 'count_kick')
                await membro.kick(reason=f'Conta criada a menos de 7 dias ({criacao_conta})')
            return
        notificacoes = client.get_channel(701907692981321758)
        mencao = await notificacoes.send(f'<@{membro.id}>')
        await mencao.delete(delay=5)

@client.event
async def on_member_remove(membro):
    # Apagar tds as msg qnd sair do div aqui
    if int(membro.guild.id) == 688409928473378931:
        def is_member(m):
            return m.author == membro

        for c in membro.guild.channels:
            if str(c.type) == 'text':
                await c.purge(check=is_member)
        
        
@client.event
async def on_message(message):
    # Parâmetros base
    prefix = ler_elemento('config', 'prefix')
    m = message.content
    ml = m.lower()
    a = message.author
    ai = int(a.id)
    aurl = a.display_avatar.url
    dn = a.display_name
    c = message.channel
    ci = c.id
    
    # Comandos de bancos de dados

    # Ler banco de dados
    if ml.startswith(f'{prefix}arquivo') and ai in [dono, fox]:  # arquivo <arquivo>
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        if arquivo_nome[-5] != '.':
            arquivo_nome = f'{arquivo_nome}.json'
        try:
            await c.send(file=File(arquivo_nome))
        except:
            await c.send(f'Arquivo "{arquivo_nome}" não encontrado')
        return
    

    # Ler chave específica
    if ml.startswith(f'{prefix}ler') and ai in [dono, fox]:  # ler <arquivo> <k1> [k2] [k3] [k4]
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = ml.split()[2]
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = ml.split()[3]
        except:
            k2 = None
        try:
            k3 = ml.split()[4]
        except:
            k3 = None
        try:
            k4 = ml.split()[5]
        except:
            k4 = None
        if k4 != None:
            ult_k = k4
        if k3 != None:
            ult_k = k3
        elif k2 != None:
            ult_k = k2
        else:
            ult_k = k1
        # Criação temp.json para envio
        with open('temp.json', 'w+', encoding='utf8') as arquivo:
            adicionar = {ult_k: ler_elemento(arquivo_nome, k1, k2, k3, k4)}
            json.dump(adicionar, arquivo, ensure_ascii=False,
                  sort_keys=True, indent=4, separators=(',', ':'))
        await c.send(file=File('temp.json'))
        # Deleta temp.json
        os.remove(f'{os.path.dirname(os.path.abspath(__file__))}/temp.json')
        return


    # Adicionar lista banco de dados
    if ml.startswith(f'{prefix}adicionarlista') and ai in [dono, fox]:  # el <arquivo> <k1> [k2] [k3] [k4] <v>
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = ml.split()[2]
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = ml.split()[3]
        except:
            k2 = None
        try:
            k3 = ml.split()[4]
        except:
            k3 = None
        try:
            k4 = ml.split()[5]
        except:
            k4 = None
        try:
            v = ml.split()[6]
        except:
            v = None
        for k in [k2, k3, k4, v]:
            if k is None:
                break
            v = k
        if v == k4:
            k4 = None
        if v == k3:
            k3 = None
        if v == k2:
            k2 = None        
        await c.send(f'"{escrever_elemento_lista(arquivo_nome,k1,v,k2,k3,k4)}"')
        return


    # Escrever banco de dados
    if ml.startswith(f'{prefix}escrever') and ai in [dono, fox]:  # escrever <arquivo> <k1> [k2] [k3] [k4] <v>
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = ml.split()[2]
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = ml.split()[3]
        except:
            k2 = None
        try:
            k3 = ml.split()[4]
        except:
            k3 = None
        try:
            k4 = ml.split()[5]
        except:
            k4 = None
        try:
            v = ml.split()[6]
        except:
            v = None
        for k in [k2, k3, k4, v]:
            if k is None:
                break
            v = k
        if v == k4:
            k4 = None
        if v == k3:
            k3 = None
        if v == k2:
            k2 = None
        if v.isnumeric():
            v = int(v)
        await c.send(f'"{escrever_elemento(arquivo_nome, k1, v, k2, k3, k4)}"')
        return


    # Deletar valor lista banco de dados
    if ml.startswith(f'{prefix}deletarvalor') and ai in [dono, fox]:  # del <arquivo> <k1> [k2] [k3] [k4] <v>
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = ml.split()[2]
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = ml.split()[3]
        except:
            k2 = None
        try:
            k3 = ml.split()[4]
        except:
            k3 = None
        try:
            k4 = ml.split()[5]
        except:
            k4 = None
        try:
            v = str(ml.split()[6])
        except:
            v = None
        for k in [k2, k3, k4, v]:
            if k is None:
                break
            v = k
        if v == k4:
            k4 = None
        if v == k3:
            k3 = None
        if v == k2:
            k2 = None
        await c.send(deletar_valor_lista(arquivo_nome, k1, v, k2, k3, k4))
        return


    # Deletar elemento banco de dados
    if ml.startswith(f'{prefix}deletar') and ai in [dono, fox]:  # del <arquivo> <k1> [k2] [k3] [k4]
        try:
            arquivo_nome = ml.split()[1]
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = ml.split()[2]
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = ml.split()[3]
        except:
            k2 = None
        try:
            k3 = ml.split()[4]
        except:
            k3 = None
        try:
            k4 = ml.split()[5]
        except:
            k4 = None
        await c.send(deletar_item(arquivo_nome, k1, k2, k3, k4))
        return
    

    # Trocar valor chave
    if ml.startswith(f'{prefix}trocar') and ai in [dono, fox]:  # trocar <arquivo> <chave 1> [chave 2] [chave 3] [chave 4] <nova chave>
        try:
            arquivo = str(ml.split()[1])
        except:
            await c.send('Favor digitar o nome do arquivo.')
            return
        try:
            k1 = str(ml.split()[2])
        except:
            await c.send('Favor digitar uma chave.')
            return
        try:
            k2 = str(ml.split()[3])
        except:
            await c.send('Favor digitar uma nova chave.')
            return
        try:
            k3 = str(ml.split()[4])
        except:
            k3 = None
        try:
            k4 = str(ml.split()[5])
        except:
            k4 = None
        try:
            v = str(ml.split()[6])
        except:
            v = None
        for k in [k2, k3, k4, v]:
            if k is None:
                break
            v = k
        if v == k4:
            k4 = None
        if v == k3:
            k3 = None
        if v == k2:
            k2 = None
        await c.send(f'"{trocar_chave(arquivo, v, k1, k2, k3, k4)}"')
        return

	
    # Backup
    if ml == f'{prefix}backup' and ai in [dono, fox]:
        z = zipfile.ZipFile('backup.zip', 'w', zipfile.ZIP_DEFLATED)
        for arquivo in os.listdir(os.getcwd()):
            if arquivo not in [
                '.cache',
                '.local',
                'backup.zip',
                'cba4afe2-3dbe-4f7f-b603-671cdb53d27e.tar.gz',
                'archive-2021-08-15T175220-0500.tar.gz',
                'discordpy'
            ]:
                z.write(arquivo)
        z.close()
        await c.send(file=File('backup.zip'))
        os.remove(f'{os.path.dirname(os.path.abspath(__file__))}/backup.zip')
        return      


    
    # comandos exclusivos do dono

	# Enviar msg chat específico
    if ml.startswith(f'{prefix}donoenviar') and ai == dono:  # PrefixEnviar <id chat> <msg>
        try:
            await message.delete()
        except:
            pass
        try:
            chat = client.get_channel(int(ml.split()[1]))
            msg_i = len(f'{prefix}donoenviar ') + len(ml.split()[1])+1
            msg = m[msg_i:]
            await chat.send(msg)
            confirmacao = await c.send('Mensagem enviada!')
            await confirmacao.delete(delay=5)
            return
        except:
            return
        

	# Reiniciar Bot
    if ml in [f'{prefix}dr', f'{prefix}donoreiniciar'] and ai == dono:
        try:
            await message.delete()
        except:
            pass
        try:
            confirmacao = await c.send('Reiniciando... Z z z')
            await confirmacao.delete(delay=5)
            await client.logout()
            return
        except:
            return


    # Adicionar cargo
    if ml.startswith(f'{prefix}donoaddrole') and ai == dono:  # Add <sv> <cargo> <pessoa>
        try:
            await message.delete()
        except:
            pass
        try:
            guild = client.get_guild(int(ml.split()[1]))
            role_id = int(ml.split()[2])
            pessoa = get(guild.members, id=int(ml.split()[3]))
            role = get(guild.roles, id=role_id)
            await pessoa.add_roles(role)
            confirmacao = await c.send('Cargo adicionado')
            await confirmacao.delete(delay=5)
            return
        except:
            return
    
    
    # Remover cargo
    if ml.startswith(f'{prefix}donoremoverole') and ai == dono:  # Add <sv> <cargo> <pessoa>
        try:
            await message.delete()
        except:
            pass
        try:
            guild = client.get_guild(int(ml.split()[1]))
            role_id = int(ml.split()[2])
            pessoa = get(guild.members, id=int(ml.split()[3]))
            role = get(guild.roles, id=role_id)
            await pessoa.remove_roles(role)
            confirmacao = await c.send('Cargo removido.')
            await confirmacao.delete(delay=5)
            return
        except:
            return


    # Kickar
    if ml.startswith(f'{prefix}donokick') and ai == dono:  # Add <sv> <pessoa> [motivo]
        try:
            await message.delete()
        except:
            pass
        try:
            guild = client.get_guild(int(ml.split()[1]))
            pessoa = get(guild.members, id=int(ml.split()[2]))
            motivo = m[(len(f'{prefix}donokick')+len(ml.split()[1])+len(ml.split()[2])+3):]
            await pessoa.kick(reason=motivo)
            confirmacao = await c.send('Membro kickado.')
            await confirmacao.delete(delay=5)
            return
        except:
            return


    # Banir
    if ml.startswith(f'{prefix}donoban') and ai == dono:  # ban <sv> <pessoa> [motivo]
        try:
            await message.delete()
        except:
            pass
        try:
            guild = client.get_guild(int(ml.split()[1]))
            pessoa = get(guild.members, id=int(ml.split()[2]))
            motivo = m[(len(f'{prefix}donoban')+len(ml.split()[1])+len(ml.split()[2])+3):]
            await pessoa.ban(reason=motivo)
            confirmacao = await c.send('Membro banido.')
            await confirmacao.delete(delay=5)
            return
        except:
            return


    # Unban
    if ml.startswith(f'{prefix}donounban') and ai == dono:  # unban <sv> <pessoa> 
        try:
            await message.delete()
        except:
            pass
        try:
            guild = client.get_guild(int(ml.split()[1]))
            pessoa = get(guild.members, id=int(ml.split()[2]))
            motivo = m[(len(f'{prefix}donoban')+len(ml.split()[1])+len(ml.split()[2])+3):]
            await pessoa.unban(reason=motivo)
            confirmacao = await c.send('Membro desbanido.')
            await confirmacao.delete(delay=5)
            return
        except:
            return


    # Editar mensagem
    if ml.startswith(f'{prefix}donoeditarmsg') and ai == dono:  # em <id do chat> <id da msg> <nova msg>
        try:
            await message.delete()
        except:
            pass
        try:
            id_chat = int(ml.split()[1])
            id_msg = int(ml.split()[2])
            nova_msg = m[(len(f'{prefix}donoeditarmsg ')+len(ml.split()[1])+len(ml.split()[2])+2):]
            msg = await client.get_channel(id_chat).history().get(id=id_msg)
            await msg.edit(content=nova_msg)
            confirmacao = await c.send('Mensagem editada.')
            await confirmacao.delete(delay=5)
            return
        except:
            return
    

    # Deletar mensagem
    if ml.startswith(f'{prefix}donodelmsg') and ai == dono:  # delmsg <id do chat> <id da msg>
        try:
            await message.delete()
        except:
            pass
        try:
            id_chat = int(ml.split()[1])
            id_msg = int(ml.split()[2])
            msg = await client.get_channel(id_chat).history().get(id=id_msg)
            await msg.delete()
            confirmacao = await c.send('Mensagem deletada.')
            await confirmacao.delete(delay=5)
            return
        except:
            return
    
    # Aviso staff
    for chat in ler_elemento('config', 'ids_importantes', 'chats_svs'):
        if int(ai) in list(map(int, (ler_elemento('config', 'ids_importantes', 'ignorar_verificacao')))): break
        if chat[0] == c.id:
            erro = False
            erro_msg = ''
            m_split = m.split()
            contagem_membros = []
            for palavra_link in m_split:
                find_gg = palavra_link.find('discord.gg')
                find_com = palavra_link.find('discord.com')
                pass_if = False
                if find_gg != -1:
                    invite = palavra_link[find_gg:]
                    pass_if = True
                if find_com != -1:
                    invite = palavra_link[find_com:]
                    pass_if = True
                if pass_if:
                    if invite.find('>*') != -1:
                        invite = invite.replace('>*', '')
                    try:
                        invite = await client.fetch_invite(url = invite)
                    except:  # Em caso de link inválido
                        return
                    member_count_number = invite.approximate_member_count
                    if str(member_count_number).find('.') != -1:
                        member_count_number = int(str(member_count_number).replace('.', ''))
                    if str(member_count_number).find(',') != -1:
                        member_count_number = int(str(member_count_number).replace(',', ''))
                    contagem_membros.append(member_count_number)
            for count_membros in contagem_membros:
                if chat[2] == 'infinito':
                    if not chat[1] <= count_membros:
                        erro = True
                        erro_msg = f'Contém servidor -{chat[1]} ({count_membros}) membros em <#{chat[0]}>.'
                else:
                    if not chat[1] <= count_membros:
                        erro = True
                        erro_msg = f'Contém servidor -{chat[1]} ({count_membros}) membros em <#{chat[0]}>.'
                    elif not count_membros <= chat[2]:
                        erro = True
                        erro_msg = f'Contém servidor +{chat[2]} ({count_membros}) membros em <#{chat[0]}>.'
            if erro:
                ed = discord.Embed(
                    title = 'Advirta',
                    description = f'Motivo: {erro_msg}',
                    colour = discord.Color.red()
                )
                link_msg = f'https://discord.com/channels/{message.guild.id}/{c.id}/{message.id}'
                ed.add_field(
                    name=f'Mensagem',
                    value=f'{link_msg}',
                    inline=False
                )
                ed.add_field(
                    name='Autor',
                    value=f'{dn} ({a} - {ai})',
                    inline=False
                )
                chat_comandos_staff = client.get_channel(ler_elemento('config', 'ids_importantes', 'logs_bot'))
                await chat_comandos_staff.send(f'<@&{ler_elemento("config", "ids_importantes", "staff")}>', embed=ed)
                ed_dm = discord.Embed(
                	title='Aviso',
                    description=f'Detectei um erro na sua divulgação',
                    colour=discord.Colour.red()
                )
                ed_dm.add_field(
                	name='Pelo motivo',
                    value=erro_msg,
                    inline=False
                )
                ed_dm.add_field(
                	name='Divulgação defeituosa',
                    value=f'{link_msg}',
                    inline=False
                )
                ed_dm.add_field(
                	name='Obs.:',
                    value='Caso você sair do servidor todas as suas mensagens serão apagadas automaticamente, ' \
                    	'ou seja todas as suas divulgações também, por isso não tente burlar a punição',
                    inline=False
                )
                ed_dm.add_field(
                    name='Obs. 2:',
                    value='Caso delete sua mensagem em até 1 min, não será punido.',
                    inline=False
                )
                try:
                    await a.send(embed=ed_dm)
                except:
                    pass
                return

    # Chat correto
    if c.id not in [756294407036207115, 842566116978327584, 
        842098048074383450, 785151816907227187, 740289180591980665, 
        698678106113704037, 756295298879586444] and (ml.startswith(prefix) and ml != '.'):
        if ai not in [dono, fox]:
            aviso = await c.send(f'Por favor, digite comandos apenas em ' \
                f'<#{ler_elemento("config", "ids_importantes", "chat_comandos")}>.')
            await aviso.delete(delay=5)
            return

    # Sinonimos dos comandos
    ajuda = [
        f'{client.user.id}',
        f'<@{client.user.id}>',
        f'<@!{client.user.id}>',
        f'{prefix}ajuda',
        f'{prefix}help',
        f'{prefix}comando',
        f'{prefix}command',
        f'{prefix}comandos',
        f'{prefix}commands'
    ]
    compra = [
        f'{prefix}compra',
        f'{prefix}comprar',
        f'{prefix}shop',
        f'{prefix}pacote',
        f'{prefix}pacotes'
    ]
    div = [
        f'{prefix}div',
        f'{prefix}div1',
        f'{prefix}div2',
        f'{prefix}divulgue',
        f'{prefix}divulgação',
        f'{prefix}divulgaçao',
        f'{prefix}divulgacão',
        f'{prefix}divulgacao',
        f'{prefix}divulgar'
    ]
    help_div = [
        f'{prefix}help div',
        f'{prefix}help divulgação',
        f'{prefix}help 2',
        f'{prefix}help2',
        f'{prefix}ajuda 2',
        f'{prefix}ajuda2',
        f'{prefix}comando 2',
        f'{prefix}command 2',
        f'{prefix}comandos 2',
        f'{prefix}commands 2',
        f'{prefix}comando2',
        f'{prefix}command2',
        f'{prefix}comandos2',
        f'{prefix}commands2',
        f'{prefix}help compra',
        f'{prefix}ajuda compra'
    ]
    help_adm = [
        f'{prefix}help adm',
        f'{prefix}helpadm',
        f'{prefix}help administração',
        f'{prefix}help administraçao',
        f'{prefix}help administracão',
        f'{prefix}help administracao',
        f'{prefix}help admin',
        f'{prefix}helpadministração',
        f'{prefix}helpadministraçao',
        f'{prefix}helpadministracão',
        f'{prefix}helpadministracao',
        f'{prefix}helpadmin'
    ]
    help_mod = [
        f'{prefix}help mod',
        f'{prefix}helpmod'
        f'{prefix}help moderação',
        f'{prefix}help moderaçao',
        f'{prefix}help moderacão',
        f'{prefix}help moderacao'
    ]
    save = [
        f'{prefix}save',
        f'{prefix}salvar'
    ]
    expiracao_sinonimos = [
        f'{prefix}exp',
        f'{prefix}expiração',
        f'{prefix}expiraçao',
        f'{prefix}expiracão',
        f'{prefix}expiracao'
        f'{prefix}time',
        f'{prefix}tempo',
        f'{prefix}temp'
    ]
    editar_sugestao = [
        f'{prefix}editarsugestão',
        f'{prefix}editarsugestao',
        f'{prefix}editarsugest',
        f'{prefix}editsugestão',
        f'{prefix}editsugestao',
        f'{prefix}editsugest'
    ]
    excluir_sugestao = [
        f'{prefix}excluirsugestão',
        f'{prefix}excluirsugestao',
        f'{prefix}excluirsugest',
        f'{prefix}deletarsugestão',
        f'{prefix}deletarsugestao',
        f'{prefix}deletarsugest',
        f'{prefix}deletesugestão',
        f'{prefix}deletesugestao',
        f'{prefix}deletesugest',
        f'{prefix}delsugestão',
        f'{prefix}delsugestao',
        f'{prefix}delsugest'
    ]
    aprovar_sugestao = [
        f'{prefix}aprovarsugestão',
        f'{prefix}aprovarsugestao',
        f'{prefix}aprovarsugest',
        f'{prefix}asugestão',
        f'{prefix}asugestao',
        f'{prefix}asugest'
    ]
    reprovar_sugestao = [
        f'{prefix}reprovarsugestão',
        f'{prefix}reprovarsugestao',
        f'{prefix}reprovarsugest',
        f'{prefix}rsugestão',
        f'{prefix}rsugestao',
        f'{prefix}rsugest'
    ]
    sugerir = [
        f'{prefix}sugerir',
        f'{prefix}sugest',
        f'{prefix}sugestão',
        f'{prefix}sugestao'
    ]

    # Comandos

    # Help
    if ml in ajuda:
        ed = discord.Embed(
            title=f'Meu prefixo é: `{prefix}`\n<> -> Parâmetro obrigatório',
            color=discord.Colour.dark_blue()
        )
        ed.set_author(name = dn, icon_url = aurl)
        ed.add_field(
            name = '`Ping`',
            value = 'Retorna a latência do bot.',
            inline = False
        )
        ed.add_field(
            name= '`Comprar`',
            value = 'Compra uma semi-divulgação automática por sonhos.',
            inline=False
        )
        ed.add_field(
            name= '`Sugerir <sugestão>` ou `sugest`',
            value = f'Faz uma sugestão no canal de <#{ler_elemento("config", "ids_importantes", "sugestoes")}>.',
            inline=False
        )
        ed.add_field(
            name= '`Editarsugestão <link ou id da sugestão> <nova sugestão>` ou `editsugest`',
            value = f'Altera sugestão feita no canal de <#{ler_elemento("config", "ids_importantes", "sugestoes")}>.',
            inline=False
        )
        ed.add_field(
            name= '`Deletarsugestão <link ou id da sugestão>` ou `delsugest`',
            value = f'Exclui uma sugestão feita no canal de <#{ler_elemento("config", "ids_importantes", "sugestoes")}>.',
            inline=False
        )
        if c.id == ler_elemento('config', 'ids_importantes', 'chat_comando_div'):
            ed.add_field(
                name='`help div`',
                value='Mostra os comandos de divulgação.',
                inline=False
            )
            ed.set_footer(text='Pg 1/2')
        if ai in [dono, fox]:
            ed.add_field(
                name='`help adm`',
                value='Mostra comandos exclusivos da administração do bot.',
                inline=False
            )
        if str(c.type) == 'private':
            if ai == dono:
                confirmacao_mod = True
            else:
                return
        else:
            confirmacao_mod = False
            for cargo in a.roles:
                for mod_id in ler_elemento('config', 'ids_importantes', 'mods_ids'):
                    if int(cargo.id) == int(mod_id):
                        confirmacao_mod = True
        if confirmacao_mod or ai == dono:
            ed.add_field(
            	name='`Help mod`',
                value='Mostra os comandos exclusivos da moderação do bot.',
                inline=False
            )
        
        await c.send(embed=ed)
        return
    

    # Help div
    if ml in help_div and c.id == ler_elemento('config', 'ids_importantes', 'chat_comando_div'):
        ed = discord.Embed(
            title='Divulgação',
            color=discord.Colour.dark_green()
        )
        ed.set_author(name = dn, icon_url = aurl)
        ed.add_field(
            name='`div`',
            value='Divulga mensagem configurada nos canais comprados.',
            inline=False
        )
        ed.add_field(
            name='`salvar` ou `save`',
            value='Salva nova mensagem',
            inline=False
        )
        ed.add_field(
            name='`expiração` ou `exp`',
            value='Mostra tempo para a expiração da compra e tempo _slowmode_ do comando `div`.',
            inline=False
        )
        ed.add_field(
            name='`lembrar <sim/não>`',
            value='Ativa ou desativa o lembrete automático sempre que é possível divulgar.',
            inline=False
        )
        ed.set_footer(text='Pg 2/2')

        await c.send(embed=ed)
        return
    

    # Help adm
    if ml in help_mod:
        if str(c.type) == 'private':
            if ai == dono:
                confirmacao_mod = True
            else:
                return
        else:
            confirmacao_mod = False
            for cargo in a.roles:
                for mod_id in ler_elemento('config', 'ids_importantes', 'mods_ids'):
                    if int(cargo.id) == int(mod_id):
                        confirmacao_mod = True
            if int(ci) == int(ler_elemento('config', 'ids_importantes', 'chat_comandos_sv_staff')):
                confirmacao_mod = True
        if confirmacao_mod or ai == dono:
            ed = discord.Embed(
            	title='Comandos da moderação',
                description='<> -> Parâmetro obrigatório\n[] -> Parâmetro opcional',
                color=discord.Colour.purple()
            )
            ed.set_author(name = dn, icon_url = aurl)
            ed.add_field(
                name='`batercartao` ou `bc`',
                value='Inicia/finaliza cartão',
                inline=False
            )
            ed.add_field(
                name='`ebc <id do cartão> <novo horário>`',
                value='Altera o horário de saída. Favor usar apenas em cartões finalizados.',
                inline=False
            )
            ed.add_field(
            	name='`AprovarSugestão <id ou link da sugestão> [motivo da aprovação]` ou `asugest`',
                value='Aprova sugestão feita',
                inline=False
            )
            ed.add_field(
            	name='`ReprovarSugestão <id ou link da sugestão> [motivo da reprovação]` ou `rsugest`',
                value='Reprova sugestão feita',
                inline=False
            )
            await c.send(embed=ed)
            return


    # Help mod
    if ml in help_adm and ai in [dono, fox]:
        ed = discord.Embed(
            title='Comandos da administração',
            description='<> -> Parâmetro obrigatório\n[] -> Parâmetro opcional',
            color=discord.Colour.gold()
        )
        ed.set_author(name = dn, icon_url = aurl)
        ed.add_field(
            name='`arquivo <arquivo>`',
            value='Retorna arquivo completo de banco de dados.',
            inline=False
        )
        ed.add_field(
            name='`ler <arquivo> <chave 1> [chave 2] [chave 3] [chave 4]`',
            value='Retorna valor contido na chave específica',
            inline=False
        )
        ed.add_field(
            name='`adicionarlista <arquivo> <chave 1> [chave 2] [chave 3] [chave 4] <valor>`',
            value='Adiciona valor a lista específica (ou cria e adiciona, caso não exista).',
            inline=False
        )
        ed.add_field(
            name='`escrever <arquivo> <chave 1> [chave 2] [chave 3] [chave 4] <valor>`',
            value='Escreve valor em chave específica (ou cria e adiciona, caso não exista).',
            inline=False
        )
        ed.add_field(
            name='`deletarvalor <arquivo> <chave 1> [chave 2] [chave 3] [chave 4] <valor>`',
            value='Deleta valor de lista esecífica.',
            inline=False
        )
        ed.add_field(
            name='`deletar <arquivo> <chave 1> [chave 2] [chave 3] [chave 4]`',
            value='Deleta valor específico',
            inline=False
        )
        ed.add_field(
            name='`trocar <arquivo> <chave 1> [chave 2] [chave 3] [chave 4] <nova chave>`',
            value='Troca a chave por outra (preservando seu conteúdo).',
            inline=False
        )
        await c.send(embed=ed)
        return


    # Ping
    if ml == f'{prefix}ping':
        msg_resposta = await c.send(f'Pong :ping_pong:: A latência da API é de {int(client.latency*1000)}ms')
        await msg_resposta.edit(content=f'Pong :ping_pong:: A minha latência é de '\
			f'{int((msg_resposta.created_at-message.created_at).microseconds/1000)}ms e '\
			f'a da API é de {int(client.latency*1000)}ms.')
        return

    # Compra

    # Renovação confirmação
    if ler_elemento('usuarios', ai, 'renovacao') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'renovacao')
            deletar_item('usuarios', ai, 'compra')
            await c.send('Compra cancelada!')
            return
        if ml in ['s', 'sim']:
            deletar_item('usuarios', ai, 'renovacao')
            escrever_elemento('usuarios', ai, 'ativo', 'termino_compra')
        if ml in ['n', 'não', 'nao']:
            escrever_elemento('usuarios', ai, 'ativo', 'menu')
            deletar_item('usuarios', ai, 'compra')

    # Menu inicial
    if ml in compra or ler_elemento('usuarios', ai, 'menu') == 'ativo':
        # Renovação
        if ler_elemento('usuarios', ai, 'compra') != 'Chave compra não encontrada!':
            escrever_elemento('usuarios', ai, 'ativo', 'renovacao')
            await c.send('Vi que já comprou conosco anteriormente. Gostaria de renovar o pacote? ' \
                '(Favor digitar apenas __sim__ ou __não__.)')
            return
        if ler_elemento('usuarios', ai, 'menu') != 'Chave menu não encontrada':
            deletar_item('usuarios', ai, 'menu')

        escrever_elemento('usuarios', ai, 'ativo', 'pacote')
        pacotes = ler_elemento('config', 'pacotes')
        pacote_lista = ''
        for pacote in pacotes:
            if pacote != "Começar index no 1":
                pacote_lista = f'{pacote_lista}\n' \
                    f'{pacotes.index(pacote)} - Pacote {pacote["nome"]} - {pacote["preco"]}k'
        await c.send(
            'Deseja comprar algum de nossos pacotes? (Confira as descrições de cada um em <#740291900669558894>) \n\n' \
            f'Não - Não quero pacotes{pacote_lista}\n\n'
            'Favor digitar apenas a opção.\n'
            '1º exemplo: **6**\n'
            '2º exemplo: **Não**'
        )
        return

    # Escolha de opção
    if ler_elemento('usuarios', ai, 'pacote') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'pacote')
            await c.send('Compra cancelada!')
            return
        if ml in ['n', 'não', 'nao']:
            deletar_item('usuarios', ai, 'pacote')
            escrever_elemento('usuarios', ai, 'ativo', 'compra_chat')
        else:
            try:
                pacotes = ler_elemento('config', 'pacotes')
                if pacotes[int(ml)] == "Começar index no 1":  # Testar se opção existe e impedir index 0
                    await c.send('Favor digitar opção ou __cancelar__ para cancelar a compra')
                    return
                deletar_item('usuarios', ai, 'pacote')
                escrever_elemento('usuarios', ai, 'ativo', 'pacote_comprado')
                escrever_elemento('usuarios', ai, int(ml), 'compra', 'pacote')

                # Setar pacote
                msg = 'Por favor selecione'
                for chats in ler_elemento('config', 'pacotes')[int(ml)]['chat']:
                   
                    # Qnt de chats
                    if chats[1] == 1:
                        chat = '1 chat'
                    else:
                        chat = f'{chats[1]} chats'

                    # Definição de quais chats
                    if chats[0] == 'divulgacao_principal':
                        if msg != 'Por favor selecione':
                            msg = f'{msg} e {chat} da categoria Divulgação Principal'
                        else:
                            msg = f'{msg} {chat} da categoria Divulgação Principal'
                    elif chats[0] == 'divulgacao_em_categorias':
                        if msg != 'Por favor selecione':
                            msg = f'{msg} e {chat} da categoria Divulgação em Categorias'
                        else:
                            msg = f'{msg} {chat} da categoria Divulgação em Categorias'
                    elif chats[0] == 'redes_sociais':
                        if msg != 'Por favor selecione':
                            msg = f'{msg} e {chat} da categoria Redes Sociais'
                        else:
                            msg = f'{msg} {chat} da categoria Redes Sociais'
                    elif chats[0] == 'procuracoes':
                        if msg != 'Por favor selecione':
                            msg = f'{msg} e {chat} da categoria Procurações'
                        else:
                            msg = f'{msg} {chat} da categoria Procurações'
                    elif chats[0] == 'colecionador':
                        if msg != 'Por favor selecione':
                            msg = f'{msg} e {chat} da categoria Colecionador'
                        else:
                            msg = f'{msg} {chat} da categoria Colecionador'
                msg = f'{msg}\nObs.:  Você irá mencionar os canais ou colocar os ids **na ordem que foi pedido**\n' \
                        '1º exemplo: 708348843950997504 688420681913991177 754296899938287686\n' \
                        '2º exemplo: <#708348843950997504> <#688420681913991177> <#754296899938287686>'
                await c.send(msg)
                return
            except:
                await c.send('Favor digitar uma opção ou __cancelar__ para cancelar a compra')
                return


    # Confirmação pacote
    if ler_elemento('usuarios', ai, 'pacote_comprado') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'compra')
            deletar_item('usuarios', ai, 'pacote_comprado')
            await c.send('Compra cancelada!')
            return

        chats_pacote_inicial = ler_elemento('config', 'pacotes')[ler_elemento('usuarios', ai, 'compra', 'pacote')]['chat']
        chats_pacote = ''
        for chat in chats_pacote_inicial:
            chats_pacote = (f'{chats_pacote} {(f"{chat[0]} "*chat[1]).strip()}').strip()
        chats_pacote = chats_pacote.split()

        chats = ml
        if chats.find('<#') != -1:
            chats = ml.replace('<#', '')
            chats = chats.replace('>', '')
        chats = chats.split()

        if len(chats) != len(chats_pacote):
            await c.send('Você selecionou uma quantidade de canais que não condiz com o comprado. ' \
                'Favor tentar novamente.')
            return

        count = 0
        for chat in chats_pacote:
            if chat == 'divulgacao_principal':
                if int(chats[count]) not in ler_elemento('config', 'cat_div_princ'):
                    await c.send(f'Chat <#{chats[count]}> ' \
                        'não está na categoria Divulgação Principal. Favor tentar novamente ' \
                        'ou __cancelar__ para cancelar compra')
                    return
            if chat == 'divulgacao_em_categorias':
                if int(chats[count]) not in ler_elemento('config', 'cat_div_em_cat'):
                    await c.send(f'Chat <#{chats[count]}> ' \
                        'não está na categoria Divulgação em Categorias. Favor tentar novamente ' \
                        'ou __cancelar__ para cancelar compra')
                    return
            if chat == 'redes_sociais':
                if int(chats[count]) not in ler_elemento('config', 'cat_rs'):
                    await c.send(f'Chat <#{chats[count]}> ' \
                        'não está na categoria Redes Sociais. Favor tentar novamente ' \
                        'ou __cancelar__ para cancelar compra')
                    return
            if chat == 'procuracoes':
                if int(chats[count]) not in ler_elemento('config', 'cat_procura'):
                    await c.send(f'Chat <#{chats[count]}> ' \
                        'não está na categoria Procurações. Favor tentar novamente ' \
                        'ou __cancelar__ para cancelar compra')
                    return
            if chat == 'vip':
                try:  # Confirmar se o usuário digitou algum vip
                    chats[count]
                except:
                    return
                
                vips = ler_elemento('config', 'vips')
                roles = []
                for r in a.roles:
                    roles.append(int(r.id))
                vip_chat = []
                for vip in vips:
                    for r in roles:
                        if vip["id"] == r:
                            vip_chat.append(vip["chat"])
                if vip_chat == []:
                    await c.send('Você não possui nenhum cargo vip. ' \
                        'Por favor, tente novamente ou __cancelar__ para cancelar')
                    return

                if chat not in vip_chat:
                    await c.send('Você não possui o cargo vip correspondente a esse chat. ' \
                        'Por favor, tente novamente ou __cancelar__ para cancelar')
                    return
            count += 1

        # Caso todos os chats estejam certos
        escrever_elemento('usuarios', ai, chats, 'compra', 'chats')
        escrever_elemento('usuarios', ai,
            ler_elemento('config', 'pacotes')[ler_elemento('usuarios', ai, 'compra', 'pacote')]['tempo'], 
            'compra', 'tempo')
        escrever_elemento('usuarios', ai,
            ler_elemento('config', 'pacotes')[ler_elemento('usuarios', ai, 'compra', 'pacote')]['link'], 
            'compra', 'link')
        escrever_elemento('usuarios', ai,
            ler_elemento('config', 'pacotes')[ler_elemento('usuarios', ai, 'compra', 'pacote')]['preco'], 
            'compra', 'preco')
        escrever_elemento('usuarios', ai, 'ativo', 'termino_compra')
        deletar_item('usuarios', ai, 'pacote_comprado')
        deletar_item('usuarios', ai, 'compra', 'pacote')

    # Compra + chat
    if ler_elemento('usuarios', ai, 'compra+chat') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'compra+chat')
            deletar_item('usuarios', ai, 'compra')
            await c.send('Compra cancelada!')
            return
        if ml in ['n', 'não', 'nao']:
            deletar_item('usuarios', ai, 'compra+chat')
            escrever_elemento('usuarios', ai, 'ativo','compra_tempo')  
        elif ml in ['s', 'sim']:
            deletar_item('usuarios', ai, 'compra+chat')
            escrever_elemento('usuarios', ai, 'ativo', 'compra_chat')
        else:
            await c.send('Opção inválida! Favor digitar apenas __sim__ ou __não__, ' \
                'ou __cancelar__ para cancelar compra.')
            return

    # Compra de chats (fora dos pacotes)
    if ler_elemento('usuarios', ai, 'compra_chat') == 'ativo':
        # Criação dinâmica do menu
        menu_chats = '**Lista de Chats**\n\n'
        ops = ler_elemento('config', 'ops')
        for categoria in ops:
            if categoria != 'Começar no index 1':
                menu_chats = f'{menu_chats}{categoria["nome"]}\n\n'
                for chat in categoria["chats_preco"]:
                    menu_chats = f'{menu_chats}{ops.index(categoria)}.{categoria["chats_preco"].index(chat)} ' \
                        f'- <#{chat[0]}> - {chat[1]}k\n'
                menu_chats = f'{menu_chats}\n'
        menu_chats = f'{menu_chats}Favor selecionar apenas uma opção, **com** o `.`\nEx.: `3.9`'
        escrever_elemento('usuarios', ai, 'ativo', 'compra_chat_item')
        deletar_item('usuarios', ai, 'compra_chat')
        menu_chats = await c.send(menu_chats)
        await menu_chats.delete(delay=600)
        return
    
    # Selecionar/escolher chat
    if ler_elemento('usuarios', ai, 'compra_chat_item') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'compra_chat_item')
            await c.send('Compra cancelada!')
            return
        try:
            categoria_index = int((str(ml).split()[0]).split('.')[0])
            chat_index = int((str(ml).split()[0]).split('.')[1])
        except:
            await c.send('Opção inválida! Favor escolher uma opção válida, seguindo o exemplo.')
            return
        try:
            nome_categoria = ler_elemento('config', 'ops')[categoria_index]['nome'].lower()
        except:
            await c.send('Opção inválida! Favor escolher uma opção válida, seguindo o exemplo.')
            return
        
        # Teste perm vip
        if nome_categoria.count('colecionador') > 0 or nome_categoria.count('vip') > 0:
            vip_confirmacao = False
            roles = []
            for r in a.roles:
                roles.append(int(r.id))
            for vip in ler_elemento('config', 'vips'):
                for r in roles:
                    if vip['id'] == r:
                        vip_confirmacao = True
            if not vip_confirmacao:
                await c.send('Você não tem permissão para divulgar nesse canal. Favor escolher outro chat.')
                return

        # Selecionar chat
        try:
            chat = ler_elemento('config', 'ops')[categoria_index]['chats_preco'][chat_index][0]
            preco = ler_elemento('config', 'ops')[categoria_index]['chats_preco'][chat_index][1]
        except:
            await c.send('Opção inválida! Favor escolher uma opção válida, seguindo o exemplo (**3.9**).')
            return
        if ler_elemento('usuarios', ai, 'compra', 'preco') != 'Chave preco não encontrada!':
            valor_total = ler_elemento('usuarios', ai, 'compra', 'preco')
        else:
            valor_total = 0
        for chat_pre_comprado in ler_elemento('usuarios', ai, 'compra', 'chats'):
            if str(chat) == str(chat_pre_comprado):
                escrever_elemento('usuarios', ai, 'ativo', 'compra+chat')
                deletar_item('usuarios', ai, 'compra_chat_item')
                await c.send('Esse chat já foi adicionado... Deseja comprar mais chats?')
                return
        escrever_elemento_lista('usuarios', ai, chat, 'compra', 'chats')
        escrever_elemento('usuarios', ai, valor_total + preco,'compra', 'preco')
        escrever_elemento('usuarios', ai, 'ativo', 'compra+chat')
        deletar_item('usuarios', ai, 'compra_chat_item')
        await c.send('Deseja comprar mais chats? (Favor digitar apenas __sim__ ou __não__.)')
        return

    """
    # Compra + tempo
    if ler_elemento('usuarios', ai, 'compra+tempo') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'compra+tempo')
            deletar_item('usuarios', ai, 'compra')
            await c.send('Compra cancelada!')
            return
        if ml in ['s', 'sim']:
            deletar_item('usuarios', ai, 'compra+tempo')
            escrever_elemento('usuarios', ai, 'ativo', 'compra_tempo')
        elif ml in ['n', 'não', 'nao']:
            deletar_item('usuarios', ai, 'compra+tempo')
            escrever_elemento('usuarios', ai, 'ativo', 'termino_compra')
        else:
            await c.send('Opção inválida! Favor digitar apenas __sim__ ou __não__, ' \
                'ou __cancelar__ para cancelar compra.')
            return
    """

    # Compra tempo
    if ler_elemento('usuarios', ai, 'compra_tempo') == 'ativo':
        # Criação dinâmica do menu
        menu_tempo = '**Lista de Tempos**\n\n'
        tempo_preco = ler_elemento('config', 'tempo_preco')
        for tempo in tempo_preco:
            if tempo != 'Começar index no 1':
                menu_tempo = f'{menu_tempo}{tempo_preco.index(tempo)} - Duração: {tempo[0]}d - {tempo[1]}k\n'
        menu_tempo = f'{menu_tempo}\nFavor selecionar apenas o número.'
        escrever_elemento('usuarios', ai, 'ativo', 'compra_tempo_item')
        deletar_item('usuarios', ai, 'compra_tempo')
        await c.send(menu_tempo)
        return
    
    # Selecionar/escolher tempo
    if ler_elemento('usuarios', ai, 'compra_tempo_item') == 'ativo':
        tempos_disponiveis = len(ler_elemento('config', 'tempo_preco'))
        if not 0 < int(ml) < tempos_disponiveis:
            await c.send('Opção inválida! Favor digitar apenas um número válido.')
            return
        if ler_elemento('usuarios', ai, 'compra', 'tempo') != 'Chave tempo não encontrada!':
            tempo_inicial = ler_elemento('usuarios', ai, 'compra', 'tempo')
        else:
            tempo_inicial = 0
        tempo_final = tempo_inicial + ler_elemento('config', 'tempo_preco')[int(ml)][0]
        if ler_elemento('usuarios', ai, 'compra', 'preco') != 'Chave preco nao encontrada!':
            preco_inicial = ler_elemento('usuarios', ai, 'compra', 'preco')
        else:
            preco_inicial = 0
        preco_final = preco_inicial + ler_elemento('config', 'tempo_preco')[int(ml)][1]
        deletar_item('usuarios', ai, 'compra_tempo_item')
        escrever_elemento('usuarios', ai, tempo_final, 'compra', 'tempo')
        escrever_elemento('usuarios', ai, preco_final, 'compra', 'preco')
        escrever_elemento('usuarios', ai, 'ativo', 'termino_compra')

    # Término de compra
    if ler_elemento('usuarios', ai, 'termino_compra') == 'ativo':
        if len(ler_elemento("usuarios", ai, "compra", "chats")) == 1:
            chats = f'<#{ler_elemento("usuarios", ai, "compra", "chats")[0]}>'
        else:
            l = ler_elemento("usuarios", ai, "compra", "chats")
            l2 = []
            for e in l:
                l2.append(str(e))
            chats = f'<#{">, <#".join(l2)}>'
        preco = ler_elemento('usuarios', ai, 'compra', 'preco')
        if ler_elemento('usuarios', ai, 'compra', 'link') == 'Chave link não encontrada!':
            escrever_elemento('usuarios', ai, 1, 'compra', 'link')
            link = '1 link'
        elif ler_elemento('usuarios', ai, 'compra', 'link') == 1:
            link = '1 link'
        else:
            link = f"{ler_elemento('usuarios', ai, 'compra', 'link')} links"
        tempo = ler_elemento('usuarios', ai, 'compra', 'tempo')
        mensagem = f'Você confirma as seguintes informações?\n\n' \
            f'Tempo: {tempo}d\n' \
            f'Chats: {chats}\n' \
            f'Especialidade: {link}\n' \
            f'Preço: {preco}k\n\n' \
            'Favor digitar apenas __sim__ ou __não__.'
        deletar_item('usuarios', ai, 'termino_compra')
        escrever_elemento('usuarios', ai, 'ativo', 'termino_compra_confirmacao')
        await c.send(mensagem)
        return
    
    # Confirmar término de compra
    if ler_elemento('usuarios', ai, 'termino_compra_confirmacao') == 'ativo':
        if ml == 'cancelar':
            deletar_item('usuarios', ai, 'compra')
            deletar_item('usuarios', ai, 'termino_compra_confirmacao')
            await c.send('Compra cancelada!')
            return
        if ml in ['n', 'não', 'nao']:
            deletar_item('usuarios', ai, 'compra')
            deletar_item('usuarios', ai, 'termino_compra_confirmacao')
            await c.send('Que pena que não pude te ajudar... '\
                'Caso esteja enfrentando dificuldades, abra um ticket em <#739150700147114045>, ' \
                'para que um de nossos staffs possa te auxiliar.')
            return
        if ml in ['s', 'sim']:
            deletar_item('usuarios', ai, 'termino_compra_confirmacao')
            escrever_elemento('usuarios', ai, 'ativo', 'pagamento')
            await c.send('Por favor, aguarde até que alguém com o cargo ' \
                f'<@&{ler_elemento("config", "ids_importantes", "receptores_de_pagamento")}> ' \
                'responda a essa mensagem. Confira se a pessoa realmente tem esse cargo, ' \
                'pois não nos responsabilizamos por pagamentos a pessoas erradas. ' \
                'Após essa conferência, pague o valor citado à ela. Quando o pagamento for ' \
                'efetuado, envie qualquer mensagem, para que eu possa adicionar os ítens comprados.\n\n' \
                'Obs. 1: O pagamento deverá ser feito em ' \
                f'<#{ler_elemento("config", "ids_importantes", "chat_pagamento")}>.\n' \
                'Obs. 2: A compra será efetuada assim você enviar a primeira mensagem após a compra')
            await client.get_channel(740288961502773323).send(f"O usuário <@{ai}> deve pagar {ler_elemento('usuarios', ai, 'compra', 'preco')*1000}")
            return
        # Opção inválida
        await c.send('Opção inválida! Favor digitar apenas __sim__ ou __não__.')
        return

    # Cancelamento
    if ler_elemento('usuarios', ai, 'pagamento') == 'ativo' and ml == 'cancelar':
        deletar_item('usuarios', ai, 'pagamento')
        deletar_item('usuarios', ai, 'compra')
        await c.send('Compra cancelada!')
        return

    # Confirmação de recebimento
    if c.id == ler_elemento('config', 'ids_importantes', 'chat_pagamento') and \
        ai == ler_elemento('config', 'ids_importantes', 'lori'):
        
        # Variáveis de controle
        mls = ml.split()
        if len(mls) == 0: return
        
        if mls[0] in ['💸', ':money_with_wings:']:
            id_receptor = str(mls[7])
            id_pagador = str(mls[2])
            valor = mls[9]
        elif ml.find('transferência realizada com sucesso!') != -1:
            id_receptor = str(mls[27])
            id_pagador = str(mls[12])
            valor = mls[8]
        else: return
        
        valor = int(str(valor).replace('*', '').replace(',', '').replace('.', ''))
        id_receptor = int(id_receptor.replace('>', '').replace('<@', ''))
        id_pagador = int(id_pagador.replace('>', '').replace('<@', ''))
        
        # Confirmar se usuário realmente comprou algo
        if ler_elemento('usuarios', id_pagador, 'pagamento') != 'ativo':
            return
        
        # Confirmar se usuario pd receber valor
        r = []
        for membro in message.guild.members:
            for role in membro.roles:
                if role.id == ler_elemento('config', 'ids_importantes', 
                    'receptores_de_pagamento'):
                    r.append(membro.id)
                    
        if id_receptor not in r:
            await c.send('O usuário que você pagou não pertence a lista de ' \
                'usuários que podem receber o pagamento. Favor tentar novamente.')
            return
        
        if valor != ler_elemento('usuarios', id_pagador, 'compra', 'preco')*1000:
            await c.send(f'**Valor incorreto!**\n' \
                f'<@{id_receptor}>, favor devolver o valor.\n' \
                f'<@{id_pagador}>, sua compra ainda está ativa. Pague o valor de '\
                f'{ler_elemento("usuarios", id_pagador, "compra", "preco")}k sonhos ou ' \
                'digite __cancelar__ para cancelar compra.')
            return
        
        escrever_elemento('usuarios', id_pagador, 'ativo', 'pagamento_feito')
        deletar_item('usuarios', id_pagador, 'pagamento')
        await c.send(f'Pagamento confirmado! Escreva qualquer mensagem para que eu possa atribuir o produto.')
        return

    # Dar ítens
    if ler_elemento('usuarios', ai, 'pagamento_feito') == 'ativo':
        deletar_item('usuarios', ai, 'pagamento_feito')
        role = get(a.guild.roles, id=ler_elemento('config', 'ids_importantes', 'semi_div'))
        try: await a.add_roles(role)
        except: pass
        
        tempo = relativedelta(days=+ler_elemento('usuarios', ai, 'compra', 'tempo'))
        expiracao = datetime.strftime(agora() + tempo, '%d/%m/%Y-%H:%M')
        
        escrever_elemento('usuarios', ai, expiracao, 'compra', 'expiracao')
        escrever_elemento('usuarios', ai, 'ativo', 'save')

        await c.send('Compra realizada! Esperamos que aproveite.')
        chat_div = client.get_channel(ler_elemento('config', 'ids_importantes', 'chat_comando_div'))
        await chat_div.send(f'<@{ai}>, sua próxima mensagem nesse chat será salva para a divulgação. ' \
            'Tenha **cuidado** para não burlar as regras de nenhum dos canais comprados.')
        return
        
    # Salvar div
    if ler_elemento('usuarios', ai, 'save') == 'ativo' and \
    (c.id == ler_elemento('config', 'ids_importantes', 'chat_comando_div') or c.id == ler_elemento('config', 'ids_importantes', 'comandos_staff')):
        
        # Confirmar máx de links comprados
        count_link = 0
        for link in ler_elemento('config', 'links_validos'):
            count_link += str(ml).count(link)
        if count_link > ler_elemento('usuarios', ai, 'compra', 'link'):
            await c.send('Quantidade de links comprados ultrapassada! Favor tentar novamente.')
            return
        
        # Retirar menção @everyone e @here
        if str(m).count('@everyone') > 0:
            message.content = message.content.replace('@everyone', '')
        if str(m).count('@here') > 0:
            message.content = message.content.replace('@here', '')     
        
        # Conferência de membros nos chats sv p, m e g
        for chat_comprado in ler_elemento('usuarios', ai, 'compra', 'chats'):
            for chat_pmg in ler_elemento('config', 'ids_importantes', 'chats_svs'):
                if int(chat_comprado) == int(chat_pmg[0]):
                    m_split = m.split()
                    contagem_membros = []
                    for palavra_link in m_split:
                        find_gg = palavra_link.find('discord.gg')
                        find_com = palavra_link.find('discord.com')
                        pass_if = False
                        if find_gg != -1:
                            invite = palavra_link[find_gg:]
                            pass_if = True
                        if find_com != -1:
                            invite = palavra_link[find_com:]
                            pass_if = True
                        if pass_if:
                            if invite.find('>*') != -1:
                                invite = invite.replace('>*', '')
                            try:
                                invite = await client.fetch_invite(url = invite)
                            except:  # Em caso de link inválido
                                await c.send('Alguns links fornecidos são inválidos! Favor tentar novamente. \n' \
                                        'Em caso de persistência aguarde um ' \
                                        f'<@&{ler_elemento("config", "ids_importantes", "receptores_de_pagamento")}>')
                                return
                            member_count_number = invite.approximate_member_count
                            if str(member_count_number).find('.') != -1:
                                member_count_number = int(str(member_count_number).replace('.', ''))
                            if str(member_count_number).find(',') != -1:
                                member_count_number = int(str(member_count_number).replace(',', ''))
                            contagem_membros.append(member_count_number)
                    chat_errado = False
                    for count_membros in contagem_membros:
                        if chat_pmg[2] == 'infinito':
                            if not chat_pmg[1] <= count_membros:
                                chat_errado = True
                        else:
                            if not chat_pmg[1] <= count_membros <= chat_pmg[2]:
                                chat_errado = True
                    if chat_errado:
                        await c.send('Há servidor(es) que não obece(m) os requisitos do chat ' \
                                    f'<#{chat_comprado}>. Favor tentar novamente.')
                        return

        # Salvar msg
        escrever_elemento('usuarios', ai, message.content, 'compra', 'msg')
        deletar_item('usuarios', ai, 'save')

        await c.send(f'Divulgação salva! Para divulgar, utilize o comando `{prefix}div`. ' \
            f'Caso queira alterar essa divulgação durante o tempo comprado, utlize `{prefix}save` nesse chat. ')
        return

    # Salvar div via comando
    if ml in save and (c.id == ler_elemento('config', 'ids_importantes', 'chat_comando_div') or c.id == ler_elemento('config', 'ids_importantes', 'comandos_staff')):

        expiracao = ler_elemento('usuarios', ai, 'compra', 'expiracao')

        # Caso não tenha comprado
        if expiracao == 'Chave expiracao não encontrada!':
            await c.send(f'Você não comprou nenhuma semi-divulgação. Faça isso com o comando `{prefix}comprar`.')
            return
        
        expiracao = datetime.strptime(expiracao, '%d/%m/%Y-%H:%M')
        tempo_de_expiracao = (expiracao - agora()).days
        if tempo_de_expiracao < 0:
            await c.send(f'Tempo expirado! Caso queira continuar, compre com o comando `{prefix}comprar`.')
            await a.remove_roles(ler_elemento('config', 'ids_importantes', 'semi_div'))
            return
        
        # Encaminhar para salvamento
        escrever_elemento('usuarios', ai, 'ativo', 'save')

        await c.send(f'<@{ai}>, sua próxima mensagem nesse chat será salva para a divulgação. ' \
            'Tenha **cuidado** para não burlar as regras de nenhum dos canais comprados.')
        return

    # Divulgação semi-automática
    if ml in div:
        expiracao = ler_elemento('usuarios', ai, 'compra', 'expiracao')
        
        # Caso não tenha comprado
        if expiracao == 'Chave expiracao não encontrada!':
            await c.send(f'Você não comprou nenhuma semi-divulgação. Faça isso com o comando `{prefix}comprar`.')
            return
        
        expiracao = datetime.strptime(expiracao, '%d/%m/%Y-%H:%M')
        tempo_de_expiracao = (expiracao - agora()).days
        if tempo_de_expiracao < 0:
            await c.send(f'Tempo expirado! Caso queira continuar, compre com o comando `{prefix}comprar`.')
            if ler_elemento('usuarios', ai, 'compra', 'ult_div') != 'Chave ult_div não encontrada!':
                deletar_item('usuarios', ai, 'compra', 'ult_div')
            deletar_item('usuarios', ai, 'compra', 'expiracao')
            deletar_item('usuarios', ai, 'compra', 'msg')
            role = get(a.guild.roles, id=ler_elemento('config', 'ids_importantes', 'semi_div'))
            try:
                await a.remove_roles(role)
            except: pass
            return
        
        # Conferencia de slowmode
        ult_div = ler_elemento('usuarios', ai, 'compra', 'ult_div')
        if ult_div != 'Chave ult_div não encontrada!':
            ult_div = datetime.strptime(ult_div, '%d/%m/%Y-%H:%M')
            if not ((agora()-ult_div).seconds)//3600 > 0 and not (agora()-ult_div).days > 0:
                await c.send('O tempo entre semi-divulgações é de 1h. ' \
                    f'Espere {60-(((agora() - ult_div).seconds)//60)}min para usar esse comando novamente.')
                return
        
        # Div nos canais comprados
        for chat in ler_elemento('usuarios', ai, 'compra', 'chats'):
            chat = client.get_channel(int(chat))
            await chat.send(f'{ler_elemento("usuarios", ai, "compra", "msg")}\n\nBy {dn} ({a} - {ai})')
        
        # Confirmação de div
        escrever_elemento('usuarios', ai, datetime.strftime(agora(), '%d/%m/%Y-%H:%M'), 'compra', 'ult_div')
        await c.send('Divulgação(ões) realizada(s) com sucesso!')
        if ler_elemento('usuarios', ai, 'lembrete') == True:
            for lembrete in ler_elemento('usuarios', 'lembretes'):
                if lembrete[0] == ai:
                    deletar_valor_lista('usuarios', 'lembretes', lembrete)
            escrever_elemento_lista('usuarios', 'lembretes', [ai, datetime.strftime(agora(), '%d/%m/%Y-%H:%M')])
        return

    # Consultar tempo de expiração
    if ml in expiracao_sinonimos and c.id == ler_elemento('config', 'ids_importantes', 'chat_comando_div'):
        expiracao = ler_elemento('usuarios', ai, 'compra', 'expiracao')

        # Caso não tenha comprado
        if expiracao == 'Chave expiracao não encontrada!':
            await c.send(f'Você não comprou nenhuma semi-divulgação. Faça isso com o comando `{prefix}comprar`.')
            return
        
        expiracao_date = datetime.strptime(expiracao, '%d/%m/%Y-%H:%M')
        tempo = expiracao_date - agora()

        # Caso tempo tenha expirado
        if tempo.days < 0:
            await c.send(f'Tempo expirado! Caso queira continuar, compre com o comando `{prefix}comprar`.')
            if ler_elemento('usuarios', ai, 'compra', 'ult_div') != 'Chave ult_div não encontrada!':
                deletar_item('usuarios', ai, 'compra', 'ult_div')
            deletar_item('usuarios', ai, 'compra', 'expiracao')
            deletar_item('usuarios', ai, 'compra', 'msg')
            role = get(a.guild.roles, id=ler_elemento('config', 'ids_importantes', 'semi_div'))
            await a.remove_roles(role)
            return
        
        # Conferencia de slowmode
        ult_div = ler_elemento('usuarios', ai, 'compra', 'ult_div')
        return_ult_div = 'Você pode realizar uma divulgação.'
        if ult_div != 'Chave ult_div não encontrada!':
            ult_div = datetime.strptime(ult_div, '%d/%m/%Y-%H:%M')
            if not ((agora()-ult_div).seconds)//3600 > 0:
                return_ult_div = f'Espere {60-(((agora() - ult_div).seconds)//60)}min para divulgar.'

        tempo = [tempo.days, floor(tempo.seconds/3600),
            floor((tempo.seconds - (3600*(floor(tempo.seconds/3600))))/60)]
        expiracao = expiracao.split('-')

        if int(tempo[0]) == 1:
            tempo[0] = '1 dia'
        else:
            tempo[0] = f'{tempo[0]} dias'
        if int(tempo[1]) == 1:
            tempo[1] = '1 hora'
        else:
            tempo[1] = f'{tempo[1]} horas'
        if int(tempo[2]) == 1:
            tempo[2] = '1 minuto'
        else:
            tempo[2] = f'{tempo[2]} minutos'
        await c.send(
            f'Divulgação: {return_ult_div}\n'
            f'Expira em: {expiracao[0]} às {expiracao[1]}.\n' \
            f'Tempo restante: {tempo[0]}, {tempo[1]} e {tempo[2]}.')
        return


    
    # Comandos
    
    # Sugerir
    try:
        if ml.split()[0] in sugerir:
            sugestao = m[(len(ml.split()[0])+1):]
            if sugestao == '':
                await c.send(f'<@{ai}>, favor inserir uma sugestão.')
                try: await message.delete()
                except: pass
                return
            ed = discord.Embed(
                title=f'Sugestão de {dn} ({ai})',
                description=sugestao,
                colour=discord.Colour.blue()
            )
            try: await message.delete()
            except: pass
            sugestoes_chat_id = ler_elemento('config', 'ids_importantes', 'sugestoes')
            sugestoes_chat = client.get_channel(sugestoes_chat_id)
            sugestao_bot = await sugestoes_chat.send(embed=ed)
            for emoji_dict in ler_elemento('config', 'ids_importantes', 'emojis_vx').values():
                emoji = client.get_emoji(emoji_dict['id'])
                await sugestao_bot.add_reaction(emoji)
            await c.send(f'Sua sugestão foi enviada com sucesso para <#{sugestoes_chat_id}>')
            return
    except:
        pass


    # Editar Sugestão
    try:
        if ml.split()[0] in editar_sugestao:  # PrefixEditsugest <id/link msg> <nova sugest>
            msg = m.split()[1]
            if msg.isnumeric():
                msg = int(msg)
            else:
                try:
                    msg = int(msg[-18:])
                except:
                    await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                    try: await message.delete()
                    except: pass
                    return
            nova_sugestao =  m[(len(f'{prefix}editsugest')+2+len(ml.split()[1])):]
            await message.delete()
            if nova_sugestao == '':
                await c.send(f'<@{ai}>, favor digitar a nova sugestão.')
                return
            sugestoes_chat_id = ler_elemento('config', 'ids_importantes', 'sugestoes')
            sugestoes_chat = client.get_channel(sugestoes_chat_id)
            try:
                msg = await sugestoes_chat.history().get(id=msg)
            except:
                await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                return
            if msg.embeds[0].title.count(str(ai)) < 1:
                await c.send(f'<@{ai}>, você deverá ser o(a) autor(a) da mensagem para poder editá-la.')
                return
            nova_embed = discord.Embed(
                title=f'Sugestão de {dn} ({ai})',
                description=nova_sugestao,
                colour=discord.Colour.blue()
            )
            await msg.edit(embed=nova_embed)
            await c.send(f'<@{ai}>, sugestão editada com sucesso!')
            return
    except:
        pass

    
    # Excluir sugestão
    try:
        if ml.split()[0] in excluir_sugestao:
            msg = m.split()[1]
            try: await message.delete()
            except: pass
            if msg.isnumeric():
                msg = int(msg)
            else:
                try:
                    msg = int(msg[-18:])
                except:
                    await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                    await message.delete()
                    return
            sugestoes_chat_id = ler_elemento('config', 'ids_importantes', 'sugestoes')
            sugestoes_chat = client.get_channel(sugestoes_chat_id)
            try:
                msg = await sugestoes_chat.history().get(id=msg)
            except:
                await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                return
            if msg.embeds[0].title.count(str(ai)) < 1:
                confirmacao_mod_sugest = False
                for cargo in a.roles:
                    for mod_id in ler_elemento('config', 'ids_importantes', 'mods_sugests'):
                        if int(cargo.id) == int(mod_id):
                            confirmacao_mod_sugest = True
                if confirmacao_mod_sugest or ai == dono:
                    pass
                else:
                    await c.send(f'<@{ai}>, você deverá ser o(a) autor(a) da mensagem para poder excluí-la.')
                    return
            await msg.delete()
            await c.send(f'<@{ai}>, sugestão deletada com sucesso!')
            return
    except:
        pass
    

    # Aprovar sugestão
    try:
        if ml.split()[0] in aprovar_sugestao:  # PrefixAsugest <id ou link sugest> [motivo]
            confirmacao_mod = False
            for cargo in a.roles:
                for mod_id in ler_elemento('config', 'ids_importantes', 'mods_ids'):
                    if int(cargo.id) == int(mod_id):
                        confirmacao_mod = True
            if not (confirmacao_mod or ai == dono):
                await c.send(f'<@{ai}>, você não tem permissão para usar esse comando!')
                return
            msg = m.split()[1]
            if msg.isnumeric():
                msg = int(msg)
            else:
                try:
                    msg = int(msg[-18:])
                except:
                    await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                    try:
                        await message.delete()
                    except:
                        pass
                    return
            sugestoes_chat_id = ler_elemento('config', 'ids_importantes', 'sugestoes')
            sugestoes_chat = client.get_channel(sugestoes_chat_id)
            try:
                msg = await sugestoes_chat.history().get(id=msg)
            except:
                await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                return
            motivo = m[(len(ml.split()[0])+len(ml.split()[1])+2):]
            if motivo == '':
                motivo = 'Gostamos da sugestão!'
            display_name_msg = (msg.embeds[0].title).replace('Sugestão de ', '')
            display_name_msg = display_name_msg[:(display_name_msg.find('(')-1)]
            autor_id_msg = int((msg.embeds[0].title[(msg.embeds[0].title.find('(')+1):]).replace(')', ''))
            ed = discord.Embed(
                title='Sugestão aprovada!',
                description=f'Sugestão de: {display_name_msg} ({autor_id_msg})',
                colour=discord.Colour.green()
            )
            ed.add_field(
                name='Sugestão feita:',
                value=msg.embeds[0].description,
                inline=False
            )
            ed.add_field(
                name='Motivo da aprovação:',
                value=motivo,
                inline=False
            )
            sugests_aprovadas = client.get_channel(ler_elemento('config', 'ids_importantes', 'sugests_feedback'))
            autor_msg = client.get_user(autor_id_msg)
            await msg.delete()
            try: await message.delete()
            except: pass
            await sugests_aprovadas.send(embed=ed)
            try:
                await autor_msg.send(embed=ed)
            except:
                pass
            await c.send(f'<@{ai}>, sugestão de {display_name_msg} ({autor_id_msg}) aprovada!')
            return
    except:
        pass
        

    # Reprovar sugestão
    try:
        if ml.split()[0] in reprovar_sugestao:  # PrefixAsugest <id ou link sugest> [motivo]
            confirmacao_mod = False
            for cargo in a.roles:
                for mod_id in ler_elemento('config', 'ids_importantes', 'mods_ids'):
                    if int(cargo.id) == int(mod_id):
                        confirmacao_mod = True
            if not (confirmacao_mod or ai == dono):
                await c.send(f'<@{ai}>, você não tem permissão para usar esse comando!')
                return
            msg = m.split()[1]
            if msg.isnumeric():
                msg = int(msg)
            else:
                try:
                    msg = int(msg[-18:])
                except:
                    await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                    try: await message.delete()
                    except: pass
                    return
            sugestoes_chat_id = ler_elemento('config', 'ids_importantes', 'sugestoes')
            sugestoes_chat = client.get_channel(sugestoes_chat_id)
            try:
                msg = await sugestoes_chat.history().get(id=msg)
            except:
                await c.send(f'<@{ai}>, favor inserir o id ou link da mensagem corretamente no primeiro parâmetro.')
                return
            motivo = m[(len(ml.split()[0])+len(ml.split()[1])+2):]
            if motivo == '':
                motivo = 'Não gostamos da sugestão!'
            display_name_msg = (msg.embeds[0].title).replace('Sugestão de ', '')
            display_name_msg = display_name_msg[:(display_name_msg.find('(')-1)]
            autor_id_msg = int((msg.embeds[0].title[(msg.embeds[0].title.find('(')+1):]).replace(')', ''))
            ed = discord.Embed(
                title='Sugestão reprovada!',
                description=f'Sugestão de: {display_name_msg} ({autor_id_msg})',
                colour=discord.Colour.red()
            )
            ed.add_field(
                name='Sugestão feita:',
                value=msg.embeds[0].description,
                inline=False
            )
            ed.add_field(
                name='Motivo da reprovação:',
                value=motivo,
                inline=False
            )
            sugests_aprovadas = client.get_channel(ler_elemento('config', 'ids_importantes', 'sugests_feedback'))
            autor_msg = client.get_user(autor_id_msg)
            await msg.delete()
            try: await message.delete()
            except: pass
            await sugests_aprovadas.send(embed=ed)
            try:
                await autor_msg.send(embed=ed)
            except:
                pass
            await c.send(f'<@{ai}>, sugestão de {display_name_msg} ({autor_id_msg}) reprovada!')
            return
    except:
        pass
    

    # Bater cartão
    if ml in [f'{prefix}batercartao', f'{prefix}bc'] and \
        ci == ler_elemento('config', 'ids_importantes', 'chat_bater_cartao'):
        horario = datetime.strftime(agora(), '%H:%M:%S')
        async def iniciar_cartao():
            guilds_staffs = ler_elemento('config', 'ids_importantes', 'guilds_staffs')
            servidores = []
            for s in guilds_staffs.items():
                servidor = client.get_guild(int(s[0]))
                try:
                    pessoa = get(servidor.members, id=ai)
                except:
                    return
                try:
                    for r in pessoa.roles:
                        if int(s[1]) == int(r.id):
                            servidores.append(servidor.name)
                except:
                    pass
            servidores_staff = ''
            len_servidores_m_1 = len(servidores) - 1
            count = 0
            for e in servidores:
                if count < (len_servidores_m_1 - 2):
                    servidores_staff = f'{servidores_staff}{e}, '
                elif count < len_servidores_m_1:
                    servidores_staff = f'{servidores_staff}{e} e '
                else:
                    servidores_staff = f'{servidores_staff}{e}'
                count += 1
            data = datetime.strftime(agora(), '%d/%m/%Y')
            msg = f':id:・**Id:** {ai}\n' \
                f':spy:・**Nome:** {dn}\n' \
                f':date:・**Data:** {data}\n' \
                f':bus:・**Qual/Quais servidores você e statff:** {servidores_staff}\n' \
                f':mailbox:・**Horário de entrada:** {horario}\n' \
                f':mailbox_closed:・**Horário de saída:**'
            msg = await c.send(msg)
            escrever_elemento('usuarios', ai, msg.id, 'bater_cartao')
            await message.delete()
            return
        if ler_elemento('usuarios', ai, 'bater_cartao') == f'Chave bater_cartao não encontrada!':
            await iniciar_cartao()
        else:
            hc = [message async for message in c.history()]
            msg_original = ''
            for msg in hc:
                if msg.id == int(ler_elemento('usuarios', ai, 'bater_cartao')):
                    msg_original = msg
            if msg_original != '':
                msg = f'{msg_original.content} {horario}'
            else:
                deletar_item('usuarios', ai, 'bater_cartao')
                await iniciar_cartao()
                return
            await msg_original.edit(content=msg)
            await message.delete()
            deletar_item('usuarios', ai, 'bater_cartao')
            return


    # Editar horário de saída
    if ml.startswith(f'{prefix}ebc') and \
        ci == ler_elemento('config', 'ids_importantes', 'chat_bater_cartao'):  # ebc <id da msg> <novo horario>
        ler_bc = ler_elemento('usuarios', ai, 'bater_cartao')
        if ler_bc != f'Chave bater_cartao não encontrada!':
            if int(ler_bc) == int(ml.split()[1]):
                aviso = await c.send(f'<@{ai}>, Esse cartão ainda está em andamento, favor terminá-lo antes.')
                await aviso.delete(delay=10)
                await message.delete()
                return
        try:
            msg = await c.history().get(id=int(ml.split()[1]))
        except:
            await message.delete()
            aviso = await c.send(f'<@{ai}>, mensagem não encontrada.')
            await aviso.delete(delay=10)
            return
        msg_c = msg.content
        id_autor = int(msg_c[(msg_c.lower().find('id:** ')+6):((msg_c.lower().find('id:** ')+24))])
        if id_autor != int(ai):
            await message.delete()
            aviso = await c.send(f'<@{ai}>, Você deve ser o autor da mensagem para poder editá-la.')
            await aviso.delete(delay=10)
            return
        try:
            novo_horario = ml.split()[2]
        except:
            await message.delete()
            aviso = await c.send(f'<@{ai}>, favor digitar um novo horário.')
            await aviso.delete(delay=10)
            return
        async def aviso_horario_errado():
            await message.delete()
            aviso = await c.send(f'<@{ai}>, favor digitar o novo horário corretamente (ex.: `08:59`)')
            await aviso.delete(delay=10)
            return
        try:
            int(novo_horario[:2])
            int(novo_horario[-2:])
            if novo_horario[2] != ':':
                await aviso_horario_errado()
        except:
            await aviso_horario_errado()
        novo_cartao = f'{msg_c[:-6]} {novo_horario}'
        await msg.edit(content=novo_cartao)
        await message.delete()
        return



    if ml.startswith(f'{prefix}lembrar') and \
        (ci == ler_elemento('config', 'ids_importantes', 'chat_comando_div') or ai == dono):
        try:
            parametro = ml.split()[1]
        except:
            await c.send('Você deve inserir o parâmetro `sim` ou `não`')
            return
        if parametro in ['s', 'sim', 'y', 'yes']:
            escrever_elemento('usuarios', ai, True, 'lembrete')
            escrever_elemento_lista('usuarios', 'lembretes', [ai, ler_elemento('usuarios', ai, 'compra', 'ult_div')])
            await c.send('Você será lembrado assim que estiver apto a divulgar.')
            return
        elif parametro in ['n', 'no', 'não', 'nao']:
            if ler_elemento('usuarios', ai, 'lembrete') != 'Chave lembrete não encontrado!':
                deletar_item('usuarios', ai, 'lembrete')
            for lembrete in ler_elemento('usuarios', 'lembretes'):
                if lembrete[0] == ai:
                    deletar_valor_lista('usuarios', 'lembretes', lembrete)
            await c.send('Você não será lembrado.')
            return
        else:
            await c.send('Você deve inserir o parâmetro `sim` ou `não`')            



    





    
# Iniciar bot
client.run(ler_elemento('config', 'token'))
