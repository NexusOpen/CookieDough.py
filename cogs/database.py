import os
import discord
from databases import Database
from discord.ext import commands


class Database(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def generateserverdata(self, ctx):
        server = ctx.message.guild.id
        database = Database('sqlite///testdb.db')


    @commands.command()
    async def getuserdata(self, user=None):
        if user is None:
            return None
        database = Database('sqlite///testdb.db')
        await database.connect()
        query = """"""
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
    bot.add_cog(Database(bot))
