import os
import discord
import random
import sqlalchemy
from databases import Database
from discord.ext import commands


class Econ(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # freshly generate data for a new server
    @commands.command()
    async def generateserverdata(self, ctx):
        server = ctx.message.guild.id
        # currently, the bot uses "testdb" as its database. IDK if it would be better to generate a new database per
        # server, or if it would make more sense to just have one bigass file but... for now it's just a testing thing
        database = Database('sqlite:///testdb.db')
        await database.connect()
        # currently using raw queries in string form. maybe switch to using sqlalchemy?
        # creating the user table for the server - holds various info specific to each user like wallet etc.
        query = """CREATE TABLE IF NOT EXISTS '""" + str(server) + """_users' (
        user INTEGER PRIMARY KEY,
        wallet INTEGER,
        inventory TEXT,
        continence
        )"""
        await database.execute(query=query)
        # Just an idea for the shop, allow for certain items having a limit you can have at once,
        # and others having a limit for the number a user can ever purchase. I.E. "upgrade to Gold rank" can't be
        # purchased more than once, because it's a one-time upgrade.
        # table for the shop stuff, obvs.
        query = f"CREATE TABLE IF NOT EXISTS '{server}_shop' (name TEXT PRIMARY KEY, description TEXT, price INTEGER," \
                f"heldlimit INTEGER, purchaselimit INTEGER)"
        await database.execute(query=query)
        userlist = ctx.message.guild.members
        values = []
        for user in userlist:
            values.append({"user": user.id, "wallet": 0, "inventory": "{}", "continence": False})
        query = f"INSERT INTO '{server}_users'(user, wallet, inventory, continence) " \
                f"VALUES (:user, :wallet, :inventory, :continence)"
        await database.execute_many(query=query, values=values)
        await database.disconnect()
        await ctx.send("success!")

    # completely reset server data
    @commands.command()
    async def serverwipe(self, ctx):
        await ctx.send("Are you sure you want to wipe the server's data from my memory? This action cannot be undone.")
        usertable = str(ctx.message.guild.id) + "_users"
        shoptable = str(ctx.message.guild.id) + "_shop"
        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author and m.content.lower() in ('yes', 'no')
        confirmation = await self.bot.wait_for('message', timeout=60.0, check=check)
        if confirmation.content.lower() == 'yes':
            await ctx.send("got it, wiping everything.")
            database = Database('sqlite:///testdb.db')
            await database.connect()
            query = f"DROP TABLE IF EXISTS '{usertable}'"
            await database.execute(query=query)
            query = f"DROP TABLE IF EXISTS '{shoptable}'"
            await database.execute(query=query)
            await database.disconnect()
            await ctx.send("server deleted. use .generateserverdata to set things up again")
        elif confirmation.content.lower() == 'no':
            await ctx.send("Phew! That was a close one, huh?")

    # mostly a testing command though we may be able to do stuff with it in the future.
    # grabs the requested user's information from the user table for the server.
    @commands.command()
    async def getuserdata(self, ctx, user: discord.Member = None):
        server = ctx.message.guild.id
        if user is None:
            user = ctx.message.author
        user = user.id
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"SELECT * FROM '{server}_users' WHERE user = {user}"
        result = await database.fetch_one(query=query)
        await ctx.send(result)
        await database.disconnect()

    # mostly a testing command.
    # lists all of the users who are continent.
    @commands.command()
    async def getcontlist(self, ctx, continent="false"):
        if continent == "true" or continent == "True" or continent == "continent":
            continent = True
        else:
            continent = False
        server = ctx.message.guild.id
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"SELECT * FROM '{server}_users' WHERE continence = {continent}"
        result = await database.fetch_all(query=query)
        await ctx.send(result)
        await database.disconnect()

    # takes a specified user and attribute (ex. wallet) and returns and/or says that value.
    @commands.command()
    async def getuserattr(self, ctx, att, user: discord.Member = None):
        if user is None:
            user = ctx.author
        userid = user.id
        server = ctx.message.guild.id
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"SELECT {att} FROM '{server}_users' WHERE user = {userid}"
        result = await database.fetch_one(query=query)
        result = result[0]
        if ctx.command.name == "getuserattr":
            await ctx.send(f"{ctx.author.mention} {att} for {user.mention}: {result}")
        await database.disconnect()
        return result

    # returns and/or says a user's current wallet balance.
    @commands.command(aliases=["balance", "wallet", "cookiejar", "bank"])
    async def bal(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        userid = user.id
        server = ctx.message.guild.id
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"SELECT wallet FROM '{server}_users' WHERE user = {userid}"
        result = await database.fetch_one(query=query)
        result = result[0]
        if ctx.command.name == "bal":
            await ctx.send(f"{ctx.author.mention} {user.mention} has {result} cookies.")
        await database.disconnect()
        return result

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # IMPORTANT: DO NOT LET THIS SEE THE LIGHT OF DAY. EVER. LIKE, PROBABLY DELETE IT PERIOD.
    # LITERALLY JUST TAKES WHATEVER INPUT PROVIDED AS AN SQL QUERY AND RUNS IT WITHOUT QUESTION.
    @commands.command()
    async def executeraw(self, ctx):
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = ctx.message.content[11:]
        await database.execute(query=query)
        await ctx.send("done.")
        await database.disconnect()
    # IMPORTANT: DELETE BEFORE PUBLISHING FINAL BUILD
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # specifies a user, a value, and an attribute, sets that user's attribute to that value.
    @commands.command()
    async def setuserattr(self, ctx, att, value, user: discord.Member = None):
        if user is None:
            user = ctx.author
        userid = user.id
        server = ctx.message.guild.id
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"UPDATE '{server}_users' SET {att} = {value} WHERE user = {userid}"
        await database.execute(query=query)
        if ctx.command.name == "setuserattr":
            await ctx.send(f"{ctx.author.mention} {att} for {user.mention} set to {value}")
        await database.disconnect()

    # our !work command.
    @commands.command()
    async def play(self, ctx):
        user = ctx.message.author
        userid = user.id
        server = ctx.message.guild.id
        # currently, there is a 1 in 51 chance of getting a jackpot that drastically increases the value of the work.
        # determine the amount to reward the player with
        jackpot = random.randrange(0, 51)
        if jackpot == 51:
            jackpot = random.randrange(0, 500)
        jackpot = jackpot + 75
        # add the amount to the player's account
        database = Database('sqlite:///testdb.db')
        await database.connect()
        query = f"SELECT wallet FROM '{server}_users' WHERE user = {userid}"
        result = await database.fetch_one(query=query)
        result = result[0] + jackpot
        query = f"UPDATE '{server}_users' SET wallet = {result} WHERE user = {userid}"
        await database.execute(query=query)
        await database.disconnect()
        await ctx.send(f"{user.mention} you got {jackpot} cookies!")

    #deprecated code, will delete soonish
    # def findguild(self, ctx, finduser=False):
    #     guild = ctx.message.guild.id
    #     database_path = "database/Guilds/" + str(guild) + "/"
    #     if finduser:
    #         database_path = database_path + "Users/"
    #     return database_path
    #
    # #adds database path to file if path isn't already present
    # def getfile(self, ctx, file, finduser=False):
    #     database_path = self.findguild(ctx, finduser)
    #     if not database_path in file:
    #         file = database_path + file
    #     if not file_extension in file:
    #         file = file + file_extension
    #     return file
    #
    # def splitfile(self, file):
    #     if len(file) < 1:
    #         return None
    #     path = file.split("/")
    #     file = path.pop(-1)
    #     path = "/".join(path)
    #     return [file, path]
    #
    # #checks if a file exists within the database already
    # def fileexists(self, file):
    #     file = self.splitfile(file)
    #     if file[0] in os.listdir(file[1]):
    #         return True
    #     return False
    #
    # def readfile(self, ctx, file):
    #     file = self.getfile(ctx, file)
    #     if self.fileexists(file):
    #         with open(file, "r") as read_file:
    #             output = json.load(read_file)
    #             return output
    #     return None
    #
    # def writefile(self, ctx, file, data=None, user=False):
    #     file = self.getfile(ctx, file, user)
    #     if data is None:
    #         return
    #     with open(file, "w") as write_file:
    #         json.dump(data, write_file)
    #
    # #TESTING COMMANDS: DO NOT USE FOR REALSIES
    # @commands.command(aliases=["readme"])
    # @commands.has_permissions(administrator=True)
    # async def printfile(self, ctx, file=""):
    #     self.findguild(ctx)
    #     file = self.getfile(ctx, file)
    #     output = self.readfile(ctx, file)
    #     if output is not None:
    #         await ctx.send(f'<@{ctx.author.id}> {output}')
    #         return
    #     await ctx.send(f'<@{ctx.author.id}> {file} doesn\'t exist yet.')
    #
    # @commands.command(aliases=[])
    # async def printuser(self, ctx, file: discord.Member = None):
    #     path = self.findguild(ctx, True) + str(file.id)
    #     path = self.getfile(ctx, path)
    #     output = self.readfile(ctx, path)
    #     if file.color.value == 0x000000:
    #         embdcolor = 0x008282
    #     else:
    #         embdcolor = file.color.value
    #     embd = discord.Embed(color=embdcolor)
    #     embd.set_author(name=file.name + str(file.discriminator), url=discord.Embed.Empty, icon_url=file.avatar_url)
    #     for att in output:
    #         if isinstance(output[att], dict):
    #             dickt = output[att]
    #             attstring = ""
    #             for x in dickt:
    #                 attstring = attstring + x + ": " + dickt[x] + "\n"
    #             embd.add_field(name=att, value=attstring)
    #
    #         else:
    #             embd.add_field(name=att, value=output[att])
    #     if output is not None:
    #         await ctx.send(embed=embd)
    #         return
    #     await ctx.send(f'<@{ctx.author.id}> {file} doesn\'t exist yet.')
    #
    # #this will literally write whatever is entered into a file be very careful with it
    # @commands.command(aliases=["newfile"])
    # @commands.has_permissions(administrator=True)
    # async def updatefile(self, ctx, file="", data=""):
    #     await ctx.send(f'{self.findguild(ctx)}')
    #     file = self.getfile(ctx, file)
    #     self.writefile(file, ctx, data)
    #     await ctx.send(f'<@{ctx.author.id}> {file} successfully written')
    #
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def addallusers(self, ctx, reset=False):
    #     await ctx.send(f'<@{ctx.author.id}> Adding all users to the database. This may take a while.')
    #     async with ctx.channel.typing():
    #         userlist = ctx.message.guild.members
    #         for user in userlist:
    #             await ctx.send(f'{user}')
    #             await self.adduser(ctx, user, reset)
    #     await ctx.send(f'<@{ctx.author.id}> done.')
    #
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def adduser(self, ctx, user: discord.Member = None, reset=False):
    #     if user == None:
    #         await ctx.send(f'<@{ctx.author.id}> No member specified, or member does not exist.')
    #         return
    #     file = self.getfile(ctx, "Users/" + str(user.id))
    #     if self.fileexists(file) and not reset:
    #         if ctx.command.name == "adduser":
    #             await ctx.send(f'<@{ctx.author.id}> User already existed.')
    #         else:
    #             await ctx.send(f'User already added.')
    #         return
    #     data = {
    #         "cookie jar": "0",
    #         "inventory": "cookie jar",
    #         "babytalk": {"on/off": "off", "timer": "None"},
    #         "diaper checks": "0",
    #         "contracts": {"None": "None"},
    #         # note: {"example": {"role": "contractor", "terms": "None", "time": "0", "punishment/reward": "None/None"}}
    #         "tutorial progress": "None",
    #         "hypnotized": {"tist": "None", "timer": "None"}
    #     }
    #     self.writefile(ctx, file, data)
    #     await ctx.send(f'User successfully added.')
    #     if ctx.command.name == "adduser":
    #         await ctx.send(f'<@{ctx.author.id}> User successfully added!')
    #
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def editatt(self, ctx, user: discord.Member=None, attr=None, args=""):
    #     if user is None:
    #         user = ctx.author
    #     if attr is None:
    #         if ctx.command.name == "editattr":
    #             await ctx.send(f'<@{ctx.author.id}> Error: No attribute specified.')
    #             return
    #         return None
    #     file = self.getfile(ctx, str(user.id), True)
    #     output = self.readfile(ctx, file)
    #
    #     output[attr] = args
    #     self.writefile(ctx, file, output, True)
    #     if ctx.command.name == "editattr":
    #         await ctx.send(f'<@{ctx.author.id}> {attr} successfully set to {args}')
    #     # finally:
    #     #     if True or ctx.command.name == "editattr":
    #     #         await ctx.send(f'<@{ctx.author.id}> Error: {attr} cannot be set to {args}')
    #     #         return
    #     return
    #
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def getatt(self, ctx, user: discord.Member = None, attr=None, *args):
    #     if user is None:
    #         user = ctx.author
    #     if attr is None:
    #         if ctx.command.name == "editattr":
    #             await ctx.send(f'<@{ctx.author.id}> Error: No attribute specified.')
    #             return
    #         return None
    #     file = self.getfile(ctx, str(user.id), True)
    #     output = self.readfile(ctx, file)
    #     if attr in output:
    #         if ctx.command.name == "getattr":
    #             await ctx.send(f'<@{ctx.author.id}> {output[attr]}')
    #         else:
    #             return output[attr]
    #
    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # async def serverinit(self, ctx):
    #     guilddir = "database/Guilds/" + str(ctx.message.guild.id) + "/"
    #     if not str(ctx.message.guild.id) in os.listdir("database/Guilds/"):
    #         os.mkdir(guilddir)
    #         await ctx.send(f'<@{ctx.author.id}> Guild added!')
    #     if not "Users/" in os.listdir(guilddir):
    #         os.mkdir(guilddir + "Users/")
    #         await ctx.send(f'<@{ctx.author.id}> User folder added!')
    #     await ctx.send(f'<@{ctx.author.id}> All done!')



def setup(bot):
    bot.add_cog(Econ(bot))
