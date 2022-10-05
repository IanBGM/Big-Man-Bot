import asyncio
import datetime
import random
import re
import sqlite3
from urllib import request, parse

import humanfriendly
import nextcord
import cooldowns
import requests
from easy_pil import load_image_async, Editor
from googletrans import Translator
from nextcord.ext import commands, application_checks

import External
from External import Variables, Colors, Emojis, Fonts, set_inv, gift_check, sell_check, start_turf, start_cheat, start_turf_extreme, start_blitz
from Interactions import Modals
from Market import start_turf_extreme_cm_amiibos, start_turf_cm_amiibos, start_blitz_pm_amiibos


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    # region COMMON

    @nextcord.slash_command(name="assistance", guild_ids=Variables.guild_ids)
    async def assistance_slash(self, interaction: nextcord.Interaction):
        """Help on all my command names!"""
        assistanceEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Assistance!)",
                                         description="*Ay? (Need some help with that?)*", timestamp=interaction.created_at)

        assistanceEmbed.add_field(name="Ay (Common)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Common"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Management)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Management"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Entertainment)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Entertainment"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Economy)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Economy"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Leveling)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Leveling"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Holder)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Holder"))) + "\n```")

        await interaction.user.send(embed=assistanceEmbed)
        await interaction.send("Ay! (I messaged you my commands!)")

    @nextcord.slash_command(name="command", guild_ids=Variables.guild_ids)
    async def command_slash(self, interaction: nextcord.Interaction, name):
        """Get further assistance on commands!"""
        command = self.client.get_command(name)

        if command is None:
            return await interaction.send("Ay.. (I can't find that command in my code..)")

        commandEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Command Assistance!)", timestamp=interaction.created_at)
        commandEmbed.add_field(
            name=f"Ay ({command.name} Command)",
            value=f"*Ay!* ```\n({command.help})\n```\n*Ay!* ```\n({command.usage})\n```\n*Ay!* ```\n({', '.join(command.aliases)})\n```"
        )

        await interaction.send(embed=commandEmbed)

    @nextcord.slash_command(name="request", guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def request_slash(self, interaction: nextcord.Interaction):
        """Send feature request for me!"""
        await interaction.response.send_modal(Modals.RequestModal(self.client))

    @nextcord.slash_command(name="bug", guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def bug_slash(self, interaction: nextcord.Interaction):
        """Send bug report for fixing!"""
        await interaction.response.send_modal(Modals.BugModal(self.client))

    # noinspection PyUnusedLocal
    @request_slash.error
    async def request_error(self, ctx, error):
        if isinstance(error, cooldowns.CallableOnCooldown):
            return

    # noinspection PyUnusedLocal
    @bug_slash.error
    async def bug_error(self, ctx, error):
        if isinstance(error, cooldowns.CallableOnCooldown):
            return

    @nextcord.slash_command(name='server-info', guild_ids=Variables.guild_ids)
    async def server_info_slash(self, interaction: nextcord.Interaction):
        """Sends info on the current server!"""
        guild = interaction.guild

        server_data = {
            "Name": f"\"{guild.name}\"",
            "Owner": f"\"{guild.owner.name + '#' + guild.owner.discriminator}\"",
            "All Channels": f"{len(guild.text_channels) + len(guild.voice_channels)}",
            "Members": f"{guild.member_count}",
            "Bots": f"{len(guild.bots)}",
            "Custom Emojis": f"{len(guild.emojis)}",
            "Verification Level": f"{guild.verification_level}",
            "Creation Time": f"{guild.created_at.strftime('%b %d, %Y, %T')}"
        }

        serverEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=interaction.created_at,
                                     description=f"Ay ```\n"
                                                 f"(\nName : {server_data['Name']}\n\n"
                                                 f"Owner : {server_data['Owner']}\n\n"
                                                 f"All Channels : {server_data['All Channels']}\n\n"
                                                 f"Members : {server_data['Members']}\n\n"
                                                 f"Bots : {server_data['Bots']}\n\n"
                                                 f"Custom Emojis : {server_data['Custom Emojis']}\n\n"
                                                 f"Verification Level : {server_data['Verification Level']}\n\n"
                                                 f"Creation Time : {server_data['Creation Time']}\n)\n\n"
                                                 f"\n```")

        # for [name, value] in server_data.items():
        #     serverEmbed.add_field(name=f'Ay ({name})', value=f"*Ay ({value})*")

        try:
            serverEmbed.set_thumbnail(url=guild.icon.url)
        except AttributeError:
            pass
        serverEmbed.set_author(name=f"Ay! ({server_data['Name']} Information!)")
        serverEmbed.set_footer(text=f"Ay! (ID: {guild.id}!)")
        await interaction.send(embed=serverEmbed)

    @nextcord.slash_command(name='user-info', guild_ids=Variables.guild_ids)
    async def user_info_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        """Sends info on the user!"""
        if member is None:
            member = interaction.user

        # noinspection PyBroadException
        try:
            user_data = {
                "Name": f"\"{member.name}\"",
                "Nickname": f"\"{member.nick}\"",
                "Discriminator": f"{member.discriminator}",
                "Activity": f"\"{member.activities[0].name}\"",
                "Roles": f"{len(member.roles)}",
                "Joined Time": f"{member.joined_at.strftime('%b %d, %Y, %T')}",
                "Creation Time": f"{member.created_at.strftime('%b %d, %Y, %T')}"
            }
        except:
            user_data = {
                "Name": f"\"{member.name}\"",
                "Nickname": f"\"{member.nick}\"",
                "Discriminator": f"{member.discriminator}",
                "Roles": f"{len(member.roles)}",
                "Joined Time": f"{member.joined_at.strftime('%b %d, %Y, %T')}",
                "Creation Time": f"{member.created_at.strftime('%b %d, %Y, %T')}"
            }

        # noinspection PyBroadException
        try:
            userEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=interaction.created_at,
                                       description=f"Ay ```\n"
                                                   f"(\nName : {user_data['Name']}\n\n"
                                                   f"Nickname : {user_data['Nickname']}\n\n"
                                                   f"Discriminator : {user_data['Discriminator']}\n\n"
                                                   f"Activity : {user_data['Activity']}\n\n"
                                                   f"Roles : {user_data['Roles']}\n\n"
                                                   f"Joined Time : {user_data['Joined Time']}\n\n"
                                                   f"Creation Time : {user_data['Creation Time']}\n)\n\n"
                                                   f"\n```")
        except:
            userEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=interaction.created_at,
                                       description=f"Ay ```\n"
                                                   f"(\nName : {user_data['Name']}\n\n"
                                                   f"Nickname : {user_data['Nickname']}\n\n"
                                                   f"Discriminator : {user_data['Discriminator']}\n\n"
                                                   f"Activity : None\n\n"
                                                   f"Roles : {user_data['Roles']}\n\n"
                                                   f"Joined Time : {user_data['Joined Time']}\n\n"
                                                   f"Creation Time : {user_data['Creation Time']}\n)\n\n"
                                                   f"\n```")

        # for [name, value] in user_data.items():
        #     serverEmbed.add_field(name=f'Ay ({name})', value=f"*Ay ({value})*")
        try:
            user = await self.client.fetch_user(member.id)
            banner_url = user.banner.url
            userEmbed.set_author(name=f"Ay! ({user_data['Name']} Information!)", icon_url=member.avatar.url)
            if banner_url:
                userEmbed.set_image(url=banner_url)
        except AttributeError:
            userEmbed.set_author(name=f"Ay! ({user_data['Name']} Information!)")
        userEmbed.set_footer(text=f"Ay! (ID: {member.id}!)")
        await interaction.send(embed=userEmbed)

    # endregion

    # region ECONOMY

    @nextcord.slash_command(name="balance", guild_ids=Variables.guild_ids)
    async def balance_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        """Check your balance!"""
        if member is None:
            member = interaction.user

        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

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

        balanceEmbed = nextcord.Embed(colour=Colors.dark_grey, title=f"Ay! ({member.name} Balance!)", timestamp=interaction.created_at)

        balanceEmbed.add_field(name='Ay (Wallet)', value=f"{Emojis.judd} *Ay* (**{wallet} BMD**)")
        balanceEmbed.add_field(name='Ay (Bank)', value=f"*Ay* (**{bank} / {max_bank} BMD**) {Emojis.lil_judd}")
        balanceEmbed.add_field(name='Ay (BMD Flow)', value=f"{Emojis.judd} *Ay* (**{wallet + bank} BMD**) {Emojis.lil_judd}")

        balanceEmbed.set_footer(text="Ay! (BMD = Big Man Dollars!)")

        await interaction.send(embed=balanceEmbed)

    @nextcord.slash_command(name='deposit', guild_ids=Variables.guild_ids)
    async def deposit_slash(self, interaction: nextcord.Interaction, amount: int = 50):
        """Deposit your BMD into the Big Man Bank! (0 for All)"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT * FROM curr WHERE user_id = {interaction.user.id}")
        data = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = data[1]
            bank = data[2]
            max_bank = data[3]
        except:
            return await interaction.send("Ay.. (Something with wrong..)", ephemeral=True)

        if amount == 0 and wallet + bank > max_bank:
            return await interaction.send("Ay.. (That amount goes over the Bank Capacity, you cannot deposit anymore BMD..)", ephemeral=True)

        if amount != 0 and amount < 1:
            return await interaction.send("Ay.. (Please deposit at least **1 BMD**..)", ephemeral=True)
        if wallet < amount:
            return await interaction.send("Ay.. (Not enough BMD to deposit..)")
        elif amount + bank > max_bank:
            return await interaction.send("Ay.. (That amount goes over the Bank Capacity, you cannot deposit anymore BMD..)", ephemeral=True)
        else:
            if amount == 0 and not wallet + bank > max_bank:
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank + wallet, interaction.user.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - wallet, interaction.user.id))
                await interaction.send(f"Ay! (You have placed **all your BMD** in the Big Man Bank!)")
            else:
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank + amount, interaction.user.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))
                await interaction.send(f"Ay! (You have placed **{amount} BMD** in the Big Man Bank!)")

        db.commit()
        cursor.close()
        db.close()

    @nextcord.slash_command(name='withdraw', guild_ids=Variables.guild_ids)
    async def withdraw_slash(self, interaction: nextcord.Interaction, amount: int = 50):
        """Withdraw your BMD from the Big Man Bank! (0 for All)"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT * FROM curr WHERE user_id = {interaction.user.id}")
        data = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = data[1]
            bank = data[2]
        except:
            return await interaction.send("Ay.. (Something with wrong..)", ephemeral=True)

        if amount != 0 and amount < 1:
            return await interaction.send("Ay.. (Please withdraw at least **1 BMD**..)")
        if bank < amount:
            return await interaction.send("Ay.. (Not enough BMD to withdraw)", ephemeral=True)
        else:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bank, interaction.user.id))
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank - bank, interaction.user.id))
                await interaction.send(f"Ay! (You have took **all your BMD** from the Big Man Bank!)")
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + amount, interaction.user.id))
                cursor.execute("UPDATE curr SET bank = ? WHERE user_id = ?", (bank - amount, interaction.user.id))
                await interaction.send(f"Ay! (You have took **{amount} BMD** from the Big Man Bank!)")

        db.commit()
        cursor.close()
        db.close()

    @nextcord.slash_command(name='job', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 1800, cooldowns.SlashBucket.author)
    async def job_slash(self, interaction: nextcord.Interaction):
        """Get a job! Make some BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        bmd_earned = random.randint(1, 100)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
        wallet = cursor.fetchone()

        # noinspection PyBroadException
        try:
            wallet = wallet[0]
        except:
            wallet = 0

        sql = "UPDATE curr SET wallet = ? WHERE user_id = ?"
        val = wallet + int(bmd_earned), interaction.user.id
        cursor.execute(sql, val)

        await interaction.send(f"Ay! (You earned **{bmd_earned} BMD**! Spend it wisely!)")

        db.commit()
        cursor.close()
        db.close()

    # noinspection PyUnusedLocal
    @job_slash.error
    async def job_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='loan', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 10, cooldowns.SlashBucket.author)
    async def loan_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, amount: int = 100):
        """Loan BMD to others!"""
        member = member
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
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

        if member == interaction.user:
            return await interaction.send("Ay!? (You can\'t give BMD to yourself!? Almost impossible!)", ephemeral=True)

        if wallet < amount:
            return await interaction.send("Ay.. (Not enough BMD to send to others..)", ephemeral=True)

        if amount < 100:
            return await interaction.send("Ay.. (Sorry, 100 or above to send BMD to others..)", ephemeral=True)

        cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))
        cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + amount, member.id))
        db.commit()

        await interaction.send(f"Ay! (You have sent **{amount} BMD** to {member.mention})")

    # noinspection PyUnusedLocal
    @loan_slash.error
    async def loan_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    # noinspection SpellCheckingInspection
    @nextcord.slash_command(name="turf", guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 60, cooldowns.SlashBucket.author)
    async def turf_slash(self, interaction: nextcord.Interaction, amount: int = 85):
        """Play Turf War for BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT * FROM inv WHERE user_id = {interaction.user.id}")
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

        if amount != 0 and amount < 85:
            return await interaction.send("Ay.. (Sorry, 85 or above to play turf..)", ephemeral=True)

        if wallet < amount:
            return await interaction.send("Ay.. (You don't have enough BMD to put in that much BMD..)", ephemeral=True)

        if cm_amiibos > 0:
            await start_turf_cm_amiibos(interaction)
        else:
            await start_turf(interaction)

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
                cursor.execute("UPDATE inv SET cm_amiibos = ? WHERE user_id = ?", (cm_amiibos - 1, interaction.user.id))
            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bmd_won, interaction.user.id))
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the Turf Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{bmd_won} BMD** you won! Use it wisely!)", timestamp=interaction.created_at)
            winEmbed.add_field(name=f"{interaction.user.name} Percentage", value=f"*{round(user_final, 1)}%*")
            winEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await interaction.send(embed=winEmbed)
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
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - bmd_lost, interaction.user.id))
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the Turf Battle..)",
                                       description=f"Ay.. (Better luck next time.. you lost **{bmd_lost} BMD**.)", timestamp=interaction.created_at)
            lostEmbed.add_field(name=f"{interaction.user.name} Percentage", value=f"*{round(user_final, 1)}%*")
            lostEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await interaction.send(embed=lostEmbed)
            cursor.close()
            db.close()

        else:

            # region TIE_CHECKS

            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the Turf Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=interaction.created_at)
            await interaction.send(embed=tieEmbed)
            cursor.close()
            db.close()

    # noinspection PyUnusedLocal
    @turf_slash.error
    async def turf_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='cheat', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 120, cooldowns.SlashBucket.author)
    async def cheat_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, amount: int = 500):
        """Cheat others for BMD?"""
        member = member
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
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

        if member == interaction.user:
            return await interaction.send("Ay!? (Cheat.. yourself!?)")

        if memWallet < amount:
            return await interaction.send("Ay.. (They don't have enough BMD for you to partake in this procedure..)", ephemeral=True)

        if amount != 0 and amount < 500:
            return await interaction.send("Ay.. (Sorry, 500 or above to cheat BMD from others..)", ephemeral=True)

        await start_cheat(interaction, member)

        user_chance = random.randint(1, 150)
        member_chance = random.randint(1, 150)

        if user_chance > member_chance:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + memWallet, interaction.user.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet - memWallet, member.id))
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + amount, interaction.user.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet - amount, member.id))
            db.commit()

            if amount == 0:
                takeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f":question: Ay..? (You cheated them successfully..?) :question:",
                                           description=f"Ay? (Enjoy the **{memWallet} BMD** you took? *Dials 911-SP3*)", timestamp=interaction.created_at)
            else:
                takeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f":question: Ay..? (You cheated them successfully..?) :question:",
                                           description=f"Ay? (Enjoy the **{amount} BMD** you took? *Dials 911-SP3*)", timestamp=interaction.created_at)

            await interaction.send(embed=takeEmbed)
            cursor.close()
            db.close()

        elif user_chance < member_chance:
            if amount == 0:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + memWallet, member.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - memWallet, interaction.user.id))
            else:
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (memWallet + amount, member.id))
                cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - amount, interaction.user.id))
            db.commit()

            if amount == 0:
                caughtEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay..? (You got caught..?)",
                                             description=f"Ay.. (See you later.. you were fined **{memWallet} BMD**. {member.name} has claimed this..)", timestamp=interaction.created_at)
            else:
                caughtEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay..? (You got caught..?)",
                                             description=f"Ay.. (See you later.. you were fined **{amount} BMD**. {member.name} has claimed this..)", timestamp=interaction.created_at)

            await interaction.send(embed=caughtEmbed)
            cursor.close()
            db.close()

        else:
            homeEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (You went back home!?)",
                                       description=f"Ay!? (You went back home and decided not to cheat someone!?)", timestamp=interaction.created_at)
            await interaction.send(embed=homeEmbed)
            cursor.close()
            db.close()

    # noinspection PyUnusedLocal
    @cheat_slash.error
    async def cheat_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    # noinspection SpellCheckingInspection
    @nextcord.slash_command(name='extreme-turf', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 90, cooldowns.SlashBucket.author)
    async def extreme_turf_slash(self, interaction: nextcord.Interaction, amount: int = 135):
        """Play Extreme Turf War for BMD!"""
        db = sqlite3.connect("curr.sqlite")
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
        wallet = cursor.fetchone()
        cursor.execute(f"SELECT * FROM inv WHERE user_id = {interaction.user.id}")
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
        
        if amount != 0 and amount < 135:
            return await interaction.send("Ay.. (Sorry, 135 or above to play extreme turf..)", ephemeral=True)

        if wallet < amount:
            return await interaction.send("Ay.. (You don't have enough BMD to put in that much BMD..)", ephemeral=True)

        if cm_amiibos > 0:
            await start_turf_extreme_cm_amiibos(interaction)
        else:
            await start_turf_extreme(interaction)

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
                cursor.execute("UPDATE inv SET cm_amiibos = ? WHERE user_id = ?", (cm_amiibos - 1, interaction.user.id))
            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet + bmd_won, interaction.user.id))
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the EXTREME Turf Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{bmd_won} BMD** you won! Use it wisely!)", timestamp=interaction.created_at)
            winEmbed.add_field(name=f"{interaction.user.name} Percentage", value=f"*{round(user_final, 1)}%*")
            winEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await interaction.send(embed=winEmbed)
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
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            cursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - bmd_lost, interaction.user.id))
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the EXTREME Turf Battle..)",
                                       description=f"Ay.. (Better luck next time.. you lost **{bmd_lost} BMD**.)", timestamp=interaction.created_at)
            lostEmbed.add_field(name=f"{interaction.user.name} Percentage", value=f"*{round(user_final, 1)}%*")
            lostEmbed.add_field(name=f"Opponent Percentage", value=f"*{round(opponent_final, 1)}%*")

            await interaction.send(embed=lostEmbed)
            cursor.close()
            db.close()

        else:

            # region TIE_CHECKS

            if shooters > 0:
                cursor.execute("UPDATE inv SET shooters = ? WHERE user_id = ?", (shooters - 1, interaction.user.id))
            if rollers > 0:
                cursor.execute("UPDATE inv SET rollers = ? WHERE user_id = ?", (rollers - 1, interaction.user.id))
            if splatlings > 0:
                cursor.execute("UPDATE inv SET splatlings = ? WHERE user_id = ?", (splatlings - 1, interaction.user.id))
            if blasters > 0:
                cursor.execute("UPDATE inv SET blasters = ? WHERE user_id = ?", (blasters - 1, interaction.user.id))
            if brushes > 0:
                cursor.execute("UPDATE inv SET brushes = ? WHERE user_id = ?", (brushes - 1, interaction.user.id))
            if dualies > 0:
                cursor.execute("UPDATE inv SET dualies = ? WHERE user_id = ?", (dualies - 1, interaction.user.id))
            if chargers > 0:
                cursor.execute("UPDATE inv SET chargers = ? WHERE user_id = ?", (chargers - 1, interaction.user.id))
            if sloshers > 0:
                cursor.execute("UPDATE inv SET sloshers = ? WHERE user_id = ?", (sloshers - 1, interaction.user.id))
            if brellas > 0:
                cursor.execute("UPDATE inv SET brellas = ? WHERE user_id = ?", (brellas - 1, interaction.user.id))

            # endregion

            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the EXTREME Turf Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=interaction.created_at)
            await interaction.send(embed=tieEmbed)
            cursor.close()
            db.close()

    # noinspection PyUnusedLocal
    @extreme_turf_slash.error
    async def extreme_turf_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='inventory', guild_ids=Variables.guild_ids)
    async def inventory_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        """View inventories!"""

        await set_inv(member, interaction.user, interaction.created_at, interaction)

    # @nextcord.slash_command(name='market', guild_ids=Variables.guild_ids)
    # @cooldowns.cooldown(1, 5, cooldowns.SlashBucket.author)
    # async def market_slash(self, interaction: nextcord.Interaction):
    #     """View the Marketplace where you can spend BMD!"""
    #
    #     db = sqlite3.connect('curr.sqlite')
    #     cursor = db.cursor()
    #
    #     cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
    #     enabled = cursor.fetchone()
    #     if enabled and not enabled[0]:
    #         return await interaction.send('Ay.. (Economy is currently disabled for this server..)', ephemeral=True)
    #
    #     data = External.set_shop(interaction.created_at)
    #     pages = Paginations.GlobalPageSource.GlobalButtonMenu(
    #         source=Paginations.GlobalPageSource(data),
    #     )
    #     await pages.start(interaction=interaction)
    #     await interaction.send(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
    #     # await External.paginate(self.client, interaction, interaction.user, set_shop(interaction.created_at), Selections.MarketSelection.ShopDropdown(self.client), True)
    #     # await ctx.send(view=Selections.MarketSelection.ShopDropdown(self.client))
    #     cursor.close()
    #     db.close()

    # noinspection PyUnusedLocal
    # @market_slash.error
    # async def market_error(self, ctx, error):
    #     if isinstance(error, TypeError):
    #         return

    @nextcord.slash_command(name='gift', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 8, cooldowns.SlashBucket.author)
    async def gift_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, item_id: str, amount: int = 1):
        """Gift your items to others!"""

        await gift_check(item_id, interaction, interaction.user, member, amount, self.client)

    # noinspection PyUnusedLocal
    @gift_slash.error
    async def gift_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='sell', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 8, cooldowns.SlashBucket.author)
    async def sell_slash(self, interaction: nextcord.Interaction, item_id: str, amount: int = 1):
        """Sell your items for BMD!"""

        await sell_check(item_id, interaction, interaction.user, amount)

    # noinspection PyUnusedLocal
    @sell_slash.error
    async def sell_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    # noinspection SpellCheckingInspection
    # @nextcord.slash_command(name='bmdboard', guild_ids=Variables.guild_ids)
    # async def bmdboard_slash(self, interaction: nextcord.Interaction):
    #     """Shows all the balances ranked!"""
    #
    #     db = sqlite3.connect('curr.sqlite')
    #     cursor = db.cursor()
    #
    #     cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
    #     enabled = cursor.fetchone()
    #     if enabled and not enabled[0]:
    #         return await interaction.send('Ay.. (Economy is currently disabled for this server..)')
    #
    #     cursor.execute(f'SELECT user_id, wallet, bank FROM curr ORDER BY (wallet+bank) DESC LIMIT 10')
    #     data = cursor.fetchall()
    #
    #     if data:
    #         bmdEmbed = nextcord.Embed(title='Ay! (Global Economy System Leaderboard!)', color=Colors.dark_grey, timestamp=interaction.created_at)
    #         count = 0
    #
    #         for table in data:
    #             count += 1
    #             user = interaction.guild.get_member(table[0])
    #
    #             bmdEmbed.add_field(name=f'Ay! ({count}. {user.name + "#" + user.discriminator})',
    #                                value=f"*Ay* (**BMD Flow** : *{table[1] + table[2]}*)", inline=False)
    #
    #         bmdEmbed.set_footer(text=f"Ay! (Top 10 Results!)")
    #         return await interaction.send(embed=bmdEmbed)
    #     return await interaction.send("Ay.. (I can't seem to find anyone stored in my database for the economy leaderboard..)")

    # endregion

    # region LEVELING

    @nextcord.slash_command(name='level', guild_ids=Variables.guild_ids)
    async def level_slash(self, interaction: nextcord.Interaction, member: nextcord.Member = None):
        """View levels!"""
        if member is None:
            member = interaction.user

        guild = interaction.guild

        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Leveling is currently disabled for this server..)', ephemeral=True)

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
            "next_lvl_xp": xp_max,
            "percent": xp
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
        await interaction.send(file=file)

        cursor.close()
        db.close()

    # noinspection SpellCheckingInspection
    @nextcord.slash_command(name='blitz', guild_ids=Variables.guild_ids)
    @cooldowns.cooldown(1, 180, cooldowns.SlashBucket.author)
    async def blitz_slash(self, interaction: nextcord.Interaction):
        """Play Experience Blitz for XP!"""

        await interaction.send("Ay? (Are you sure you want to play Experience Blitz? A **300 BMD** fee is required to play.)")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            return await interaction.send("Ay! (No Experience Blitz! Got it!)")

        db = sqlite3.connect("level.sqlite")
        cursor = db.cursor()
        
        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {interaction.guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Leveling is currently disabled for this server..)', ephemeral=True)
        
        cursor.execute(f"SELECT xp FROM levels WHERE user_id = {interaction.user.id}")
        xp = cursor.fetchone()

        currDb = sqlite3.connect("curr.sqlite")
        currCursor = currDb.cursor()
        currCursor.execute(f"SELECT wallet FROM curr WHERE user_id = {interaction.user.id}")
        wallet = currCursor.fetchone()
        currCursor.execute(f"SELECT pm_amiibos FROM inv WHERE user_id = {interaction.user.id}")
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
            return await interaction.send("Ay.. (300 BMD is required to play..)", ephemeral=True)

        if pm_amiibos > 0:
            await start_blitz_pm_amiibos(interaction)
        else:
            await start_blitz(interaction)

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
                currCursor.execute("UPDATE inv SET pm_amiibos = ? WHERE user_id = ?", (pm_amiibos - 1, interaction.user.id))
            currCursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - 300, interaction.user.id))
            cursor.execute("UPDATE levels SET xp = ? WHERE user_id = ?", (xp + xp_won, interaction.user.id))
            currDb.commit()
            db.commit()

            winEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"{Emojis.something_man} Ay! (You win the Experience Blitz Battle!) {Emojis.dancing_man}",
                                      description=f"Ay! (Please enjoy the **{xp_won} XP** you won! Use it wisely!)", timestamp=interaction.created_at)
            if opponent_final == "KNOCKOUT":
                winEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{user_final}*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            elif user_final == "KNOCKOUT":
                winEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{user_final}*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            else:
                winEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{round(user_final)} XP*")
                winEmbed.add_field(name=f"Opponent Count", value=f"*{round(opponent_final)} XP*")

            await interaction.send(embed=winEmbed)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

        elif user_chance < opponent_chance:
            xp_won = random.randint(1, 50)
            currCursor.execute("UPDATE curr SET wallet = ? WHERE user_id = ?", (wallet - 300, interaction.user.id))
            cursor.execute("UPDATE levels SET xp = ? WHERE user_id = ?", (xp + xp_won, interaction.user.id))
            currDb.commit()
            db.commit()

            lostEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay.. (You lost the Experience Blitz Battle..)",
                                       description=f"Ay.. (Better luck next time.. you still won **{xp_won} XP**.)", timestamp=interaction.created_at)
            if opponent_final == "KNOCKOUT":
                lostEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{user_final} XP*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final}*")
            elif user_final == "KNOCKOUT":
                lostEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{user_final}*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{opponent_final} XP*")
            else:
                lostEmbed.add_field(name=f"{interaction.user.name} Count", value=f"*{round(user_final)}*")
                lostEmbed.add_field(name=f"Opponent Count", value=f"*{round(opponent_final)}*")

            await interaction.send(embed=lostEmbed)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

        else:
            tieEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay!? (No one won the Experience Blitz Battle! Tie!)",
                                      description=f"Ay (It was a tie, come back whenever you want!)", timestamp=interaction.created_at)
            await interaction.send(embed=tieEmbed)
            cursor.close()
            currCursor.close()
            db.close()
            currDb.close()

    # noinspection PyUnusedLocal
    @blitz_slash.error
    async def blitz_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    # noinspection SpellCheckingInspection
    @nextcord.slash_command(name='levelboard', guild_ids=Variables.guild_ids)
    async def levelboard_slash(self, interaction: nextcord.Interaction):
        """Shows all the levels ranked!"""

        guild = interaction.guild

        db = sqlite3.connect('level.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Leveling is currently disabled for this server..)')

        cursor.execute(f'SELECT user_id, level, xp FROM levels WHERE guild_id = {guild.id} ORDER BY level DESC, xp DESC LIMIT 10')
        data = cursor.fetchall()

        if data:
            levelEmbed = nextcord.Embed(title='Ay! (Level System Leaderboard!)', color=Colors.dark_grey, timestamp=interaction.created_at)
            count = 0

            for table in data:
                count += 1
                user = interaction.guild.get_member(table[0])

                levelEmbed.add_field(name=f'Ay! ({count}. {user.name + "#" + user.discriminator})',
                                     value=f"*Ay* (**Level** : *{table[1]}* | **XP** : *{table[2]} / {table[1] * 30}*)", inline=False)

            return await interaction.send(embed=levelEmbed)
        return await interaction.send("Ay.. (I can't seem to find anyone stored in my database for the leveling leaderboard..)", ephemeral=True)

    # endregion

    # region MANAGEMENT

    @nextcord.slash_command(name='system', guild_ids=Variables.guild_ids)
    async def system_slash(self, interaction: nextcord.Interaction):
        """Configure system-related commands!"""
        pass

    @system_slash.subcommand(name='enable')
    @application_checks.has_permissions(manage_guild=True)
    async def enable_slash(self, interaction: nextcord.Interaction, system_name: str):
        """Enable built-in systems!

        system_name: str
            LEVELING_SYSTEM, ECONOMY_SYSTEM, STARBOARD_SYSTEM
        """

        system_names = ['LEVELING_SYSTEM', 'ECONOMY_SYSTEM', 'STARBOARD_SYSTEM']

        if system_name.upper() not in system_names:
            return await interaction.send("Ay.. (I couldn't find that system.. Here are my current ones: `" + ", ".join(system_names) + "`)", ephemeral=True)

        guild = interaction.guild

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
                    return await interaction.send("Ay! (Leveling is already enabled in this server!)", ephemeral=True)
                levelCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                levelCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                levelDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            levelDb.commit()

            await interaction.send("Ay! (Leveling has been enabled for this server!)")
            levelCursor.close()
            levelDb.close()

        if system_name.upper() == system_names[1]:

            currCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = currCursor.fetchone()

            if enabled:
                if enabled[0]:
                    return await interaction.send("Ay! (Economy is already enabled in this server!)", ephemeral=True)
                currCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                currCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                currDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            currDb.commit()

            await interaction.send("Ay! (Economy has been enabled for this server!)")
            currCursor.close()
            currDb.close()

        if system_name.upper() == system_names[2]:

            mainCursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
            enabled = mainCursor.fetchone()

            if enabled:
                if enabled[0]:
                    return await interaction.send("Ay! (Starboard is already enabled in this server!)", ephemeral=True)
                mainCursor.execute('UPDATE starSystem SET enabled = ? WHERE guild_id = ?', (True, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                mainCursor.execute('INSERT INTO starSystem (guild_id, enabled) VALUES (?, ?)', (guild.id, True))
                mainDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            mainDb.commit()

            await interaction.send("Ay! (Starboard has been enabled for this server!)")
            mainCursor.close()
            mainDb.close()

    @system_slash.subcommand(name='disable')
    @application_checks.has_permissions(manage_guild=True)
    async def disable_slash(self, interaction: nextcord.Interaction, system_name: str):
        """Disable built-in systems!

        system_name: str
            LEVELING_SYSTEM, ECONOMY_SYSTEM, STARBOARD_SYSTEM
        """

        system_names = ['LEVELING_SYSTEM', 'ECONOMY_SYSTEM', 'STARBOARD_SYSTEM']

        if system_name.upper() not in system_names:
            return await interaction.send("Ay.. (I couldn't find that system.. Here are my current ones: `" + ", ".join(system_names) + "`)", ephemeral=True)

        guild = interaction.guild

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
                    return await interaction.send("Ay! (Leveling is already disabled in this server!)", ephemeral=True)
                levelCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                levelCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                levelDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            levelDb.commit()

            await interaction.send("Ay! (Leveling has been disabled for this server!)")
            levelCursor.close()
            levelDb.close()

        if system_name.upper() == system_names[1]:

            currCursor.execute(f'SELECT enabled FROM system WHERE guild_id = {guild.id}')
            enabled = currCursor.fetchone()

            if enabled:
                if not enabled[0]:
                    return await interaction.send("Ay! (Economy is already disabled in this server!)", ephemeral=True)
                currCursor.execute('UPDATE system SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                currCursor.execute('INSERT INTO system (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                currDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            currDb.commit()

            await interaction.send("Ay! (Economy has been disabled for this server!)", ephemeral=True)
            currCursor.close()
            currDb.close()

        if system_name.upper() == system_names[2]:

            mainCursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
            enabled = mainCursor.fetchone()

            if enabled:
                if not enabled[0]:
                    return await interaction.send("Ay! (Starboard is already disabled in this server!)", ephemeral=True)
                mainCursor.execute('UPDATE starSystem SET enabled = ? WHERE guild_id = ?', (False, guild.id))
            else:
                msg = await interaction.send("Ay.. (Couldn't find data for system in this server.. Creating it now! Try using system commands again afterwards.)", ephemeral=True)
                mainCursor.execute('INSERT INTO starSystem (guild_id, enabled) VALUES (?, ?)', (guild.id, False))
                mainDb.commit()
                return await msg.edit(content="Ay! (Complete adding system data!)")
            mainDb.commit()

            await interaction.send("Ay! (Starboard has been disabled for this server!)", ephemeral=True)
            mainCursor.close()
            mainDb.close()

    @nextcord.slash_command(name='star-setup', guild_ids=Variables.guild_ids)
    async def star_setup_slash(self):
        """Configure starboard-related commands!"""
        pass

    @star_setup_slash.subcommand(name='channel')
    @application_checks.has_permissions(manage_guild=True)
    async def channel_slash(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        """Set the channel for Starboard!"""

        guild = interaction.guild

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Starboard is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f'SELECT channel_id FROM starboard WHERE guild_id = {guild.id}')
        channelData = cursor.fetchone()

        if channelData:
            channelData = channelData[0]

            if channelData == channel.id:
                return await interaction.send("Ay! (That channel is already the starboard channel!)", ephemeral=True)
            cursor.execute('UPDATE starboard SET channel_id = ? WHERE guild_id = ?', (channel.id, guild.id))
            await interaction.send(f"Ay! (The starboard channel has now been set to {channel.mention}!)")
        else:
            msg = await interaction.send("Ay.. (I couldn't find any starboard data for this server.. Creating it now! Try using starboard setup commands again afterwards..", ephemeral=True)
            cursor.execute('INSERT INTO starboard (guild_id, channel_id, stars) VALUES (?, ?, ?)', (guild.id, channel.id, 5))
            db.commit()
            return await msg.edit("Ay! (Complete adding starboard data!)")
        db.commit()
        cursor.close()
        db.close()

    @star_setup_slash.subcommand(name='limit')
    @application_checks.has_permissions(manage_guild=True)
    async def limit_slash(self, interaction: nextcord.Interaction, limit: int):
        """Set the channel for Starboard!"""

        guild = interaction.guild

        if limit == 0:
            return await interaction.send('Ay.. (You cannot set the star limit to **0**..)', ephemeral=True)

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(f'SELECT enabled FROM starSystem WHERE guild_id = {guild.id}')
        enabled = cursor.fetchone()
        if enabled and not enabled[0]:
            return await interaction.send('Ay.. (Starboard is currently disabled for this server..)', ephemeral=True)

        cursor.execute(f'SELECT stars FROM starboard WHERE guild_id = {guild.id}')
        limitData = cursor.fetchone()

        if limitData:
            limitData = limitData[0]

            if limit == limitData:
                return await interaction.send("Ay! (That star limit is already the starboard star limit!)", ephemeral=True)
            cursor.execute('UPDATE starboard SET stars = ? WHERE guild_id = ?', (limit, guild.id))
            await interaction.send(f"Ay! (The starboard star limit has now been set to **{limit}**!)")
        else:
            msg = await interaction.send("Ay.. (I couldn't find any starboard data for this server.. Creating it now! Try using starboard setup commands again afterwards..", ephemeral=True)
            cursor.execute('INSERT INTO starboard (guild_id, channel, stars) VALUES (?, ?, ?)', (guild.id, 0, 5, True))
            db.commit()
            return await msg.edit("Ay! (Complete adding starboard data!)")
        db.commit()
        cursor.close()
        db.close()

    @nextcord.slash_command(name='clean-invites', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(manage_guild=True)
    @cooldowns.cooldown(1, 30, cooldowns.SlashBucket.guild)
    async def clean_invites_slash(self, interaction: nextcord.Interaction):
        """Clean all invites in the server!"""
        await interaction.send("Ay? (Are you sure you want to clean all the invites?)")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            return await interaction.send("Ay! (Operation Aborted!)", ephemeral=True)

        msg = await interaction.send("Ay.. (Purging invites..)")

        for invite in await interaction.guild.invites():
            await invite.delete()

        await msg.edit("Ay! (Operation Complete! All invites have been purged!)")

    # noinspection PyUnusedLocal
    @clean_invites_slash.error
    async def clean_invites_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='clean-roles', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(manage_roles=True)
    @cooldowns.cooldown(1, 30, cooldowns.SlashBucket.guild)
    async def clean_roles_slash(self, interaction: nextcord.Interaction):
        """Clean all roles in the server!"""
        await interaction.send("Ay? (Are you sure you want to clean all the roles?)")

        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel

        try:
            response = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

        if response.content.lower() not in ("yes", "y"):
            return await interaction.send("Ay! (Operation Aborted!)", ephemeral=True)

        msg = await interaction.send("Ay.. (Purging roles..)")

        for role in interaction.guild.roles:
            # noinspection PyBroadException
            try:
                await role.delete()
            except:
                continue

        await msg.edit("Ay! (Operation Complete! All roles have been purged!)")

    # noinspection PyUnusedLocal
    @clean_roles_slash.error
    async def clean_roles_error(self, ctx, error):
        if isinstance(error, TypeError):
            return

    @nextcord.slash_command(name='kick', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(kick_members=True)
    async def kick_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason=None):
        """Kicks whoever needs to be kicked!"""

        if member == interaction.user:
            return await interaction.send("Ay!? (Kicking yourself!? Almost impossible!)", ephemeral=True)
        if member == self.client.user:
            return await interaction.send("Ay!? (Kicking **me**!? Almost impossible!)", ephemeral=True)

        kickEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay! (Kick Success!)", timestamp=interaction.created_at,
                                   description=f"*Ay! (**ID:** `{member.id}`)*\n*Ay! (**Username:** `{member.name}`)*\n*Ay! (**Tag:** `{member.discriminator}`)*\n*Ay! (**Reason:** `{reason}`)*")

        await member.kick(reason=reason)
        await interaction.send(embed=kickEmbed)

    @nextcord.slash_command(name='ban', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(ban_members=True)
    async def ban_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason=None):
        """Bans whoever needs to be banned!"""

        if member == interaction.user:
            return await interaction.send("Ay!? (Banning yourself!? Almost impossible!)", ephemeral=True)
        if member == self.client.user:
            return await interaction.send("Ay!? (Banning **me**!? Almost impossible!)", ephemeral=True)

        banEmbed = nextcord.Embed(color=Colors.dark_grey, title=f"Ay! (Ban Success!)", timestamp=interaction.created_at,
                                  description=f"*Ay! (**ID:** `{member.id}`)*\n*Ay! (**Username:** `{member.name}`)*\n*Ay! (**Tag:** `{member.discriminator}`)*\n*Ay! (**Reason:** `{reason}`)*")

        await member.ban(reason=reason)
        await interaction.send(embed=banEmbed)

    @nextcord.slash_command(name='clear', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(manage_messages=True)
    async def clear_slash(self, interaction: nextcord.Interaction, amount: int = 1):
        """Clears out messages!"""
        if amount < 1:
            return await interaction.send("Ay.. (You have to clear 1 or more messages..)", ephemeral=True)

        if amount > 100:
            return await interaction.send("Ay.. (Cannot purge more than 100 messages..)", ephemeral=True)
        else:
            await interaction.channel.purge(limit=amount)
            await interaction.send(f'Ay! (I have cleared out {amount} messages in this channel!)', delete_after=5)

    @nextcord.slash_command(name='timeout', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(moderate_members=True)
    async def timeout_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, time, *, reason=None):
        """Timeout members for duration of time!"""

        # noinspection PyBroadException
        try:
            time = humanfriendly.parse_timespan(time)
        except:
            return await interaction.send("Ay.. (Something went wrong.. I don't think the time is valid..)", ephemeral=True)

        if member == interaction.user:
            return await interaction.send("Ay!? (Timing out yourself!? Almost impossible!)", ephemeral=True)
        if member == self.client.user:
            return await interaction.send("Ay!? (Timing out **me**!? Almost impossible!)", ephemeral=True)

        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        await interaction.send(f"Ay! (Timed out {member.mention} for **{round(time)} Seconds**! Reasoning can be viewed in audit log!)")

    @nextcord.slash_command(name='de-timeout', guild_ids=Variables.guild_ids)
    @application_checks.has_permissions(moderate_members=True)
    async def de_timeout_slash(self, interaction: nextcord.Interaction, member: nextcord.Member, *, reason=None):
        """De-timeout members who have been timed out!"""

        if member == interaction.user:
            return await interaction.send("Ay!? (De-timing out yourself!? Almost impossible!)", ephemeral=True)
        if member == self.client.user:
            return await interaction.send("Ay!? (De-timing out **me**!? Almost impossible!)", ephemeral=True)

        await member.edit(timeout=None, reason=reason)
        await interaction.send(f"Ay! (De-timed out {member.mention}! Reasoning can be viewed in audit log!)")

    # endregion

    # region ENTERTAINMENT

    @nextcord.slash_command(name='translate', guild_ids=Variables.guild_ids)
    async def translate_slash(self, interaction: nextcord.Interaction, language: str, *, message: str):
        """Translate messages to another language!"""
        translator = Translator()

        try:
            translation = translator.translate(message, dest=language)
        except ValueError:
            return await interaction.send("Ay.. (Something went wrong.. is that language correct?)", ephemeral=True)

        translateEmbed = nextcord.Embed(title='Ay! (Translation!)', description=f"Ay \n```\n(\"{translation.text}\")\n```", color=Colors.dark_grey, timestamp=interaction.created_at)
        translateEmbed.set_footer(text=f"Ay! (Language: {language.upper()}!)")

        await interaction.send(embed=translateEmbed)

    @nextcord.slash_command(name='8ball', guild_ids=Variables.guild_ids)
    async def _8ball_slash(self, interaction: nextcord.Interaction, *, message: str):
        """Ask questions! Get answers!"""

        inputs = [
            "Ay.. (I'm not too sure..)",
            "Ay! Ay! Ay! (Yes, Yes, Yes!)",
            "Ay.. Ay.. Ay.. (No, No, No..)"
            "Ay! (For sure!)",
            "Ay.. (I don't think so..)",
            "Ay (No)",
            "Ay (Yes)",
            "Ay..? (I didn't quite catch that..)",
            "Ay- (Uhm-)",
            "Ay? (Maybe?)"
        ]

        _8ballEmbed = nextcord.Embed(title="Ay! (Question Asked!)", color=Colors.dark_grey, timestamp=interaction.created_at)

        if message.lower() != "are you real?":
            _8ballEmbed.add_field(name='Ay (Question)', value=f"*`Ay (\"{message}\")`*", inline=False)
            _8ballEmbed.add_field(name='Ay (Answer)', value=f"*`{random.choice(inputs)}`*", inline=False)
        else:
            _8ballEmbed.add_field(name='Ay (Question)', value=f"*`Ay (\"{message}\")`*", inline=False)
            _8ballEmbed.add_field(name='Ay (Answer)', value=f"*`Ay. (Yes. Or am I? This is confusing..)`*", inline=False)

        await interaction.send(embed=_8ballEmbed)

    @nextcord.slash_command(name='reverse', guild_ids=Variables.guild_ids)
    async def reverse_slash(self, interaction: nextcord.Interaction, *, message: str):
        """Reverse messages to make them backwards!"""

        reverseEmbed = nextcord.Embed(title='Ay! (Reversed!)', description=f"Ay \n```\n(\"{message[::-1]}\")\n```", color=Colors.dark_grey, timestamp=interaction.created_at)

        await interaction.send(embed=reverseEmbed)

    @nextcord.slash_command(name='youtube', guild_ids=Variables.guild_ids)
    async def youtube_slash(self, interaction: nextcord.Interaction, *, message: str):
        """Search for something on YouTube!"""

        query_string = parse.urlencode({'search_query': message})
        htm_content = request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',
                                    htm_content.read().decode())
        await interaction.send("Ay\n" + 'http://www.youtube.com/watch?v=' + search_results[0])

    @nextcord.slash_command(name='cat', guild_ids=Variables.guild_ids)
    async def cat_slash(self, interaction: nextcord.Interaction):
        """Look at images of cats!"""
        response = requests.get('https://some-random-api.ml/img/cat')
        data = response.json()
        # noinspection PyBroadException
        try:
            catEmbed = nextcord.Embed(title="Ay!? (Cat!?)", color=Colors.dark_grey, timestamp=interaction.created_at)
            catEmbed.set_image(url=data['link'])
            return await interaction.send(embed=catEmbed)
        except:
            return await interaction.send("Ay.. (An error has occurred.. maybe try again later..)", ephemeral=True)

    @nextcord.slash_command(name='dog', guild_ids=Variables.guild_ids)
    async def dog_slash(self, interaction: nextcord.Interaction):
        """Look at images of dogs!"""
        response = requests.get('https://some-random-api.ml/img/dog')
        data = response.json()
        # noinspection PyBroadException
        try:
            dogEmbed = nextcord.Embed(title="Ay!? (Dog!?)", color=Colors.dark_grey, timestamp=interaction.created_at)
            dogEmbed.set_image(url=data['link'])
            return await interaction.send(embed=dogEmbed)
        except:
            return await interaction.send("Ay.. (An error has occurred.. maybe try again later..)", ephemeral=True)

    @nextcord.slash_command(name='base64', guild_ids=Variables.guild_ids)
    async def base64_slash(self, interaction: nextcord.Interaction, *, message: str):
        """Convert messages to Base64!"""
        response = requests.get('https://some-random-api.ml/base64?encode=' + message)
        data = response.json()
        # noinspection PyBroadException
        try:
            text = data.get('base64')
            baseEmbed = nextcord.Embed(title="Ay!? (Encoded!)", color=Colors.dark_grey, description=f"Ay \n```\n(\"{text}\")\n```", timestamp=interaction.created_at)
            return await interaction.send(embed=baseEmbed)
        except:
            return await interaction.send("Ay.. (An error has occurred.. maybe try again later..", ephemeral=True)

    @nextcord.slash_command(name='binary', guild_ids=Variables.guild_ids)
    async def binary_slash(self, interaction: nextcord.Interaction, *, message: str):
        """Convert images to Binary!"""
        response = requests.get('https://some-random-api.ml/binary?encode=' + message)
        data = response.json()
        # noinspection PyBroadException
        try:
            text = data.get('binary')
            binaryEmbed = nextcord.Embed(title="Ay!? (Encoded!)", color=Colors.dark_grey, description=f"Ay \n```\n(\"{text}\")\n```", timestamp=interaction.created_at)
            return await interaction.send(embed=binaryEmbed)
        except:
            return await interaction.send("Ay.. (An error has occurred.. maybe try again later..", ephemeral=True)

    # endregion


def setup(client):
    client.add_cog(Slash(client))
