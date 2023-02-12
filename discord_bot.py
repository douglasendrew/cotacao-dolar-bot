import discord
from discord.ext import commands
import requests
# import json
import asyncio


class Client(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        super(commands.Bot, self).__init__(command_prefix, intents=intents)
        self.add_commands()

    # Outros comandos do Bot
    def add_commands(self):
        print('Funcionando')

        @self.command(name="status", pass_context=True)
        async def status(ctx):
            print(ctx)
            await ctx.send('Legal')

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.refresh_dolar())

    async def on_ready(self):
        channel = self.get_channel(1074194502778110027)
        await channel.send('Onlineeee!')
        await self.refresh_dolar()

    num = ''

    def last_value(self, value):
        global num
        num = value

    # Faz o refresh no valor do dolar
    async def refresh_dolar(self):

        requisicao = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
        cotacao = requisicao.json()
        val = str(round(float(cotacao['USD']['bid']), 2))

        if val != self.last_value:

            self.last_value(val)

            embed = discord.Embed(
                title='Dolar Agora',
                description='Dolar está em: R$ ' + val,
                colour=discord.Colour.blue()
            )

            max = cotacao['USD']['high']
            min = cotacao['USD']['low']

            embed.set_footer(text=f'Máximo: R$ {max} | Mínimo: R$ {min}')

            channel = self.get_channel(1074194502778110027)
            while not self.is_closed():
                await channel.send(embed=embed)
                await asyncio.sleep(10)

        else:
            embed = discord.Embed(
                title='Dolar Agora',
                description='Nao teve alteraçao',
                colour=discord.Colour.blue()
            )

            channel = self.get_channel(1074194502778110027)
            while not self.is_closed():
                await channel.send(embed=embed)
                await asyncio.sleep(10)


# Client RUN
client = Client(command_prefix="!")
client.run('MTA3NDE5NDAyOTM0MTgzOTQ2MQ.GWdMY0.zzmWczj9HoZH0p4dP0jASlencQq0L80zdtSF-s')
