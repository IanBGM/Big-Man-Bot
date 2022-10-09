import asyncio
import random
import sqlite3

import nextcord
from nextcord.ext import commands

from External import Colors, Emojis, set_inv, set_shop, gift_check, sell_check, start_turf, start_turf_extreme, start_cheat
from Interactions import Selections, Paginations
from Market import start_turf_cm_amiibos, start_turf_extreme_cm_amiibos


class Economy(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(aliases=['currency', 'bal', 'money'], usage="balance [member]")
    async def balance(self, ctx, member: nextcord.Member = None):
        """Check your balance!"""
        if member is None:
            member = ctx.author

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT wallet, bank, max_bank FROM curr WHERE user_id = {member.id} ")
        bal = cursor.fetchone()
        # noinspection PyBroadException
        try:
            wallet = bal[0]
            bank = bal[1]
            max_bank = bal[2]
        except:
            wallet = 0
            bank = 0
            max_bank = 0

        if member.bot:
            return await ctx.send("Ay!? (That's a bot!?)")

        balanceEmbed = nextcord.Embed(colour=Colors.dark_grey, title=f"Ay! ({member.name} Balance!)", timestamp=ctx.message.created_at)

        balanceEmbed.add_field(name='Ay (Wallet)', value=f"{Emojis.judd} *Ay* (**{wallet} BMD**)")
        balanceEmbed.add_field(name='Ay (Bank)', value=f"*Ay* (**{bank} / {max_bank} BMD**) {Emojis.lil_judd}")
        balanceEmbed.add_field(name='Ay (BMD Flow)', value=f"{Emojis.judd} *Ay* (**{wallet + bank} BMD**) {Emojis.lil_judd}")

        balanceEmbed.set_footer(text="Ay! (BMD = Big Man Dollars!)")

        await ctx.send(embed=balanceEmbed)

    @commands.command(aliases=['place', 'dep'], usage="deposit [amount]")
    async def deposit(self, ctx, amount: int = 50):
        """Deposit your BMD into the Big Man Bank! (0 for All)"""

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT * FROM curr WHERE user_id = {ctx.author.id}")
        data = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = data[1]
            bank = data[2]
            max_bank = data[3]
        except:
            return await ctx.send("Ay.. (Something with wrong..)")

        if wallet is None or bank is None or max_bank is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        if amount == 0 and wallet + bank > max_bank:
            return await ctx.send("Ay.. (That amount goes over the Bank Capacity, you cannot deposit anymore BMD..)")

        if amount != 0 and amount < 1:
            return await ctx.send("Ay.. (Please deposit at least **1 BMD**..)")
        if wallet < amount:
            return await ctx.send("Ay.. (Not enough BMD to deposit..)")
        elif amount + bank > max_bank:
            return await ctx.send("Ay.. (That amount goes over the Bank Capacity, you cannot deposit anymore BMD..)")
        else:
            if amount == 0 and not wallet + bank > max_bank:
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank + wallet, ctx.author.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - wallet, ctx.author.id))
                await ctx.send(f"Ay! (You have placed **all your BMD** in the Big Man Bank!)")
            else:
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank + amount, ctx.author.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
                await ctx.send(f"Ay! (You have placed **{amount} BMD** in the Big Man Bank!)")

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['draw', 'take'], usage="withdraw [amount]")
    async def withdraw(self, ctx, amount: int = 50):
        """Withdraw your BMD from the Big Man Bank! (0 for All)"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT * FROM curr WHERE user_id = {ctx.author.id}")
        data = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = data[1]
            bank = data[2]
        except:
            return await ctx.send("Ay.. (Something with wrong..)")

        if wallet is None or bank is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        if amount != 0 and amount < 1:
            return await ctx.send("Ay.. (Please withdraw at least **1 BMD**..)")

        if bank < amount:
            return await ctx.send("Ay.. (Not enough BMD to withdraw)")
        else:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bank, ctx.author.id))
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank - bank, ctx.author.id))
                await ctx.send(f"Ay! (You have took **all your BMD** from the Big Man Bank!)")
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank - amount, ctx.author.id))
                await ctx.send(f"Ay! (You have took **{amount} BMD** from the Big Man Bank!)")

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['work', 'earn'], usage="job")
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def job(self, ctx):
        """Get a job! Make some BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        bmd_earned = random.randint(1, 100)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
        except:
            wallet = 0

        if wallet is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
        val = wallet + int(bmd_earned), ctx.author.id
        cursor.execute(sql, val)

        await ctx.reply(f"Ay! (You earned **{bmd_earned} BMD**! Spend it wisely!)", mention_author=False)

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['give'], usage="loan <member> [amount]")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def loan(self, ctx, member: nextcord.Member, amount: int = 100):
        """Loan BMD to others!"""
        member = member
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {member.id}")
        memWallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
            memWallet = memWallet[0]
        except:
            wallet = wallet
            memWallet = memWallet

        if member.bot:
            return await ctx.send("Ay!? (That's a bot!?)")

        if memWallet is None:
            return await ctx.send("Ay.. (They don't have any economy data..)")

        if member == ctx.author:
            return await ctx.send("Ay!? (You can\'t give BMD to yourself!? Almost impossible!)")

        if wallet < amount:
            return await ctx.send("Ay.. (Not enough BMD to send to others..)")

        if amount < 100:
            return await ctx.send("Ay.. (Sorry, 100 or above to send BMD to others..)")

        if amount == 0:
            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - wallet, ctx.author.id))
            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + wallet, member.id))
        else:
            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + amount, member.id))
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f"Ay! (You have sent **{amount} BMD** to {member.mention})")

    # noinspection SpellCheckingInspection
    @commands.command(aliases=['turf-war', 'war'], usage="turf [amount]")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def turf(self, ctx, amount: int = 85):
        """Play Turf War for BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT * FROM inv WHERE user_id = {ctx.author.id}")
        item = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
            cm_amiibos = item[2]
            shooters = item[4]
            rollers = item[5]
            splatlings = item[6]
            blasters = item[7]
            brushes = item[8]
            dualies = item[9]
            chargers = item[10]
            sloshers = item[11]
            brellas = item[12]
        except:
            wallet = wallet
            cm_amiibos = item
            shooters = item
            rollers = item
            splatlings = item
            blasters = item
            brushes = item
            dualies = item
            chargers = item
            sloshers = item
            brellas = item

        if wallet is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        if amount != 0 and amount < 85:
            return await ctx.reply("Ay.. (Sorry, 85 or above to play turf..)", mention_author=False)

        if wallet < amount:
            return await ctx.reply("Ay.. (You don't have enough BMD to put in that much BMD..)", mention_author=False)

        if cm_amiibos > 0:
            await start_turf_cm_amiibos(ctx)
        else:
            await start_turf(ctx)

        user_chance = random.randint(1, 100)
        opponent_chance = random.randint(1, 100)

        # region WEAPON CHECKS

        if shooters > 0:
            user_chance += 5
        if rollers > 0:
            user_chance += 8
        if splatlings > 0:
            user_chance += 10
        if blasters > 0:
            user_chance += 12
        if brushes > 0:
            user_chance += 14
        if dualies > 0:
            user_chance += 17
        if chargers > 0:
            user_chance += 20
        if sloshers > 0:
            user_chance += 22
        if brellas > 0:
            user_chance += 25

        # endregion

        user_final = 100 * (user_chance / (user_chance + opponent_chance))
        opponent_final = 100 * (opponent_chance / (user_chance + opponent_chance))

        if cm_amiibos > 0:
            user_final = 100
            opponent_final = 0
            user_chance = 50
            opponent_chance = 0

        if user_chance > opponent_chance:
            percent = random.randint(125, 185)

            if amount == 0:
                bmd_won = int(wallet * percent / 100)
            else:
                bmd_won = int(amount * percent / 100)

            # region WIN_CHECKS

            if cm_amiibos > 0:
                cursor.execute("UPDATE inv SET cm_amiibos = ? WHERE user_id = ?", (cm_amiibos - 1, ctx.author.id))
            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bmd_won, ctx.author.id))
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the Turf Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{bmd_won} BMD** you won! Use it wisely!)", timestamp=ctx.message.created_at)
            winEmbed.add_field(name=f"{ctx.author.name} Percentage", value=f"*{round(user_final, 1)}%*")
            winEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await ctx.reply(embed=winEmbed, mention_author=False)
            cursor.close()
            db.close()

        elif user_chance < opponent_chance:
            percent = random.randint(85, 145)
            if amount == 0:
                bmd_lost = int(wallet * percent / 100)
            else:
                bmd_lost = int(amount * percent / 100)

            # region LOSE_CHECKS

            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - bmd_lost, ctx.author.id))
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the Turf Battle..)",
                                       description=f"Ay.. (Better luck next time.. you lost **{bmd_lost} BMD**.)", timestamp=ctx.message.created_at)
            lostEmbed.add_field(name=f"{ctx.author.name} Percentage", value=f"*{round(user_final, 1)}%*")
            lostEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await ctx.reply(embed=lostEmbed, mention_author=False)
            cursor.close()
            db.close()

        else:

            # region TIE_CHECKS

            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

            # endregion

            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the Turf Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=ctx.message.created_at)
            await ctx.reply(embed=tieEmbed, mention_author=False)
            cursor.close()
            db.close()

    @commands.command(usage='cheat <member> [amount]')
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def cheat(self, ctx, member: nextcord.Member, amount: int = 500):
        """Cheat others for BMD?"""
        member = member
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {member.id}")
        memWallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
            memWallet = memWallet[0]
        except:
            wallet = wallet
            memWallet = memWallet

        if member.bot:
            return await ctx.send("Ay!? (That's a bot!?)")

        if memWallet is None:
            return await ctx.send("Ay.. (They don't have any economy data..)")

        if wallet is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        if member == ctx.author:
            return await ctx.send("Ay!? (Cheat.. yourself!?)")

        if memWallet < amount:
            return await ctx.send("Ay.. (They don't have enough BMD for you to partake in this procedure..)")

        if amount != 0 and amount < 500:
            return await ctx.send("Ay.. (Sorry, 500 or above to cheat BMD from others..)")

        await start_cheat(ctx, member)

        user_chance = random.randint(1, 150)
        member_chance = random.randint(1, 150)

        if user_chance > member_chance:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + memWallet, ctx.author.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet - memWallet, member.id))
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + amount, ctx.author.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet - amount, member.id))
            db.commit()

            if amount == 0:
                takeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f":question: Ay..? (You cheated them successfully..?) :question:",
                                           description=f"Ay? (Enjoy the **{memWallet} BMD** you took? *Dials 911-SP3*)", timestamp=ctx.message.created_at)
            else:
                takeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f":question: Ay..? (You cheated them successfully..?) :question:",
                                           description=f"Ay? (Enjoy the **{amount} BMD** you took? *Dials 911-SP3*)", timestamp=ctx.message.created_at)

            await ctx.reply(embed=takeEmbed, mention_author=False)
            cursor.close()
            db.close()

        elif user_chance < member_chance:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + memWallet, member.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - memWallet, ctx.author.id))
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + amount, member.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, ctx.author.id))
            db.commit()

            if amount == 0:
                caughtEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay..? (You got caught..?)",
                                             description=f"Ay.. (See you later.. you were fined **{memWallet} BMD**. {member.name} has claimed this..)", timestamp=ctx.message.created_at)
            else:
                caughtEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay..? (You got caught..?)",
                                             description=f"Ay.. (See you later.. you were fined **{amount} BMD**. {member.name} has claimed this..)", timestamp=ctx.message.created_at)

            await ctx.reply(embed=caughtEmbed, mention_author=False)
            cursor.close()
            db.close()

        else:
            homeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (You went back home!?)",
                                       description=f"Ay!? (You went back home and decided not to cheat someone!?)", timestamp=ctx.message.created_at)
            await ctx.reply(embed=homeEmbed, mention_author=False)
            cursor.close()
            db.close()

    # noinspection SpellCheckingInspection
    @commands.command(name='extreme-turf', aliases=['extreme-turf-war', 'extreme-war'], usage='extreme-turf [amount]')
    @commands.cooldown(1, 90, commands.BucketType.user)
    async def extreme_turf(self, ctx, amount: int = 135):
        """Play Extreme Turf War for BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT * FROM inv WHERE user_id = {ctx.author.id}")
        item = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
            cm_amiibos = item[2]
            shooters = item[4]
            rollers = item[5]
            splatlings = item[6]
            blasters = item[7]
            brushes = item[8]
            dualies = item[9]
            chargers = item[10]
            sloshers = item[11]
            brellas = item[12]
        except:
            wallet = wallet
            cm_amiibos = item
            shooters = item
            rollers = item
            splatlings = item
            blasters = item
            brushes = item
            dualies = item
            chargers = item
            sloshers = item
            brellas = item

        if wallet is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        if amount != 0 and amount < 135:
            return await ctx.reply("Ay.. (Sorry, 135 or above to play extreme turf..)", mention_author=False)

        if wallet < amount:
            return await ctx.reply("Ay.. (You don't have enough BMD to put in that much BMD..)", mention_author=False)

        if cm_amiibos > 0:
            await start_turf_extreme_cm_amiibos(ctx)
        else:
            await start_turf_extreme(ctx)

        user_chance = random.randint(50, 200)
        opponent_chance = random.randint(100, 200)

        # region WEAPON CHECKS

        if shooters > 0:
            user_chance += 5
        if rollers > 0:
            user_chance += 8
        if splatlings > 0:
            user_chance += 10
        if blasters > 0:
            user_chance += 12
        if brushes > 0:
            user_chance += 14
        if dualies > 0:
            user_chance += 17
        if chargers > 0:
            user_chance += 20
        if sloshers > 0:
            user_chance += 22
        if brellas > 0:
            user_chance += 25

        # endregion

        user_final = 100 * (user_chance / (user_chance + opponent_chance))
        opponent_final = 100 * (opponent_chance / (user_chance + opponent_chance))

        if cm_amiibos > 0:
            user_final = 100
            opponent_final = 0
            user_chance = 50
            opponent_chance = 0

        if user_chance > opponent_chance:
            percent = random.randint(200, 225)
            if amount == 0:
                bmd_won = int(wallet * percent / 100)
            else:
                bmd_won = int(amount * percent / 100)

                # region WIN_CHECKS

                if cm_amiibos > 0:
                    cursor.execute("UPDATE inv SET cm_amiibos = ? WHERE user_id = ?", (cm_amiibos - 1, ctx.author.id))
                if shooters > 0:
                    cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
                if rollers > 0:
                    cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
                if splatlings > 0:
                    cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
                if blasters > 0:
                    cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
                if brushes > 0:
                    cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
                if dualies > 0:
                    cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
                if chargers > 0:
                    cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
                if sloshers > 0:
                    cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
                if brellas > 0:
                    cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

                # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bmd_won, ctx.author.id))
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the EXTREME Turf Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{bmd_won} BMD** you won! Use it wisely!)", timestamp=ctx.message.created_at)
            winEmbed.add_field(name=f"{ctx.author.name} Percentage", value=f"*{round(user_final, 1)}%*")
            winEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await ctx.reply(embed=winEmbed, mention_author=False)
            cursor.close()
            db.close()

        elif user_chance < opponent_chance:
            percent = random.randint(185, 205)
            if amount == 0:
                bmd_lost = int(wallet * percent / 100)
            else:
                bmd_lost = int(amount * percent / 100)

                # region LOSE_CHECKS

                if shooters > 0:
                    cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
                if rollers > 0:
                    cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
                if splatlings > 0:
                    cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
                if blasters > 0:
                    cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
                if brushes > 0:
                    cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
                if dualies > 0:
                    cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
                if chargers > 0:
                    cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
                if sloshers > 0:
                    cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
                if brellas > 0:
                    cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

                # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - bmd_lost, ctx.author.id))
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the EXTREME Turf Battle..)",
                                       description=f"Ay.. (Better luck next time.. you lost **{bmd_lost} BMD**.)", timestamp=ctx.message.created_at)
            lostEmbed.add_field(name=f"{ctx.author.name} Percentage", value=f"*{round(user_final, 1)}%*")
            lostEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await ctx.reply(embed=lostEmbed, mention_author=False)
            cursor.close()
            db.close()

        else:

            # region TIE_CHECKS

            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, ctx.author.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, ctx.author.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, ctx.author.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, ctx.author.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, ctx.author.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, ctx.author.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, ctx.author.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, ctx.author.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, ctx.author.id))

            # endregion

            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the EXTREME Turf Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=ctx.message.created_at)
            await ctx.reply(embed=tieEmbed, mention_author=False)
            cursor.close()
            db.close()

    @commands.command(aliases=['inv', 'backpack', 'stuff'], usage='inventory [member]')
    async def inventory(self, ctx, member: nextcord.Member = None):
        """View inventories!"""

        await set_inv(member, ctx.author, ctx.message.created_at, ctx)

    @commands.command(aliases=['shop', 'store', 'outlet'], usage='market')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def market(self, ctx):
        """View the Marketplace where you can spend BMD!"""

        db = sqlite3.connect('curr.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        data = set_shop(ctx.message.created_at)
        pages = Paginations.GlobalPageSource.GlobalButtonMenu(
            source=Paginations.GlobalPageSource(data),
        )
        await pages.start(ctx)
        await ctx.send(" ", view=Selections.MarketSelection.ShopDropdown(self.client))
        # await paginate(self.client, ctx, ctx.author, set_shop(ctx.message.created_at), Selections.MarketSelection.ShopDropdown(self.client), True)
        # await ctx.send(view=Selections.MarketSelection.ShopDropdown(self.client))
        cursor.close()
        db.close()

    @commands.command(usage='gift <member> <item_id> [amount]')
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def gift(self, ctx, member: nextcord.Member, item_id: str, amount: int = 1):
        """Gift your items to others!"""

        if amount < 1:
            return await ctx.send("Ay.. (Please gift **1** or more of the item..)")

        await gift_check(item_id, ctx, ctx.author, member, amount, self.client)

    @commands.command(usage='sell <item_id> [amount]')
    @commands.cooldown(1, 8, commands.BucketType.user)
    async def sell(self, ctx, item_id: str, amount: int = 1):
        """Sell your items for BMD!"""

        if amount < 1:
            return await ctx.send("Ay.. (Please sell **1** or more of the item..)")

        await sell_check(item_id, ctx, ctx.author, amount)

    # noinspection SpellCheckingInspection
    # @commands.command(aliases=['all-bmd', 'balances'], usage='bmdboard')
    # async def bmdboard(self, ctx: commands.Context):
    #     """Shows all the balances ranked!"""
    #
    #     db = sqlite3.connect('curr.sqlite')
    #     cursor = db.cursor()
    #
    #     cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
    #     enabled = cursor.fetchone()
    #     if enabled and not enabled[0]:
    #         return await ctx.send('Ay.. (Economy is currently disabled for this server..)')
    #
    #     cursor.execute(f'SELECT user_id, wallet, bank FROM curr ORDER BY (wallet+bank) DESC LIMIT 10')
    #     data = cursor.fetchall()
    #
    #     if data:
    #         bmdEmbed = nextcord.Embed(title='Ay! (Global Economy System Leaderboard!)', color=Colors.dark_grey, timestamp=ctx.message.created_at)
    #         count = 0
    #
    #         for table in data:
    #             count += 1
    #             user = ctx.guild.get_member(table[0])
    #
    #             bmdEmbed.add_field(name=f'Ay! ({count}. {user.name + "#" + user.discriminator})',
    #                                value=f"*Ay* (**BMD Flow** : *{table[1] + table[2]}*)", inline=False)
    #
    #         bmdEmbed.set_footer(text=f"Ay! (Top 10 Results!)")
    #         return await ctx.send(embed=bmdEmbed)
    #     return await ctx.send("Ay.. (I can't seem to find anyone stored in my database for the economy leaderboard..)")

    # noinspection SpellCheckingInspection
    @commands.command(usage='reset')
    @commands.cooldown(1, 1800, commands.BucketType.user)
    async def reset(self, ctx):
        """Reset all your economy data!"""

        await ctx.send(f"Ay? ({ctx.author.mention} Are you sure you want to reset **all your economy data**?)")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            await ctx.send("Ay! (Operation Cancelled!)")
            return

        await ctx.send(f"Ay? (Double confirmation, are you **absolutely** sure?)")

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            await ctx.send("Ay! (Operation Cancelled!)")
            return

        db = sqlite3.connect('curr.sqlite')
        cursor = db.cursor()

        cursor.execute("UPDATE curr SET wallet = ?, bank = ?, max_bank = ? WHERE user_id = ?", (500, 0, 5000, ctx.author.id))
        cursor.execute(f'''
            UPDATE inv SET zapfish = ?, cm_amiibos = ?, pm_amiibos = ? WHERE user_id = ?
        ''', (0, 0, 0, ctx.author.id))
        db.commit()
        await ctx.send("Ay! (Economy Data has been reset! (System being disabled does not apply to reset))")
        cursor.close()
        db.close()

    @commands.command(aliases=['daily'], usage='mail')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def mail(self, ctx):
        """Get your daily mail!"""

        author = ctx.author

        db = sqlite3.connect('curr.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

        cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
        wallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
        except:
            wallet = wallet

        if wallet is None:
            return await ctx.send("Ay.. (You don't have any economy data..)")

        daily_mail = random.randint(500, 1000)
        cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + daily_mail, author.id))
        await ctx.send(f"Ay! (You have cleaned out your mail! You were also mailed **{daily_mail} BMD**!)")
        db.commit()
        cursor.close()
        db.close()

    async def cog_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'Ay!? (This command needs to cooldown!? Try in {round(error.retry_after, 2)} seconds)')

        if isinstance(error, commands.MemberNotFound):
            return await ctx.send(f'Ay!? (Who\'s that!?)')

        await ctx.send(f"Ay.. (An error has occurred in my Economy Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Economy Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*Ay! (**{ctx.guild.name}**)*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Economy(client))
