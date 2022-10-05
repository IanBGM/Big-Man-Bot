import random

import nextcord
import sqlite3

import cooldowns
from nextcord.ext import commands

from External import Colors, Variables


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        activity = nextcord.Activity(type=nextcord.ActivityType.playing, name=f"Ay! (Hopefully I am of good help!)")
        await self.client.change_presence(activity=activity, status=nextcord.Status.dnd)

        # region CURRENCY_DB
        currDB = sqlite3.connect("curr.sqlite")
        currCursor = currDB.cursor()
        currCursor.execute('''CREATE TABLE IF NOT EXISTS curr (
            user_id INTEGER, wallet INTEGER, bank INTEGER, max_bank INTEGER
        )''')
        # noinspection SpellCheckingInspection
        currCursor.execute('''CREATE TABLE IF NOT EXISTS inv (
            user_id INTEGER,
            zapfish INTEGER,
            cm_amiibos INTEGER,
            pm_amiibos INTEGER,
            shooters INTEGER,
            rollers INTEGER,
            splatlings INTEGER,
            blasters INTEGER,
            brushes INTEGER,
            dualies INTEGER,
            chargers INTEGER,
            sloshers INTEGER,
            brellas INTEGER
        )''')
        currCursor.execute('''CREATE TABLE IF NOT EXISTS system (
            guild_id INTEGER, enabled BOOL
        )''')
        # ALTERING
        # noinspection SpellCheckingInspection
        # currCursor.execute('''ALTER TABLE inv
        #     ADD pm_amiibos INTEGER;
        # ''')
        currDB.commit()
        # endregion

        # region LEVEL_DB
        levelDB = sqlite3.connect("level.sqlite")
        levelCursor = levelDB.cursor()
        levelCursor.execute('''CREATE TABLE IF NOT EXISTS levels (
            guild_id INTEGER, user_id INTEGER, level INTEGER, xp INTEGER
        )''')
        levelCursor.execute('''CREATE TABLE IF NOT EXISTS system (
            guild_id INTEGER, enabled BOOL
        )''')
        levelDB.commit()
        # endregion

        # region MAIN_DB
        mainDB = sqlite3.connect("main.sqlite")
        mainCursor = mainDB.cursor()
        mainCursor.execute('''CREATE TABLE IF NOT EXISTS starboard (
            guild_id INTEGER, channel_id INTEGER, stars INTEGER
        )''')
        mainCursor.execute('''CREATE TABLE IF NOT EXISTS starSystem (
            guild_id INTEGER, enabled BOOL
        )''')
        mainDB.commit()
        # endregion

        print("Big Man is ready & online!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: nextcord.RawReactionActionEvent):
        emoji = payload.emoji
        guild = self.client.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if emoji.name == "⭐":

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
            enabled = cursor.fetchone()
            if enabled and not enabled[0]:
                return

            cursor.execute(f'SELECT stars, channel_id FROM starboard WHERE guild_id = {guild.id}')
            data = cursor.fetchone()

            if data:
                stars = data[0]
                channelData = data[1]

                for reaction in message.reactions:
                    if reaction.emoji == "⭐":
                        if reaction.count >= stars:
                            if message.content != "":
                                starEmbed = nextcord.Embed(title="Ay! (Starboard Update!)",
                                                           description=f"*Ay!* [(***Goto message!***)]({message.jump_url})\n\n*Ay* \n```(\"{message.content}\")```", color=Colors.dark_grey)
                            else:
                                starEmbed = nextcord.Embed(title="Ay! (Starboard Update!)", description=f"*Ay!* [(***Goto message!***)]({message.jump_url})", color=Colors.dark_grey)
                            # noinspection PyBroadException
                            try:
                                starEmbed.set_image(url=message.attachments[0].url)
                            except:
                                pass
                            starEmbed.set_footer(text=f'Ay! (Sent by {message.author.name + "#" + message.author.discriminator}!)')
                            await self.client.get_channel(channelData).send(embed=starEmbed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # region CURRENCY
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM curr WHERE user_id = {message.author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO curr (user_id, wallet, bank, max_bank) VALUES (?, ?, ?, ?)"
            val = (message.author.id, 500, 0, Variables.initial_bank_capacity)
            cursor.execute(sql, val)
        db.commit()

        cursor.execute(f'SELECT user_id FROM inv WHERE user_id = {message.author.id}')
        result = cursor.fetchone()
        if result is None:
            # noinspection SpellCheckingInspection
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (message.author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
        db.commit()

        cursor.close()
        db.close()
        # endregion

        # region LEVEL
        author = message.author
        guild = message.guild

        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()
        currDb = sqlite3.connect('curr.sqlite')
        currCursor = currDb.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return

        cursor.execute('SELECT xp FROM levels WHERE user_id = ? AND guild_id = ?', (author.id, guild.id))
        xp = cursor.fetchone()
        cursor.execute('SELECT level FROM levels WHERE user_id = ? AND guild_id = ?', (author.id, guild.id))
        level = cursor.fetchone()

        if not xp or not level:
            cursor.execute('INSERT INTO levels (guild_id, user_id, level, xp) VALUES (?, ?, ?, ?)', (guild.id, author.id, 1, 5))
            db.commit()

        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 5
            level = 1

        xp_max = level * 30

        if level < 5:
            xp += random.randint(0, 2)
            cursor.execute('UPDATE levels SET xp = ? WHERE user_id = ? AND guild_id = ?', (xp, author.id, guild.id))
        else:
            rand = random.randint(0, level // 4)
            if rand == 1:
                xp += random.randint(0, 2)
                cursor.execute('UPDATE levels SET xp = ? WHERE user_id = ? AND guild_id = ?', (xp, author.id, guild.id))

        if xp >= xp_max:
            level += 1

            # region LEVEL_UP_CURRENCY
            currCursor.execute(f"SELECT wallet FROM curr WHERE user_id = {author.id}")
            wallet = currCursor.fetchone()

            # noinspection PyBroadException
            try:
                wallet = wallet[0]
            except:
                wallet = 0

            sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
            val = wallet + 30, author.id
            currCursor.execute(sql, val)
            currDb.commit()
            currCursor.close()
            currDb.close()

            # endregion

            cursor.execute('UPDATE levels SET level = ? WHERE user_id = ? AND guild_id = ?', (level, author.id, guild.id))
            cursor.execute('UPDATE levels SET xp = ? WHERE user_id = ? AND guild_id = ?', (5, author.id, guild.id))
            await message.channel.send(f"Ay! (You've leveled up to **Level {level}**! You have also been rewarded **30 BMD**!)", mention_author=False, reference=message)
        db.commit()
        cursor.close()
        db.close()
        # endregion

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"Ay.. (I can't find that command in my code..)")
        if isinstance(error, sqlite3.OperationalError):
            return await ctx.send("Ay.. (Database is locked.. give me a moment..)")

    @commands.Cog.listener()
    async def on_application_command_error(self, interaction: nextcord.Interaction, error):
        error = getattr(error, "original", error)
        if isinstance(error, cooldowns.exceptions.CallableOnCooldown):
            return await interaction.send(f'Ay!? (This command needs to cooldown!? Try in {round(error.retry_after, 2)} seconds)', ephemeral=True)
        if isinstance(error, TypeError):
            return await interaction.send('Ay.. (An error has occurred recently..)', ephemeral=True)
        if isinstance(error, sqlite3.OperationalError):
            return await interaction.send("Ay.. (Database is locked.. give me a moment..)", ephemeral=True)
        if isinstance(error, nextcord.ApplicationCheckFailure):
            return await interaction.send("Ay!? (You/**I** don't have proper permission to use this!? Sorry I can't let you/myself use this command..)", ephemeral=True)
        if isinstance(error, ValueError):
            return await interaction.send('Ay.. (An error has occurred recently..)', ephemeral=True)

        await interaction.send(f"Ay.. (An error has occurred in my Slash Code.. I have sent the error out for assistance.)", ephemeral=True)

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Slash Code..)", timestamp=interaction.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{interaction.application_command.name}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*[Ay! (**{interaction.guild.name}**)]({await interaction.channel.create_invite()})*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Events(client))
