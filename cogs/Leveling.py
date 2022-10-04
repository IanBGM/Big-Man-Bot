import asyncio
import random
import sqlite3

import cooldowns
import nextcord
from easy_pil import Editor, load_image_async
from nextcord.ext import commands

from External import Fonts, Colors, start_blitz, Emojis
from Market import start_blitz_pm_amiibos


class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['rank', 'lvl'], usage='level [member]')
    async def level(self, ctx, member: nextcord.Member = None):
        """View levels!"""
        if member is None:
            member = ctx.author

        guild = ctx.guild

        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Leveling is currently disabled for this server..)')

        cursor.execute('SELECT xp FROM levels WHERE user_id = ? AND guild_id = ?', (member.id, guild.id))
        xp = cursor.fetchone()
        cursor.execute('SELECT level FROM levels WHERE user_id = ? AND guild_id = ?', (member.id, guild.id))
        level = cursor.fetchone()

        if not xp or not level:
            cursor.execute('INSERT INTO levels (guild_id, user_id, level, xp) VALUES (?, ?, ?, ?)', (guild.id, member.id, 1, 5))
            db.commit()

        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 5
            level = 1

        xp_max = level * 30

        level_data = {
            "name": member.name + "#" + member.discriminator,
            "xp": xp,
            "level": level,
            "next_lvl_xp": xp_max  # ,
            # "percent": xp
        }

        profile_img = await load_image_async(member.avatar.url)

        background = Editor("assets/big_man.png").resize((800, 380)).blur(amount=3).rounded_corners(radius=20)
        profile = Editor(profile_img).resize((180, 180)).circle_image()

        # PREVIOUS VALUES WITH BAR: WHITE_CIRCLE = (40, 40) | RED_CIRCLE = (35, 35)
        background.ellipse((40, 90), width=200, height=200, fill="white", outline="white", stroke_width=10)
        background.ellipse((35, 85), width=210, height=210, outline="#fc585f", stroke_width=10)

        # background.rectangle((60, 280), width=650, height=40, fill="white", radius=20, stroke_width=30)
        # background.bar((60, 280), max_width=650, height=40, percentage=level_data['percent'], fill="#fc585f", radius=20)

        background.text((280, 130), "Ay! (" + level_data['name'] + ")", font=Fonts.set_splatfont(35), color="white")
        background.text((280, 200), f"Ay (Level : {level_data['level']})", font=Fonts.set_splatfont2(30), color="white")
        background.text((280, 250), f"Ay (XP : {level_data['xp']} / {level_data['next_lvl_xp']})", font=Fonts.set_splatfont2(30), color="white")
        background.text((160, 340), f"Ay! (Every level-up rewards 30 BMD as well!)", font=Fonts.set_splatfont2(25), color="white")

        background.paste(profile, (50, 100))

        file = nextcord.File(fp=background.image_bytes, filename=f'BMLS_rank_{member.name}.png')
        await ctx.send(file=file)

        cursor.close()
        db.close()

    @commands.command(usage='gain')
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def gain(self, ctx):
        """Gain some free XP every hour!"""
        db = sqlite3.connect("level.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Leveling is currently disabled for this server..)')

        xp_earned = random.randint(1, 100)

        cursor.execute(f"SELECT xp FROM levels WHERE user_id = {ctx.author.id}")
        xp = cursor.fetchone()

        # noinspection PyBroadException
        try:
            xp = xp[0]
        except:
            xp = 0

        sql = "UPDATE levels SET xp = ? WHERE user_id = ?"
        val = xp + int(xp_earned), ctx.author.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! (You gained **{xp_earned} XP**! Come back again in another hour!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @commands.command(aliases=['exp', 'blitz-battle', 'blitz-war'], usage='blitz')
    @commands.cooldown(1, 180, commands.BucketType.user)
    async def blitz(self, ctx):
        """Play Experience Blitz for XP!"""

        await ctx.send("Ay? (Are you sure you want to play Experience Blitz? A **300 BMD** fee is required to play.)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            return await ctx.send("Ay! (No Experience Blitz! Got it!)")

        db = sqlite3.connect("level.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Leveling is currently disabled for this server..)')

        cursor.execute(f"SELECT xp FROM levels WHERE user_id = {ctx.author.id}")
        xp = cursor.fetchone()

        currDb = sqlite3.connect("curr.sqlite")
        currCursor = currDb.cursor()
        currCursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = currCursor.fetchone()
        currCursor.execute(f"SELECT pm_amiibos FROM inv WHERE user_id = {ctx.author.id}")
        pm_amiibos = currCursor.fetchone()

        # noinspection PyBroadException
        try:
            xp = xp[0]
            wallet = wallet[0]
            pm_amiibos = pm_amiibos[0]
        except:
            xp = xp
            wallet = wallet
            pm_amiibos = pm_amiibos

        if wallet < 300:
            return await ctx.send("Ay.. (300 BMD is required to play..)")

        if pm_amiibos > 0:
            await start_blitz_pm_amiibos(ctx)
        else:
            await start_blitz(ctx)

        user_chance = random.randint(0, 100)
        opponent_chance = random.randint(0, 100)

        user_final = 0
        opponent_final = 0

        if pm_amiibos > 0:
            user_chance = 100
            opponent_chance = 0

        if user_chance == 0:
            user_final = "KNOCKOUT"
            opponent_final = "MAX"
        elif opponent_chance == 0:
            opponent_final = "KNOCKOUT"
            user_final = "MAX"
        elif user_chance and opponent_chance != 0:
            user_final = 100 * (user_chance / (user_chance + opponent_chance))
            opponent_final = 100 * (opponent_chance / (user_chance + opponent_chance))

        if user_chance > opponent_chance:
            xp_won = random.randint(50, 120)
            if pm_amiibos > 0:
                currCursor.execute("UPDATE inv SET pm_amiibos = ? WHERE user_id = ?", (pm_amiibos - 1, ctx.author.id))
            currCursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - 300, ctx.author.id))
            cursor.execute("UPDATE levels SET xp = ? WHERE user_id = ?", (xp + xp_won, ctx.author.id))
            currDb.commit()
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the Experience Blitz Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{xp_won} XP** you won! Use it wisely!)", timestamp=ctx.message.created_at)
            if opponent_final == "KNOCKOUT":
                winEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{user_final}*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            elif user_final == "KNOCKOUT":
                winEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{user_final}*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            else:
                winEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{round(user_final)} XP*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{round(opponent_final)} XP*")

            await ctx.reply(embed=winEmbed, mention_author=False)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

        elif user_chance < opponent_chance:
            xp_won = random.randint(1, 50)
            currCursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - 300, ctx.author.id))
            cursor.execute("UPDATE levels SET xp = ? WHERE user_id = ?", (xp + xp_won, ctx.author.id))
            currDb.commit()
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the Experience Blitz Battle..)",
                                       description=f"Ay.. (Better luck next time.. you still won **{xp_won} XP**.)", timestamp=ctx.message.created_at)
            if opponent_final == "KNOCKOUT":
                lostEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{user_final} XP*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            elif user_final == "KNOCKOUT":
                lostEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{user_final}*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final} XP*")
            else:
                lostEmbed.add_field(name=f"{ctx.author.name} Count", value=f"*{round(user_final)}*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{round(opponent_final)}*")

            await ctx.reply(embed=lostEmbed, mention_author=False)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

        else:
            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the Experience Blitz Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=ctx.message.created_at)
            await ctx.reply(embed=tieEmbed, mention_author=False)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

    @commands.command(usage='share <member> [amount]')
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def share(self, ctx, member: nextcord.Member, amount: int = 5):
        """Share your XP with others!"""
        author = ctx.author
        guild = ctx.guild

        db = sqlite3.connect("level.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Leveling is currently disabled for this server..)')

        cursor.execute(f'SELECT xp FROM levels WHERE user_id = {author.id}')
        xp = cursor.fetchone()
        cursor.execute(f'SELECT level FROM levels WHERE user_id = {author.id}')
        level = cursor.fetchone()

        cursor.execute(f'SELECT xp FROM levels WHERE user_id = {member.id}')
        mem_xp = cursor.fetchone()
        cursor.execute(f'SELECT level FROM levels WHERE user_id = {member.id}')
        mem_level = cursor.fetchone()

        # noinspection PyBroadException
        try:
            xp = xp[0]
            mem_xp = mem_xp[0]
            level = level[0]
            mem_level = mem_level[0]
        except:
            xp = xp
            mem_xp = mem_xp
            level = level
            mem_level = mem_level

        if level < 5:
            return await ctx.send("Ay.. (Sorry, you're not at least **Level 5** to be sharing XP..)")

        if mem_level < 5:
            return await ctx.send("Ay.. (Sorry, their not at least **Level 5** to be shared XP..)")

        if xp < amount:
            return await ctx.send("Ay!? (You don't have enough XP to share that much!?")

        if amount < 5:
            return await ctx.send("Ay.. (Sorry, you can't share less then 5 XP..)")

        cursor.execute('UPDATE levels SET xp = ? WHERE user_id = ?', (xp - amount, author.id))
        cursor.execute('UPDATE levels SET xp = ? WHERE user_id = ?', (mem_xp + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You have shared **{amount} XP** with {member.mention}!)")
        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @commands.command(aliases=['all-levels', 'levels'], usage='levelboard')
    async def levelboard(self, ctx: commands.Context):
        """Shows all the levels ranked!"""

        guild = ctx.guild

        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Leveling is currently disabled for this server..)')

        cursor.execute(f'SELECT user_id, level, xp FROM levels WHERE guild_id = {guild.id} ORDER BY level DESC, xp DESC LIMIT 10')
        data = cursor.fetchall()

        if data:
            levelEmbed = nextcord.Embed(title='Ay! (Level System Leaderboard!)', color=Colors.dark_grey, timestamp=ctx.message.created_at)
            count = 0

            for table in data:
                count += 1
                user = ctx.guild.get_member(table[0])

                levelEmbed.add_field(name=f'Ay! ({count}. {user.name + "#" + user.discriminator})',
                                     value=f"*Ay* (**Level** : *{table[1]}* | **XP** : *{table[2]} / {table[1] * 30}*)", inline=False)

            levelEmbed.set_footer(text=f"Ay! (Top 10 Results!)")
            return await ctx.send(embed=levelEmbed)
        return await ctx.send("Ay.. (I can't seem to find anyone stored in my database for the leveling leaderboard..)")

    async def cog_command_error(self, ctx, error):

        if isinstance(error, sqlite3.OperationalError):
            return await ctx.send("Ay.. (Database is locked.. give me a moment..)")

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'Ay!? (This command needs to cooldown!? Try in {round(error.retry_after, 2)} seconds)')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f'Ay!? (Who\'s that!?)')

        await ctx.send(f"Ay.. (An error has occurred in my Leveling Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Leveling Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*[Ay! (**{ctx.guild.name}**)]({await ctx.channel.create_invite()})*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Leveling(client))
