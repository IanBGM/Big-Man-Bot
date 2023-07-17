import sqlite3

import nextcord
from nextcord.ext import commands
from External import Colors, block_check


class Holder(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage="say <message>")
    @commands.is_owner()
    async def say(self, ctx, *, msg):
        """Holder Only!! Restricted command"""
        await ctx.reply("Ay (" + "".join(msg) + ")", mention_author=False)

    @commands.group(usage='bmd <command>', invoke_without_command=True)
    @commands.is_owner()
    async def bmd(self, ctx):
        """Holder Only!! Restricted command"""
        return

    # noinspection SpellCheckingInspection
    @bmd.command(aliases=['abmd'], usage="addb <amount> [member]")
    @commands.is_owner()
    async def addb(self, ctx, amount: int, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {member.id}")
        wallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
        except:
            wallet = 0

        sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
        val = wallet + int(amount), member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been added **{amount} BMD**! Use it wisely!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @bmd.command(aliases=['rbmd'], usage="removeb <amount> [member]")
    @commands.is_owner()
    async def removeb(self, ctx, amount: int, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {member.id}")
        wallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
        except:
            wallet = 0

        sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
        val = wallet - int(amount), member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been removed **{amount} BMD**!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @bmd.command(aliases=['sbmd'], usage="setb <amount> [member]")
    @commands.is_owner()
    async def setb(self, ctx, amount: int, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
        val = amount, member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been set **{amount} BMD**!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    @commands.group(usage='item <command>', invoke_without_command=True)
    @commands.is_owner()
    async def item(self, ctx):
        """Holder Only!! Restricted command"""
        return

    # noinspection SpellCheckingInspection
    @item.command(aliases=['aitem'], usage="addi <column> <amount> [member]")
    @commands.is_owner()
    async def addi(self, ctx, column: str, amount: int = 1, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        # noinspection PyBroadException
        try:
            cursor.execute(f"SELECT {column} FROM inv WHERE user_id = {member.id}")
            item = cursor.fetchone()
        except:
            return await ctx.send("Ay.. (Something went wrong.. is that column correct?)")

        # noinspection PyBroadException
        try:
            item = item[0]
        except:
            item = 0

        sql = f"UPDATE inv SET {column} = ? WHERE user_id = ?"
        val = item + int(amount), member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been added `{amount}x {column}`!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @item.command(aliases=['ritem'], usage="removei <column> <amount> [member]")
    @commands.is_owner()
    async def removei(self, ctx, column: str, amount: int = 1, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        # noinspection PyBroadException
        try:
            cursor.execute(f"SELECT {column} FROM inv WHERE user_id = {member.id}")
            item = cursor.fetchone()
        except:
            return await ctx.send("Ay.. (Something went wrong.. is that column correct?)")

        # noinspection PyBroadException
        try:
            item = item[0]
        except:
            item = 0

        sql = f"UPDATE inv SET {column} = ? WHERE user_id = ?"
        val = item - int(amount), member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been removed `{amount}x {column}`!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @item.command(aliases=['sitem'], usage="seti <column> <amount> [member]")
    @commands.is_owner()
    async def seti(self, ctx, column: str, amount: int = 1, member: nextcord.Member = None):
        """Holder Only!! Restricted command"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        sql = f"UPDATE inv SET {column} = ? WHERE user_id = ?"
        val = amount, member.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! ({member.mention} has been set `{amount}x {column}`!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['db'], usage='sqlite <file> <code>')
    @commands.is_owner()
    async def sqlite(self, ctx, file, *, code):
        """Holder Only!! Restricted command"""

        code = block_check(code)

        db = sqlite3.connect(file)
        cursor = db.cursor()

        try:
            cursor.execute(code)
        except sqlite3.OperationalError:
            return await ctx.send("Ay.. (Something went wrong..)")
        await ctx.send("Ay! (Sqlite Code has been executed!)")
        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=["announce"], usage="announcement <message>")
    @commands.is_owner()
    async def announcement(self, ctx, *, message):
        """Holder Only!! Restricted command"""

        for channel in ctx.guild.text_channels:
            try:
                embed = nextcord.Embed(title="Ay! (Developer Announcement!)", description=f"{message}", colour=Colors.dark_grey, timestamp=ctx.message.created_at)
                embed.set_footer(text="Ay! (This message was announced by a developer of me, please read if you'd like as it may contain major updates!)")
                await channel.send(embed=embed)
                break
            except:
                continue

    async def cog_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.NotOwner):
            return await ctx.send(f'Ay!? (You don\'t seem to be my Holder!? This command is restricted for you!)')

        await ctx.send(f"Ay.. (An error has occurred in my Holder Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Holder Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*Ay! (**{ctx.guild.name}**)*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Holder(client))
