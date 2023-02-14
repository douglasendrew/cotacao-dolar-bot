import discord
from discord.ext import commands
import requests
# Funçao onde pega o token do Discord
import token_1
# import json
import asyncio


class Client(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.all()
        super(commands.Bot, self).__init__(command_prefix, intents=intents)
        self.add_commands()

    # Outros comandos do Bot
    def add_commands(self):
        print("Carregando comandos!")

        @self.command(name="v", pass_context=True)
        async def v(ctx):
            await ctx.send(f"{ctx.author.mention}, este bot está na versao 1.0!")

    async def setup_hook(self) -> None:
        self.bg_task = self.loop.create_task(self.refresh_dolar())

    async def on_ready(self):
        channel = self.get_channel(1074194502778110027)
        await channel.send("Acompanhamento do dólar iniciado")
        await self.refresh_dolar()

    # Faz o refresh no valor do dolar
    async def refresh_dolar(self):
        channel = self.get_channel(1074194502778110027)
        value_l = ""

        while not self.is_closed():
            requisicao = requests.get("https://economia.awesomeapi.com.br/all/USD-BRL")
            cotacao = requisicao.json()
            val = str(round(float(cotacao["USD"]["bid"]), 2))

            if val != value_l:
                print(f"Valor Agora: {value_l}")
                value_l = str(val)
                embed = discord.Embed(
                    title="Dólar",
                    description="Dolar teve uma alteraçao, agora está em: R$ " + val,
                    colour=discord.Colour.green(),
                )

                max = cotacao["USD"]["high"]
                min = cotacao["USD"]["low"]

                embed.set_footer(text=f"Máximo: R$ {max} | Mínimo: R$ {min}")

                channel = self.get_channel(1074194502778110027)
                await channel.send(embed=embed)
                await asyncio.sleep(600)

            else:
                print(f"Valor Agora: {value_l}")
                await asyncio.sleep(300)


# Client RUN
client = Client(command_prefix="!")
client.run(token_1.Token.get_token())
