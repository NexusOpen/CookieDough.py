import logging
from discord import Member
from discord import User
from discord.ext import commands
import aiohttp
import asyncio
import json
import random

log = logging.getLogger("cogs.testing")


class Testing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["getuseravatar", "avatar"])
    async def getuserpic(self, ctx, user: User=None):
        await ctx.send(f'{ctx.author.mention} {user.avatar_url}')

    @commands.command(aliases=["testcommandwrite"])
    async def testjsonwrite(self, ctx):
        data = {
            "scoutmaster": {
                "name": "Cookie Dough",
                "continence": "Incontinent"
            }
        }
        with open("testingdoc.json", "w") as write_file:
            json.dump(data, write_file)
            await ctx.send(f'<@{ctx.author.id}> Wow, I just took a *massive* dump.')

    @commands.command(aliases=["suckit", "fuckyou", "errorhell"])
    async def suckmydickyoustupidrobot(self, ctx):
        wittyretorts = ["no u", "eat a fat one, moron", "go fuck yourself.",
                        "how \'bout you write the code properly, then?", "this is your fault, not mine.",
                        "I can only work with what you give me, dickweed.",
                        "you can shove that complaint straight up your ass.", "kiss my ass", "fuck you too!"]
        comeback = random.choice(wittyretorts)
        await ctx.send(f'<@{ctx.author.id}> {comeback}')


    @commands.command(aliases=["testcommanddelete"])
    async def testjsondelete(self, ctx, userid=""):
        if userid != "":
            with open("testingdoc.json", "r") as read_file:
                file = json.load(read_file)
            with open("testingdoc.json", "w") as write_file:
                if userid in file:
                    file.pop(userid)
                json.dump(file, write_file)


    @commands.command(aliases=["testcommandwrite2"])
    async def addtofile(self, ctx, member: Member = None, continence=True):
        if member is None:
            await ctx.send(f'Who the hell should I add, moron?')
            return
        user = str(member.id)
        userdict = {
            "name": member.display_name,
            "continence": str(continence)
        }
        with open("testingdoc.json", "r") as read_file:
            file = json.load(read_file)
            file[user] = userdict
            # if user in file:
            #     file[user]["continence"] = continence
            # else:
            #     file[user]
        with open("testingdoc.json", "w") as write_file:
            json.dump(file, write_file)
            await ctx.send(f'<@{ctx.author.id}> user added and/or updated!')

    @commands.command(aliases=["testcommandread"])
    async def testjsonread(self, ctx, user=None):
        if user is not None:
            if user[:3] == '<@!':
                user = user[3:]
            if user[-1] == '>':
                user = user[:-1]
            with open("testingdoc.json", "r") as read_file:
                data = json.load(read_file)
                if user in data:
                    output = "incontinent"
                    if data[user]["continence"] == "True":
                        output = "continent"
                    await ctx.send(f'User <@{user}> is {output}')
                else:
                    await ctx.send(f'Hey dipshit, wrong username.')
        else:
            with open("testingdoc.json", "r") as read_file:
                data = json.load(read_file)
                await ctx.send(f'<@{ctx.author.id}> This is a huge load. {data}')
                for x in data:
                    output = "incontinent"
                    if data[x]["continence"] == "True":
                        output = "continent"
                    await ctx.send(f'User <@{x}>, named \"{data[x]["name"]}\", is {output}')


def setup(bot):
    bot.add_cog(Testing(bot))
