import asyncio
import sqlite3

import nextcord
from nextcord.ext import menus

from External import Colors, Emojis, Costs


class Modals:
    class RequestModal(nextcord.ui.Modal):
        def __init__(self, client):
            super().__init__(
                "Ay (Feature Request)",
                timeout=10 * 60,
            )

            self.client = client

            self.name = nextcord.ui.TextInput(
                label="Ay (Feature Name)",
                placeholder='Ay! (Describe the name!)',
                required=True
            )
            self.add_item(self.name)

            self.description = nextcord.ui.TextInput(
                label="Ay (Feature Description)",
                style=nextcord.TextInputStyle.paragraph,
                placeholder="Ay! (Describe this wonderful feature!)",
                required=True
            )
            self.add_item(self.description)

        async def callback(self, interaction: nextcord.Interaction) -> None:
            response = f"Ay! (Thanks for submitting a request!)"
            await interaction.send(response)

            requestEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Feature Request Incoming!)", timestamp=interaction.created_at)

            requestEmbed.add_field(name="Ay (Feature Name)", value=f"*Ay* ```\n({self.name.value})\n```", inline=False)
            requestEmbed.add_field(name="Ay (Feature Description)", value=f"*Ay* ```\n({self.description.value})```", inline=False)
            requestEmbed.add_field(name="Ay (Feature Sender)", value=f"*Ay* ```\n({interaction.user.name + '#' + interaction.user.discriminator})\n```")

            await self.client.get_channel(1024134182479331329).send(embed=requestEmbed)

    class BugModal(nextcord.ui.Modal):
        def __init__(self, client):
            super().__init__(
                "Ay (Bug Report)",
                timeout=10 * 60,
            )

            self.client = client

            self.name = nextcord.ui.TextInput(
                label="Ay (Bug Name)",
                placeholder='Ay! (Describe the bug briefly!)',
                required=True
            )
            self.add_item(self.name)

            self.description = nextcord.ui.TextInput(
                label="Ay (Bug Description)",
                style=nextcord.TextInputStyle.paragraph,
                placeholder="Ay! (Describe this bug report!)",
                required=True
            )
            self.add_item(self.description)

        async def callback(self, interaction: nextcord.Interaction) -> None:
            response = f"Ay! (Thanks for submitting a bug report!)"
            await interaction.send(response)

            bugEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Bug Report Incoming!)", timestamp=interaction.created_at)

            bugEmbed.add_field(name="Ay (Bug Name)", value=f"*Ay* ```\n({self.name.value})\n```", inline=False)
            bugEmbed.add_field(name="Ay (Bug Description)", value=f"*Ay* ```\n({self.description.value})```", inline=False)
            bugEmbed.add_field(name="Ay (Bug Sender)", value=f"*Ay* ```\n({interaction.user.name + '#' + interaction.user.discriminator})\n```")

            await self.client.get_channel(1025667754394652702).send(embed=bugEmbed)


