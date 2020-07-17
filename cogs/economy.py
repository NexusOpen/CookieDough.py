import logging
import discord
from discord import Member
from discord.ext import commands
import aiohttp
import asyncio
import json
import random

log = logging.getLogger("cogs.testing")


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = self.bot.get_cog("Database")
        self.transferinprogress = False

    @commands.command(aliases=["bal", "cookies", "money", "cookiejar"])
    async def balance(self, ctx, user: Member=None):
        if user is None:
            user = ctx.author
        path = self.database.findguild(ctx, True) + str(user.id)
        path = self.database.getfile(ctx, path)
        output = self.database.readfile(ctx, path)
        if ctx.command.name == "balance":
            if user.color.value == 0x000000:
                embdcolor = 0x008282
            else:
                embdcolor = user.color.value
            embd = discord.Embed(color=embdcolor)
            embd.set_author(name=user.name + str(user.discriminator), url=discord.Embed.Empty, icon_url=user.avatar_url)
            embd.add_field(name="Cookie Jar", value=":cookie:" + output["cookie jar"])
            # for att in output:
            #     if isinstance(output[att], dict):
            #         dickt = output[att]
            #         attstring = ""
            #         for x in dickt:
            #             attstring = attstring + x + ": " + dickt[x] + "\n"
            #         embd.add_field(name=att, value=attstring)
            #
            #     else:
            #         embd.add_field(name=att, value=output[att])
            if output is not None:
                await ctx.send(embed=embd)
                return
            await ctx.send(f'<@{ctx.author.id}> {user} doesn\'t exist yet.')
        elif output is not None:
            return output["cookie jar"]
        return None

    @commands.command(aliases=["givecookies", "addmoney"])
    @commands.has_permissions(administrator=True)
    async def addcookies(self, ctx, user: Member=None, cookies=0):
        if user is None:
            if True or ctx.command.name == "addcookies":
                await ctx.send(f'<@{ctx.author.id}> You didn\'t tell me who to give the cookies to!')
            return False
        balance = await self.balance(ctx, user)
        balance = int(balance) + cookies
        await self.database.editatt(ctx, user, "cookie jar", str(balance))
        if ctx.command.name == "addcookies":
            await ctx.send(f'<@{ctx.author.id}> I gave {user} {cookies} cookies!')

    @commands.command(aliases=["takecookies", "subtractmoney"])
    @commands.has_permissions(administrator=True)
    async def subtractcookies(self, ctx, user: Member = None, cookies=0):
        if user is None:
            if ctx.command.name == "subtractcookies":
                await ctx.send(f'<@{ctx.author.id}> You didn\'t tell me who to take the cookies from!')
            return False
        balance = await self.balance(ctx, user)
        balance = int(balance) - cookies
        if balance < 0:
            balance = 0
        await self.database.editatt(ctx, user, "cookie jar", str(balance))
        if ctx.command.name == "subtractcookies":
            await ctx.send(f'<@{ctx.author.id}> I took {cookies} cookies from {user}!')

    @commands.command(aliases=["play"])
    async def work(self, ctx):
        user = ctx.author
        path = self.database.findguild(ctx, True) + str(user.id)
        path = self.database.getfile(ctx, path)
        output = self.database.readfile(ctx, path)
        if ctx.command.name == "work":
            earnings = random.randrange(20)
            if earnings == 20:
                earnings = random.randrange(75, 500)
            else:
                earnings = random.randrange(75, 125)
            if user.color.value == 0x000000:
                embdcolor = 0x008282
            else:
                embdcolor = user.color.value
            embd = discord.Embed(color=embdcolor)
            embd.set_author(name=user.name + str(user.discriminator), url=discord.Embed.Empty, icon_url=user.avatar_url)
            embd.add_field(name="test", value=":cookie:" + str(earnings) + " awarded.")
            await self.addcookies(ctx, user, earnings)
            if output is not None:
                await ctx.send(embed=embd)
                return
            await ctx.send(f'<@{ctx.author.id}> {user} doesn\'t exist yet.')
        return None

    @commands.command(aliases=["pay"])
    async def give(self, ctx, user: Member=None, cookies=0):
        if user is None:
            if True or ctx.command.name == "give":
                await ctx.send(f'<@{ctx.author.id}> You didn\'t tell me who to give the cookies to!')
            return False
        if cookies < 1:
            await ctx.send(f'<@{ctx.author.id}> You need to give me a valid number of cookies to give!')
            return False
        if self.transferinprogress:
            await ctx.send(f'<@{ctx.author.id}> Sorry, I\'m in the middle of something. Gimme one sec.')
            return
        if cookies > int(await self.balance(ctx, ctx.author)):
            await ctx.send(f'<@{ctx.author.id}> You don\'t have that many cookies to give!')
            return
        self.transferinprogress = True
        await self.addcookies(ctx, user, cookies)
        await self.subtractcookies(ctx, ctx.author, cookies)
        self.transferinprogress = False
        subject = user
        user = ctx.author
        if user.color.value == 0x000000:
            embdcolor = 0x008282
        else:
            embdcolor = user.color.value
        embd = discord.Embed(color=embdcolor)
        embd.set_author(name=user.name + str(user.discriminator), url=discord.Embed.Empty, icon_url=user.avatar_url)
        embd.add_field(name="test", value=user.mention + "gave :cookie:" + str(cookies) + " to " + subject.mention)
        await ctx.send(embed=embd)


def setup(bot):
    bot.add_cog(Economy(bot))
