import asyncio
import sqlite3
import datetime

import humanfriendly
import nextcord
from nextcord.ext import commands

from External import Colors


class Management(commands.Cog):
    def __init__(self, client):
        self.client = client

    # region SYSTEM

    @commands.group(usage='system [command]', invoke_without_command=True)
    async def system(self, ctx):
        """Configure system-related commands!"""
        return await ctx.send("Ay! (Here are the System Commands: `enable, disable`)")

    @system.command(usage='system enable [system_name]')
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, system_name: str):
        """Enable built-in systems!"""

        system_names = ['LEVELING_SYSTEM', 'ECONOMY_SYSTEM', 'STARBOARD_SYSTEM']

        if system_name.upper() not in system_names:
            return await ctx.send("Ay.. (I couldn't find that system.. Here are my current ones: `" + ", ".join(system_names) + "`)")

        guild = ctx.guild

        levelDb = sqlite3.connect('level.sqlite')
        levelCursor = levelDb.cursor()
        currDb = sqlite3.connect('curr.sqlite')
        currCursor = currDb.cursor()
        mainDb = sqlite3.connect('main.sqlite')
        mainCursor = mainDb.cursor()

        if system_name.upper() == system_names[0]:

            levelCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = levelCursor.fetchone()

            if enabled:
                if enabled[0]:
                    return await ctx.send("Ay! (Leveling is already enabled in this server!)")
                levelCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                levelCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                levelDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            levelDb.commit()

            await ctx.send("Ay! (Leveling has been enabled for this server!)")
            levelCursor.close()
            levelDb.close()

        if system_name.upper() == system_names[1]:

            currCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = currCursor.fetchone()

            if enabled:
                if enabled[0]:
                    return await ctx.send("Ay! (Economy is already enabled in this server!)")
                currCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                currCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                currDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            currDb.commit()

            await ctx.send("Ay! (Economy has been enabled for this server!)")
            currCursor.close()
            currDb.close()

        if system_name.upper() == system_names[2]:

            mainCursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
            enabled = mainCursor.fetchone()

            if enabled:
                if enabled[0]:
                    return await ctx.send("Ay! (Starboard is already enabled in this server!)")
                mainCursor.execute('UPDATE starSystem SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                mainCursor.execute('INSERT INTO starSystem (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                mainDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            mainDb.commit()

            await ctx.send("Ay! (Starboard has been enabled for this server!)")
            mainCursor.close()
            mainDb.close()

    @system.command(usage='system disable [system_name]')
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, system_name: str):
        """Disable built-in systems!"""

        system_names = ['LEVELING_SYSTEM', 'ECONOMY_SYSTEM', 'STARBOARD_SYSTEM']

        if system_name.upper() not in system_names:
            return await ctx.send("Ay.. (I couldn't find that system.. Here are my current ones: `" + ", ".join(system_names) + "`)")

        guild = ctx.guild

        levelDb = sqlite3.connect('level.sqlite')
        levelCursor = levelDb.cursor()
        currDb = sqlite3.connect('curr.sqlite')
        currCursor = currDb.cursor()
        mainDb = sqlite3.connect('main.sqlite')
        mainCursor = mainDb.cursor()

        if system_name.upper() == system_names[0]:

            levelCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = levelCursor.fetchone()

            if enabled:
                if not enabled[0]:
                    return await ctx.send("Ay! (Leveling is already disabled in this server!)")
                levelCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                levelCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                levelDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            levelDb.commit()

            await ctx.send("Ay! (Leveling has been disabled for this server!)")
            levelCursor.close()
            levelDb.close()

        if system_name.upper() == system_names[1]:

            currCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = currCursor.fetchone()

            if enabled:
                if not enabled[0]:
                    return await ctx.send("Ay! (Economy is already disabled in this server!)")
                currCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                currCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                currDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            currDb.commit()

            await ctx.send("Ay! (Economy has been disabled for this server!)")
            currCursor.close()
            currDb.close()

        if system_name.upper() == system_names[2]:

            mainCursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
            enabled = mainCursor.fetchone()

            if enabled:
                if not enabled[0]:
                    return await ctx.send("Ay! (Starboard is already disabled in this server!)")
                mainCursor.execute('UPDATE starSystem SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
                mainCursor.execute('INSERT INTO starSystem (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                mainDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            mainDb.commit()

            await ctx.send("Ay! (Starboard has been disabled for this server!)")
            mainCursor.close()
            mainDb.close()

    # @system.command(usage='system prefix [prefix]')
    # async def prefix(self, ctx, prefix):
    #     """Sets the prefix! (default for Default Prefix)"""
    #     guild = ctx.guild
    #
    #     if prefix == "default":
    #         return
    #
    #     db = sqlite3.connect('main.sqlite')
    #     cursor = db.cursor()
    #     cursor.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {guild.id}')
    #     data = cursor.fetchone()
    #
    #     if data:
    #         cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild_id = ?', (prefix, guild.id))
    #         await ctx.send(f'Ay! (Prefix has been updated to {prefix}!)')
    #     else:
    #         msg = await ctx.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)")
    #         cursor.execute('INSERT INTO prefixes (guild_id, prefix) VALUES (?, ?)', ("manta ", guild.id))
    #         db.commit()
    #         return await msg.edit("Ay! (Complete adding system data!)")

    # endregion

    # region STARBOARD

    @commands.group(name='star-setup', usage=['star-setup [command]'], invoke_without_command=True)
    async def star_setup(self, ctx):
        """Configure starboard-related commands!"""
        return await ctx.send("Ay! (Here are the Starboard Setup Commands: `channel, limit`)")

    @star_setup.command(usage='star-setup channel <channel>')
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: nextcord.TextChannel):
        """Set the channel for Starboard!"""

        guild = ctx.guild

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Starboard is currently disabled for this server..)')

        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {guild.id}')
        channelData = cursor.fetchone()

        if channelData:
            channelData = channelData[0]

            if channelData == channel.id:
                return await ctx.send("Ay! (That channel is already the starboard channel!)")
            cursor.execute('UPDATE starboard SET channel_id = ? WHERE guild_id = ?', (channel.id, guild.id))
            await ctx.send(f"Ay! (The starboard channel has now been set to {channel.mention}!)")
        else:
            msg = await ctx.send("Ay.. (I couldn't find any starboard data for this server.. Creating it now! Try using starboard setup commands again afterwards..")
            cursor.execute('INSERT INTO starboard (guild_id, channel_id, stars) VALUES (?, ?, ?)', (guild.id, channel.id, 5))
            db.commit()
            return await msg.edit("Ay! (Complete adding starboard data!)")
        db.commit()
        cursor.close()
        db.close()

    @star_setup.command(usage='star-setup limit <limit>')
    @commands.has_permissions(manage_guild=True)
    async def limit(self, ctx, limit: int):
        """Set the channel for Starboard!"""

        guild = ctx.guild

        if limit == 0:
            return await ctx.send('Ay.. (You cannot set the star limit to **0**..)')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Starboard is currently disabled for this server..)')

        cursor.execute(f'SELECT stars FROM starboard WHERE guild_id = {guild.id}')
        limitData = cursor.fetchone()

        if limitData:
            limitData = limitData[0]

            if limit == limitData:
                return await ctx.send("Ay! (That star limit is already the starboard star limit!)")
            cursor.execute('UPDATE starboard SET stars = ? WHERE guild_id = ?', (limit, guild.id))
            await ctx.send(f"Ay! (The starboard star limit has now been set to **{limit}**!)")
        else:
            msg = await ctx.send("Ay.. (I couldn't find any starboard data for this server.. Creating it now! Try using starboard setup commands again afterwards..")
            cursor.execute('INSERT INTO starboard (guild_id, channel, stars) VALUES (?, ?, ?)', (guild.id, 0, 5, True))
            db.commit()
            return await msg.edit("Ay! (Complete adding starboard data!)")
        db.commit()
        cursor.close()
        db.close()

    # endregion

    # @commands.command(name="clean-invites", aliases=['delete-invites', 'del-invites'], usage='clean-invites')
    # @commands.cooldown(1, 30, commands.BucketType.guild)
    # @commands.has_permissions(manage_guild=True)
    # async def clean_invites(self, ctx):
    #     """Clean all invites in the server!"""
    #     await ctx.send("Ay? (Are you sure you want to clean all the invites?)")
    #
    #     def check(m):
    #         return m.author == ctx.author and m.channel == ctx.channel
    #
    #     try:
    #         response = await self.client.wait_for('message', check=check, timeout=30)
    #     except asyncio.TimeoutError:
    #         return await ctx.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')
    #
    #     if response.content.lower() not in ("yes", "y"):
    #         return await ctx.send("Ay! (Operation Aborted!)")
    #
    #     msg = await ctx.send("Ay.. (Purging invites..)")
    #
    #     for invite in await ctx.guild.invites():
    #         await invite.delete()
    #
    #     await msg.edit("Ay! (Operation Complete! All invites have been purged!)")
    #
    # @commands.command(name="clean-roles", aliases=['delete-roles', 'del-roles'], usage='clean-roles')
    # @commands.cooldown(1, 30, commands.BucketType.guild)
    # @commands.has_permissions(manage_roles=True)
    # async def clean_roles(self, ctx):
    #     """Clean all roles in the server!"""
    #     await ctx.send("Ay? (Are you sure you want to clean all the roles?)")
    #
    #     def check(m):
    #         return m.author == ctx.author and m.channel == ctx.channel
    #
    #     try:
    #         response = await self.client.wait_for('message', check=check, timeout=30)
    #     except asyncio.TimeoutError:
    #         return await ctx.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')
    #
    #     if response.content.lower() not in ("yes", "y"):
    #         return await ctx.send("Ay! (Operation Aborted!)")
    #
    #     msg = await ctx.send("Ay.. (Purging roles..)")
    #
    #     for role in ctx.guild.roles:
    #         # noinspection PyBroadException
    #         try:
    #             await role.delete()
    #         except:
    #             continue
    #
    #     await msg.edit("Ay! (Operation Complete! All roles have been purged!)")

    @commands.command(aliases=['boot'], usage='kick <member> [reason]')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        """Kicks whoever needs to be kicked!"""

        if member == ctx.author:
            return await ctx.send("Ay!? (Kicking yourself!? Almost impossible!)")
        if member == self.client.user:
            return await ctx.send("Ay!? (Kicking **me**!? Almost impossible!)")

        kickEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay! (Kick Success!)", timestamp=ctx.message.created_at,
                                   description=f"*Ay! (**ID:** `{member.id}`)*\n*Ay! (**Username:** `{member.name}`)*\n*Ay! (**Tag:** `{member.discriminator}`)*\n*Ay! (**Reason:** `{reason}`)*")

        await member.kick(reason=reason)
        await ctx.send(embed=kickEmbed)

    @commands.command(aliases=['hammer'], usage='ban <member> [reason]')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """Bans whoever needs to be banned!"""

        if member == ctx.author:
            return await ctx.send("Ay!? (Banning yourself!? Almost impossible!)")
        if member == self.client.user:
            return await ctx.send("Ay!? (Banning **me**!? Almost impossible!)")

        banEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay! (Ban Success!)", timestamp=ctx.message.created_at,
                                  description=f"*Ay! (**ID:** `{member.id}`)*\n*Ay! (**Username:** `{member.name}`)*\n*Ay! (**Tag:** `{member.discriminator}`)*\n*Ay! (**Reason:** `{reason}`)*")

        await member.ban(reason=reason)
        await ctx.send(embed=banEmbed)

    @commands.command(aliases=['clean', 'purge'], usage='clear <amount>')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        """Clears out messages!"""
        if amount < 1:
            return await ctx.send("Ay.. (You have to clear 1 or more messages..)")

        if amount > 100:
            return await ctx.send("Ay.. (Cannot purge more than 100 messages..)")
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'Ay! (I have cleared out {amount} messages in this channel!)', delete_after=5)

    @commands.command(aliases=['mute'], usage='timeout <member> <time>')
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: nextcord.Member, time, *, reason=None):
        """Timeout members for duration of time!"""

        # noinspection PyBroadException
        try:
            time = humanfriendly.parse_timespan(time)
        except:
            return await ctx.send("Ay.. (Something went wrong.. I don't think the time is valid..)")

        if member == ctx.author:
            return await ctx.send("Ay!? (Timing out yourself!? Almost impossible!)")
        if member == self.client.user:
            return await ctx.send("Ay!? (Timing out **me**!? Almost impossible!)")

        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        await ctx.send(f"Ay! (Timed out {member.mention} for **{round(time)} Seconds**! Reasoning can be viewed in audit log!)")

    # noinspection SpellCheckingInspection
    @commands.command(name="de-timeout", aliases=['unmute'], usage='timeout <member> <time>')
    @commands.has_permissions(moderate_members=True)
    async def de_timeout(self, ctx, member: nextcord.Member, *, reason=None):
        """De-timeout members who have been timed out!"""

        if member == ctx.author:
            return await ctx.send("Ay!? (De-timing out yourself!? Almost impossible!)")
        if member == self.client.user:
            return await ctx.send("Ay!? (De-timing out **me**!? Almost impossible!)")

        await member.edit(timeout=None, reason=reason)
        await ctx.send(f"Ay! (De-timed out {member.mention}! Reasoning can be viewed in audit log!)")

    async def cog_command_error(self, ctx, error):

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"Ay!? (You don't have proper permission to use this!? Sorry I can't let you use this command.."
                                  f"I feel like you require `" + ", ".join(error.missing_permissions) + "`..?)")

        if isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f"Ay!? (**I** don't have proper permission to use this!? Sorry I can't let myself use this command.. "
                                  f"I feel like I require `" + ", ".join(error.missing_permissions) + "`..?)")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f'Ay!? (Who\'s that!?)')

        if isinstance(error, commands.ChannelNotFound):
            return await ctx.send("Ay.. (I can't seem to find that channel..)")

        await ctx.send(f"Ay.. (An error has occurred in my Management Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Management Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*[Ay! (**{ctx.guild.name}**)]({await ctx.channel.create_invite()})*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Management(client))