class Selections:
    # noinspection SpellCheckingInspection
    class SplatResultSelection(nextcord.ui.Select):
        def __init__(self):
            self.splatfest = [
                "Ay (Rock vs. Paper vs. Scissors)",
                "Ay (Gear vs. Grub vs. Fun)"
            ]

            self.selectOptions = [
                nextcord.SelectOption(label=self.splatfest[0], description="Ay! (R.P.S Splatfest Results!)", emoji="⛰"),
                nextcord.SelectOption(label=self.splatfest[1], description="Ay! (G.G.F Splatfest Results!)", emoji="⚙")
            ]
            super().__init__(placeholder="Ay! (Select Splatfest!)", options=self.selectOptions)

        async def callback(self, interaction: nextcord.Interaction):
            return

        class ResultDropdown(nextcord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(Selections.SplatResultSelection())

    # noinspection SpellCheckingInspection
    class MarketSelection(nextcord.ui.Select):
        def __init__(self, client):
            self.client = client

            self.market = [
                "Ay ( Great Zapfish Replica (Statue) )",
                "Ay ( Callie & Marie (Amiibo) )",
                "Ay ( Pearl & Marina (Amiibo) )",
                "Ay ( Shooters (Weapon) )",
                "Ay ( Rollers (Weapon) )",
                "Ay ( Splatlings (Weapon) )",
                "Ay ( Blasters (Weapon) )",
                "Ay ( Brushes (Weapon) )",
                "Ay ( Dualies (Weapon) )",
                "Ay ( Chargers (Weapon) )",
                "Ay ( Sloshers (Weapon) )",
                "Ay ( Brellas (Weapon) )",
                "Ay ( Big Man Bank Upgrade (12k) )",
                "Ay ( Big Man Bank Upgrade (6k) )",
                "Ay ( Big Man Bank Upgrade (3k) )",
                "Ay ( Big Man Bank Upgrade (96k) )",
                "Ay ( Big Man Bank Upgrade (48k) )",
                "Ay ( Big Man Bank Upgrade (24k) )"
            ]

            self.selectOptions = [
                nextcord.SelectOption(label=self.market[0], description="Ay? (Purchase this item for 100k BMD?)", emoji=f"{Emojis.zapfish_replica}"),
                nextcord.SelectOption(label=self.market[1], description="Ay? (Purchase this item for 2.2k BMD?)", emoji=f"{Emojis.callie_marie_amiibos}"),
                nextcord.SelectOption(label=self.market[2], description="Ay? (Purchase this item for 2.4k BMD?)", emoji=f"{Emojis.pearl_marina_amiibos}"),

                nextcord.SelectOption(label=self.market[3], description="Ay? (Purchase this item for 500 BMD?)", emoji=f"{Emojis.shooters}"),
                nextcord.SelectOption(label=self.market[4], description="Ay? (Purchase this item for 800 BMD?)", emoji=f"{Emojis.rollers}"),
                nextcord.SelectOption(label=self.market[5], description="Ay? (Purchase this item for 1.1k BMD?)", emoji=f"{Emojis.splatlings}"),
                nextcord.SelectOption(label=self.market[6], description="Ay? (Purchase this item for 1.4k BMD?)", emoji=f"{Emojis.blasters}"),
                nextcord.SelectOption(label=self.market[7], description="Ay? (Purchase this item for 1.7k BMD?)", emoji=f"{Emojis.brushes}"),
                nextcord.SelectOption(label=self.market[8], description="Ay? (Purchase this item for 2k BMD?)", emoji=f"{Emojis.dualies}"),
                nextcord.SelectOption(label=self.market[9], description="Ay? (Purchase this item for 2.3k BMD?)", emoji=f"{Emojis.chargers}"),
                nextcord.SelectOption(label=self.market[10], description="Ay? (Purchase this item for 2.6k BMD?)", emoji=f"{Emojis.sloshers}"),
                nextcord.SelectOption(label=self.market[11], description="Ay? (Purchase this item for 2.9k BMD?)", emoji=f"{Emojis.brellas}"),

                nextcord.SelectOption(label=self.market[12], description="Ay? (Purchase this upgrade for 12k BMD?)", emoji=f"{Emojis.big_man_bank}"),
                nextcord.SelectOption(label=self.market[13], description="Ay? (Purchase this upgrade for 6k BMD?)", emoji=f"{Emojis.big_man_bank}"),
                nextcord.SelectOption(label=self.market[14], description="Ay? (Purchase this upgrade for 3k BMD?)", emoji=f"{Emojis.big_man_bank}"),
                nextcord.SelectOption(label=self.market[15], description="Ay? (Purchase this upgrade for 96k BMD?)", emoji=f"{Emojis.big_man_bank}"),
                nextcord.SelectOption(label=self.market[16], description="Ay? (Purchase this upgrade for 48k BMD?)", emoji=f"{Emojis.big_man_bank}"),
                nextcord.SelectOption(label=self.market[17], description="Ay? (Purchase this upgrade for 24k BMD?)", emoji=f"{Emojis.big_man_bank}")
            ]
            super().__init__(placeholder="Ay! (Select an item to buy!)", options=self.selectOptions)

        async def callback(self, interaction: nextcord.Interaction):
            await interaction.edit(view=Selections.MarketSelection.ShopDropdown(self.client))

            # ZAPFISH
            if self.values[0] == self.market[0]:

                # region ZAPFISH_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item? Its a little expensive..)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region ZAPFISH_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[1]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_ZAPFISH_CHECKS
                if wallet < Costs.zapfish_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.zapfish_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET zapfish = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # CALLIE & MARIE AMIIBO
            if self.values[0] == self.market[1]:

                # region CM_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region CM_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[2]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_CM_CHECKS
                if wallet < Costs.callie_marie_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.callie_marie_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET cm_amiibos = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # PEARL & MARINA AMIIBO
            if self.values[0] == self.market[2]:

                # region PM_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region PM_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[3]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_PM_CHECKS
                if wallet < Costs.pearl_marina_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.pearl_marina_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET pm_amiibos = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # SHOOTERS WEAPON
            if self.values[0] == self.market[3]:

                # region SH_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region SH_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[4]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_SH_CHECKS
                if wallet < Costs.shooters_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.shooters_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET shooters = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # ROLLERS WEAPON
            if self.values[0] == self.market[4]:

                # region RO_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region RO_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[5]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_RO_CHECKS
                if wallet < Costs.rollers_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.rollers_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET rollers = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # SPLATLINGS WEAPON
            if self.values[0] == self.market[5]:

                # region SP_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region SP_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[5]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_SP_CHECKS
                if wallet < Costs.splatlings_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.splatlings_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET splatlings = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # BLASTERS WEAPON
            if self.values[0] == self.market[6]:

                # region BL_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region BL_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[6]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_BL_CHECKS
                if wallet < Costs.blasters_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.blasters_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET blasters = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # BRUSHES WEAPON
            if self.values[0] == self.market[7]:

                # region BR_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region BR_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[7]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_BR_CHECKS
                if wallet < Costs.brushes_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.brushes_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET brushes = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # DUALIES WEAPON
            if self.values[0] == self.market[8]:

                # region DU_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region DU_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[8]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_DU_CHECKS
                if wallet < Costs.dualies_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.dualies_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET dualies = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # CHARGERS WEAPON
            if self.values[0] == self.market[9]:

                # region CH_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region CH_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[9]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_CH_CHECKS
                if wallet < Costs.chargers_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.chargers_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET chargers = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # SLOSHERS WEAPON
            if self.values[0] == self.market[10]:

                # region SL_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region SL_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[10]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_SL_CHECKS
                if wallet < Costs.sloshers_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.sloshers_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET sloshers = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # BRELLAS WEAPON
            if self.values[0] == self.market[11]:

                # region BRE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region BRE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT * FROM inv WHERE user_id = {interaction.user.id}')
                item = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    item = item[8]
                except:
                    wallet = wallet
                    item = item

                # region OTHER_BRE_CHECKS
                if wallet < Costs.brellas_cost * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this item!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.brellas_cost * msg_int, interaction.user.id))
                cursor.execute('UPDATE inv SET brellas = ? WHERE user_id = ?', (item + msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 12K BANK UPGRADE
            if self.values[0] == self.market[12]:

                # region 12K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 12K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_12K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_12k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_12k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 12000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 6K BANK UPGRADE
            if self.values[0] == self.market[13]:

                # region 6K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 6K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_6K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_6k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_6k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 6000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 3K BANK UPGRADE
            if self.values[0] == self.market[14]:

                # region 3K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 3K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_3K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_3k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_3k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 3000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 96k BANK UPGRADE
            if self.values[0] == self.market[15]:

                # region 96K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 96K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_96K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_96k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_96k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 96000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 48k BANK UPGRADE
            if self.values[0] == self.market[16]:

                # region 48K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 48K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_48K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_48k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_48k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 48000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

            # 24k BANK UPGRADE
            if self.values[0] == self.market[17]:

                # region 24K_UPGRADE_CHECK
                await interaction.send(f"Ay? ({interaction.user.mention} Are you sure you want to pay for this item?)")

                def check(m):
                    return m.author == interaction.user and m.channel == interaction.channel

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                if response.content.lower() not in ("yes", "y"):
                    await interaction.send("Ay! (Got it! No business is happening right now!)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                await interaction.send(f"Ay? (How many?)")

                try:
                    response = await self.client.wait_for('message', check=check, timeout=30)
                except asyncio.TimeoutError:
                    return await interaction.send('Ay.. (Sorry, you took too long to respond.. Carrying on!)')

                try:
                    msg_int = int(response.content)
                except ValueError:
                    return await interaction.send("Ay.. (Something went wrong.. is that a number?)")

                if msg_int < 1:
                    await interaction.send("Ay.. (You must at least buy more than one..")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                if msg_int > 500:
                    await interaction.send("Ay.. (500 is the limit for buying items..)")
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return

                # endregion

                # region 24K_UPGRADE_DB_CONNECTION

                db = sqlite3.connect('curr.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT max_bank FROM curr WHERE user_id = {interaction.user.id}')
                max_bank = cursor.fetchone()
                cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {interaction.user.id}')
                wallet = cursor.fetchone()

                # endregion

                # noinspection PyBroadException
                try:
                    wallet = wallet[0]
                    max_bank = max_bank[0]
                except:
                    wallet = wallet
                    max_bank = max_bank

                # region OTHER_24K_UPGRADE_CHECKS
                if wallet < Costs.max_upgrade_24k * msg_int:
                    await interaction.send("Ay!? (You don't have enough BMD for this upgrade!? I can't sell it to you..)")
                    cursor.close()
                    db.close()
                    await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))
                    return
                # endregion

                cursor.execute('UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet - Costs.max_upgrade_24k * msg_int, interaction.user.id))
                cursor.execute('UPDATE curr SET max_bank = ? WHERE user_id = ?', (max_bank + 24000 * msg_int, interaction.user.id))
                db.commit()

                await interaction.send('Ay! (Glad doing business!)')
                cursor.close()
                db.close()

                await interaction.edit_original_message(content=" ", view=Selections.MarketSelection.ShopDropdown(self.client))

        class ShopDropdown(nextcord.ui.View):
            def __init__(self, client):
                self.client = client
                super().__init__()
                self.add_item(Selections.MarketSelection(self.client))


# noinspection SpellCheckingInspection
class Paginations:
    class GlobalPageSource(menus.ListPageSource):
        def __init__(self, data):
            super().__init__(data, per_page=1)

        async def format_page(self, menu, entries):
            return entries

        # noinspection SpellCheckingInspection
        class GlobalButtonMenu(menus.ButtonMenuPages, inherit_buttons=False):
            def __init__(self, source):
                super().__init__(source)

                self.add_item(menus.MenuPaginationButton(emoji=self.FIRST_PAGE))
                self.add_item(menus.MenuPaginationButton(emoji=self.PREVIOUS_PAGE))
                self.add_item(menus.MenuPaginationButton(emoji=self.STOP))
                self.add_item(menus.MenuPaginationButton(emoji=self.NEXT_PAGE))
                self.add_item(menus.MenuPaginationButton(emoji=self.LAST_PAGE))

                self._disable_unavailable_buttons()
