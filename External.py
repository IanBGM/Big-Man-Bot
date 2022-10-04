import asyncio
import sqlite3

import nextcord
from PIL import ImageFont
from nextcord.ext import commands


class Variables:
    owner_id = 972050344160931880
    guild_ids = [974813796285685811]
    # 100k
    initial_bank_capacity = 5000
    # initial_bank_capacity_text = "100,000"


class Colors:
    dark_grey = 0xa9a9a9


# noinspection SpellCheckingInspection
class Emojis:
    # OTHER
    lil_judd = "<a:lil_judd:1024468316686930010>"
    judd = "<a:judd:1024468313977401425>"
    dancing_man = '<a:dancingman:1024493790205055067>'
    something_man = "<a:somethingman:1024493783645175839>"
    big_man_bank = "<:big_man_bank:1025997402387267664>"
    big_man_icon = "<:big_man_icon:1026099362897604718>"
    # MARKET
    zapfish_replica = "<:zapfish_replica:1025264884209963088>"
    callie_marie_amiibos = "<:callie_marie_amiibos:1026115652597059584>"
    pearl_marina_amiibos = "<:pearl_marina_amiibos:1026431451723472946>"
    # WEAPONS
    shooters = "<:shooters:1026857432883925054>"
    rollers = "<:rollers:1026857431860510850>"
    splatlings = "<:splatlings:1026857430698696744>"
    blasters = "<:blasters:1026857429608189962>"
    brushes = "<:brushes:1026857428702208071>"
    dualies = "<:dualies:1026857424264646656>"
    chargers = "<:chargers:1026857427641057390>"
    sloshers = "<:sloshers:1026857425405481052>"
    brellas = "<:brellas:1026857426558922834>"


# noinspection SpellCheckingInspection
class Fonts:
    @staticmethod
    def set_splatfont(size):
        splatfont = ImageFont.truetype("assets/fonts/splatfont.ttf", size=size)
        return splatfont

    @staticmethod
    def set_splatfont2(size):
        splatfont2 = ImageFont.truetype("assets/fonts/splatfont2.ttf", size=size)
        return splatfont2


# noinspection SpellCheckingInspection
class Costs:
    zapfish_cost = 100000  # 100k
    callie_marie_cost = 2200  # 2.2k
    pearl_marina_cost = 2400  # 2.4k

    shooters_cost = 500  # 500
    rollers_cost = 800  # 800
    splatlings_cost = 1100  # 1100
    blasters_cost = 1400  # 1400
    brushes_cost = 1700  # 1700
    dualies_cost = 2000  # 2000
    chargers_cost = 2300  # 2300
    sloshers_cost = 2600  # 2600
    brellas_cost = 2900  # 2900

    max_upgrade_12k = 12000  # 12k
    max_upgrade_6k = 6000  # 6k
    max_upgrade_3k = 3000  # 3k
    max_upgrade_96k = 96000  # 96k
    max_upgrade_48k = 48000  # 48k
    max_upgrade_24k = 24000  # 24k


def get_commands(client, cog):
    cmds = []
    for y in client.commands:
        if y.cog and y.cog.qualified_name == cog:
            cmds.append(y.name)
    if "help" in cmds:
        cmds.remove("help")
    if "request" not in cmds and cog == "Common":
        cmds.append("request")
    if "bug" not in cmds and cog == "Common":
        cmds.append("bug")
    return cmds


def block_check(code):
    if code.startswith("`") and code.endswith("`"):
        return " ".join(code.split(" ")).replace('`', "")

    return code


async def paginate(client: commands.Bot, ctx: commands.Context | nextcord.Interaction, author, embeds: list[nextcord.Embed], selection: nextcord.ui.View = None, market: bool = False):
    buttons = ["⏪", "⬅", "⏹", "➡", "⏩"]
    current = 0

    if market:
        msg = await ctx.send(embed=embeds[current], view=selection)
    else:
        msg = await ctx.send(embed=embeds[current])

    # noinspection PyBroadException
    try:
        message = await msg.fetch()
    except AttributeError:
        message = msg

    for button in buttons:
        await message.add_reaction(button)

    while True:
        react, user = await client.wait_for("reaction_add", check=lambda reaction, member: member == author and reaction.message == msg and reaction.emoji in buttons)

        previous_page = current
        if react.emoji == "⏪":
            current = 0

        elif react.emoji == "⬅":
            if current > 0:
                current -= 1

        elif react.emoji == "⏹":
            for button in buttons:
                await message.remove_reaction(button, author)
            return await message.edit(content="Ay! (Cancelled Marketplace View!)", embed=None, view=None)

        elif react.emoji == "➡":
            if current < len(embeds) - 1:
                current += 1

        elif react.emoji == "⏩":
            current = len(embeds) - 1

        for button in buttons:
            await message.remove_reaction(button, author)

        if current != previous_page:
            await message.edit(embed=embeds[current])


# noinspection SpellCheckingInspection
async def set_inv(member: nextcord.Member, author, created_at, ctx):
    if member is None:
        member = author

    db = sqlite3.connect('curr.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
    enabled = cursor.fetchone()
    if enabled and not enabled[0]:
        return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

    # noinspection SpellCheckingInspection
    cursor.execute(f'SELECT * FROM inv WHERE user_id = {member.id}')
    data = cursor.fetchone()

    # noinspection PyBroadException
    try:
        # noinspection SpellCheckingInspection
        zapfish = data[1]
        cm_amiibos = data[2]
        pm_amiibos = data[3]
        shooters = data[4]
        rollers = data[5]
        splatlings = data[6]
        blasters = data[7]
        brushes = data[8]
        dualies = data[9]
        chargers = data[10]
        sloshers = data[11]
        brellas = data[12]
    except:
        # noinspection SpellCheckingInspection
        zapfish = 0
        cm_amiibos = 0
        pm_amiibos = 0
        shooters = 0
        rollers = 0
        splatlings = 0
        blasters = 0
        brushes = 0
        dualies = 0
        chargers = 0
        sloshers = 0
        brellas = 0

    # noinspection SpellCheckingInspection
    invEmbed = nextcord.Embed(title=f'Ay! ({member.name} Inventory!)', color=Colors.dark_grey, timestamp=created_at,
                              description=f'''\n
                            {Emojis.zapfish_replica} **Great Zapfish Replica (Statue)** - `x{zapfish}`\n
                            {Emojis.callie_marie_amiibos} **Callie & Marie (Amiibo)** - `x{cm_amiibos}`\n
                            {Emojis.pearl_marina_amiibos} **Pearl & Marina (Amiibo)** - `x{pm_amiibos}`\n
                            {Emojis.shooters} **Shooters (Weapon)** - `x{shooters}`\n
                            {Emojis.rollers} **Rollers (Weapon)** - `x{rollers}`\n
                            {Emojis.splatlings} **Splatlings (Weapon)** - `x{splatlings}`\n
                            {Emojis.blasters} **Blasters (Weapon)** - `x{blasters}`\n
                            {Emojis.brushes} **Brushes (Weapon)** - `x{brushes}`\n
                            {Emojis.dualies} **Dualies (Weapon)** - `x{dualies}`\n
                            {Emojis.chargers} **Chargers (Weapon)** - `x{chargers}`\n
                            {Emojis.sloshers} **Sloshers (Weapon)** - `x{sloshers}`\n
                            {Emojis.brellas} **Brellas (Weapon)** - `x{brellas}`\n
                        ''')

    await ctx.send(embed=invEmbed)
    cursor.close()
    db.close()


# noinspection SpellCheckingInspection
def set_shop(created_at, inline=False):
    # embed = nextcord.Embed(
    #     title='Ay! (Big Man\'s Marketplace!)',
    #     color=Colors.dark_grey,
    #     timestamp=created_at
    # )

    # region ITEM_EMBED_1

    itemEmbed1 = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    # noinspection SpellCheckingInspection
    itemEmbed1.add_field(
        name=f"{Emojis.zapfish_replica} Ay ( Great Zapfish Replica (Statue) : 100k BMD )",
        value=f'''*Ay (The Great Zapfish.. but as a collectible statue! Worth a lot of BMD if you ask me..)*
                \n**ID** : *BMM_G_ZAPFISH*\n**Worth** : *{round(Costs.zapfish_cost * 4 / 5)} BMD* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    itemEmbed1.add_field(
        name=f"{Emojis.callie_marie_amiibos} Ay ( Callie & Marie (Amiibo) : 2.2k BMD )",
        value=f'''*Ay (The rare Callie & Marie amiibos! Automatically used in-turf and tilts the chances to always win!)*
                \n**ID** : *BMM_CM_AMIIBOS*\n**Worth** : *{round(Costs.callie_marie_cost * 4 / 5)} BMD* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    itemEmbed1.add_field(
        name=f"{Emojis.pearl_marina_amiibos} Ay ( Pearl & Marina (Amiibo) : 2.4k BMD )",
        value=f'''*Ay (The rare Pearl & Marina amiibos! Automatically used in-blitz and tilts the chances to always win!)*
                \n**ID** : *BMM_PM_AMIIBOS*\n**Worth** : *{round(Costs.pearl_marina_cost * 4 / 5)} BMD* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    # endregion

    # region ITEM_EMBED_2

    itemEmbed2 = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    # noinspection SpellCheckingInspection
    itemEmbed2.add_field(
        name=f"{Emojis.shooters} Shooters (Weapon) | 500 BMD",
        value=f'''*Shooters! This will give you a shooters-type weapon that adds 5+ to the percentage in-turf! (Blitz not supported)*
                \n**ID** : *BMM_SHOOTERS*\n**Worth** : *{round(Costs.shooters_cost * 4 / 5)} BMD* \n**Seller** : *BaseInkling ✓*
        ''',
        inline=inline
    )

    itemEmbed2.add_field(
        name=f"{Emojis.rollers} Rollers (Weapon) | 800 BMD",
        value=f'''*Rollers! This will give you a rollers-type weapon that adds 8+ to the percentage in-turf! (Blitz not supported)*
                \n**ID** : *BMM_ROLLERS*\n**Worth** : *{round(Costs.rollers_cost * 4 / 5)} BMD* \n**Seller** : *BaseInkling ✓*
        ''',
        inline=inline
    )

    itemEmbed2.add_field(
        name=f"{Emojis.splatlings} Splatlings (Weapon) - 1100 BMD",
        value=f'''*Splatlings can give up to 10+ percentage in-turf. This also doesn't work with blitz..*
                \n**ID** : *BMM_SPLATLINGS*\n**Worth** : *{round(Costs.splatlings_cost * 4 / 5)} BMD* \n**Seller** : *SleekSplats*
        ''',
        inline=inline
    )

    # endregion

    # region ITEM_EMBED_3

    itemEmbed3 = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    # noinspection SpellCheckingInspection
    itemEmbed3.add_field(
        name=f"{Emojis.blasters} Blasters (Weapon) - 1400 BMD",
        value=f'''*Blasters can give up to 12+ percentage in-turf. This also doesn't work with blitz..*
                \n**ID** : *BMM_BLASTERS*\n**Worth** : *{round(Costs.blasters_cost * 4 / 5)} BMD* \n**Seller** : *SleekSplats*
        ''',
        inline=inline
    )

    itemEmbed3.add_field(
        name=f"{Emojis.brushes} Brushes (Weapon) - 1700 BMD",
        value=f'''*Brushes can give up to 14+ percentage in-turf. This also doesn't work with blitz..*
                \n**ID** : *BMM_BRUSHES*\n**Worth** : *{round(Costs.brushes_cost * 4 / 5)} BMD* \n**Seller** : *SleekSplats*
        ''',
        inline=inline
    )

    itemEmbed3.add_field(
        name=f"{Emojis.dualies} Dualies (Weapon) [2000 BMD]",
        value=f'''*Get some dualies! Used in-turf and boost up your percentage to about 17+ percentage! [DON'T USE ON BLITZ]*
                \n**ID** : *BMM_DUALIES*\n**Worth** : *{round(Costs.dualies_cost * 4 / 5)} BMD* \n**Seller** : *CozyOctoling ✓*
        ''',
        inline=inline
    )

    # endregion

    # region ITEM_EMBED_4

    itemEmbed4 = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    # noinspection SpellCheckingInspection
    itemEmbed4.add_field(
        name=f"{Emojis.chargers} Chargers (Weapon) [2300 BMD]",
        value=f'''*Get some chargers! Used in-turf and boost up your percentage to about 20+ percentage! [DON'T USE ON BLITZ]*
                \n**ID** : *BMM_CHARGERS*\n**Worth** : *{round(Costs.chargers_cost * 4 / 5)} BMD* \n**Seller** : *CozyOctoling ✓*
        ''',
        inline=inline
    )

    itemEmbed4.add_field(
        name=f"{Emojis.sloshers} Sloshers (Weapon) | 2600 BMD",
        value=f'''*Sloshers! This will give you a sloshers-type weapon that adds 22+ to the percentage in-turf! (Blitz not supported)*
                \n**ID** : *BMM_SLOSHERS*\n**Worth** : *{round(Costs.sloshers_cost * 4 / 5)} BMD* \n**Seller** : *BaseInkling ✓*
        ''',
        inline=inline
    )

    itemEmbed4.add_field(
        name=f"{Emojis.brellas} Brellas (Weapon) [2900 BMD]",
        value=f'''*Get some brellas! Used in-turf and boost up your percentage to about 25+ percentage! [DON'T USE ON BLITZ]*
                \n**ID** : *BMM_BRELLAS*\n**Worth** : *{round(Costs.brellas_cost * 4 / 5)} BMD* \n**Seller** : *CozyOctoling ✓*
        ''',
        inline=inline
    )

    # endregion

    # region BIG_MAN_BANK_UPGRADE

    bankUpgradeEmbed = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    bankUpgradeEmbed.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (12k) : 12k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 12k to your current bank capacity.)*
                \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    bankUpgradeEmbed.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (6k) : 6k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 6k to your current bank capacity.)*
                \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    bankUpgradeEmbed.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (3k) : 3k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 3k to your current bank capacity.)*
                \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
        ''',
        inline=inline
    )

    # endregion

    # region BIG_MAN_BANK_UPGRADE_2

    bankUpgradeEmbed2 = nextcord.Embed(
        title='Ay! (Big Man\'s Marketplace!)',
        color=Colors.dark_grey,
        timestamp=created_at
    )

    bankUpgradeEmbed2.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (96k) : 96k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 96k to your current bank capacity.)*
                    \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
            ''',
        inline=inline
    )

    bankUpgradeEmbed2.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (48k) : 48k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 48k to your current bank capacity.)*
                    \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
            ''',
        inline=inline
    )
    
    bankUpgradeEmbed2.add_field(
        name=f"{Emojis.big_man_bank} Ay ( Big Man Bank Upgrade (24k) : 24k BMD )",
        value=f'''*Ay (Upgrade your bank capacity! This will add 24k to your current bank capacity.)*
                    \n**ID** : *Upgrades do not have a specific ID.*\n**Worth** : *Upgrades do not have a specific worth.* \n**Seller** : *Big Man ✓*
            ''',
        inline=inline
    )

    # endregion

    embeds = [itemEmbed1, itemEmbed2, itemEmbed3, itemEmbed4, bankUpgradeEmbed, bankUpgradeEmbed2]

    return embeds


# noinspection PyBroadException
# noinspection SpellCheckingInspection
async def gift_check(item_id: str, ctx, author, member: nextcord.Member, amount: int, client: commands.Bot):
    db = sqlite3.connect('curr.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
    enabled = cursor.fetchone()
    if enabled and not enabled[0]:
        return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

    item_ids = [
        'BMM_G_ZAPFISH',
        'BMM_CM_AMIIBOS',
        'BMM_PM_AMIIBOS',
        'BMM_SHOOTERS',
        'BMM_ROLLERS',
        'BMM_SPLATLINGS',
        'BMM_BLASTERS',
        'BMM_BRUSHES',
        'BMM_DUALIES',
        'BMM_CHARGERS',
        'BMM_SLOSHERS',
        'BMM_BRELLAS'
    ]
    item_names = [
        "Great Zapfish Replica (Statue)",
        "Callie & Marie (Amiibo)",
        "Pearl & Marina (Amiibo)",
        "Shooters (Weapon)",
        "Rollers (Weapon)",
        "Splatlings (Weapon)",
        "Blasters (Weapon)",
        "Brushes (Weapon)",
        "Dualies (Weapon)",
        "Chargers (Weapon)",
        "Sloshers (Weapon)",
        "Brellas (Weapon)"
    ]

    if member == client.user:
        return await ctx.send('Ay!? (I can\'t accept this gift!)')

    if member.bot:
        return await ctx.send('Ay!? (They can\'t accept this gift!)')

    if item_id.upper() not in item_ids:
        return await ctx.send('Ay.. (I couldn\'t find that one.. Maybe your item id is wrong?)')

    # region ZAPFISH

    cursor.execute(f'SELECT zapfish FROM inv WHERE user_id = {member.id}')
    zapfish = cursor.fetchone()

    try:
        zapfish = zapfish[0]
    except:
        zapfish = zapfish

    if zapfish is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[0]:
        cursor.execute(f'SELECT zapfish FROM inv WHERE user_id = {author.id}')
        authorZapfish = cursor.fetchone()

        if authorZapfish is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorZapfish[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET zapfish = ? WHERE user_id = ?', (authorZapfish[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET zapfish = ? WHERE user_id = ?', (zapfish + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[0]}` to {member.mention}!)")

    # endregion

    # region CALLIE_MARIE_AMIIBO

    cursor.execute(f'SELECT cm_amiibos FROM inv WHERE user_id = {member.id}')
    cm_amiibos = cursor.fetchone()

    try:
        cm_amiibos = cm_amiibos[0]
    except:
        cm_amiibos = cm_amiibos

    if cm_amiibos is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[1]:
        cursor.execute(f'SELECT cm_amiibos FROM inv WHERE user_id = {author.id}')
        authorCMAmiibos = cursor.fetchone()

        if authorCMAmiibos is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorCMAmiibos[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET cm_amiibos = ? WHERE user_id = ?', (authorCMAmiibos[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET cm_amiibos = ? WHERE user_id = ?', (cm_amiibos + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[1]}` to {member.mention}!)")

    # endregion

    # region PEARL_MARINA_AMIIBO

    cursor.execute(f'SELECT pm_amiibos FROM inv WHERE user_id = {member.id}')
    pm_amiibos = cursor.fetchone()

    try:
        pm_amiibos = pm_amiibos[0]
    except:
        pm_amiibos = pm_amiibos

    if pm_amiibos is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[2]:
        cursor.execute(f'SELECT pm_amiibos FROM inv WHERE user_id = {author.id}')
        authorPMAmiibos = cursor.fetchone()

        if authorPMAmiibos is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorPMAmiibos[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET pm_amiibos = ? WHERE user_id = ?', (authorPMAmiibos[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET pm_amiibos = ? WHERE user_id = ?', (pm_amiibos + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[2]}` to {member.mention}!)")

    # endregion

    # region SHOOTERS

    cursor.execute(f'SELECT shooters FROM inv WHERE user_id = {member.id}')
    shooters = cursor.fetchone()

    try:
        shooters = shooters[0]
    except:
        shooters = shooters

    if shooters is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[3]:
        cursor.execute(f'SELECT shooters FROM inv WHERE user_id = {author.id}')
        authorShooters = cursor.fetchone()

        if authorShooters is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorShooters[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET shooters = ? WHERE user_id = ?', (authorShooters[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET shooters = ? WHERE user_id = ?', (shooters + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[3]}` to {member.mention}!)")

    # endregion

    # region ROLLERS

    cursor.execute(f'SELECT rollers FROM inv WHERE user_id = {member.id}')
    rollers = cursor.fetchone()

    try:
        rollers = rollers[0]
    except:
        rollers = rollers

    if rollers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[4]:
        cursor.execute(f'SELECT rollers FROM inv WHERE user_id = {author.id}')
        authorRollers = cursor.fetchone()

        if authorRollers is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorRollers[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET rollers = ? WHERE user_id = ?', (authorRollers[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET rollers = ? WHERE user_id = ?', (rollers + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[4]}` to {member.mention}!)")

    # endregion

    # region SPLATLINGS

    cursor.execute(f'SELECT splatlings FROM inv WHERE user_id = {member.id}')
    splatlings = cursor.fetchone()

    try:
        splatlings = splatlings[0]
    except:
        splatlings = splatlings

    if splatlings is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[5]:
        cursor.execute(f'SELECT splatlings FROM inv WHERE user_id = {author.id}')
        authorSplatlings = cursor.fetchone()

        if authorSplatlings is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorSplatlings[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET splatlings = ? WHERE user_id = ?', (authorSplatlings[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET splatlings = ? WHERE user_id = ?', (splatlings + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[5]}` to {member.mention}!)")

    # endregion

    # region BLASTERS

    cursor.execute(f'SELECT blasters FROM inv WHERE user_id = {member.id}')
    blasters = cursor.fetchone()

    try:
        blasters = blasters[0]
    except:
        blasters = blasters

    if blasters is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[6]:
        cursor.execute(f'SELECT blasters FROM inv WHERE user_id = {author.id}')
        authorBlasters = cursor.fetchone()

        if authorBlasters is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorBlasters[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET blasters = ? WHERE user_id = ?', (authorBlasters[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET blasters = ? WHERE user_id = ?', (blasters + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[6]}` to {member.mention}!)")

    # endregion

    # region BRUSHES

    cursor.execute(f'SELECT brushes FROM inv WHERE user_id = {member.id}')
    brushes = cursor.fetchone()

    try:
        brushes = brushes[0]
    except:
        brushes = brushes

    if brushes is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[7]:
        cursor.execute(f'SELECT brushes FROM inv WHERE user_id = {author.id}')
        authorBrushes = cursor.fetchone()

        if authorBrushes is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorBrushes[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET brushes = ? WHERE user_id = ?', (authorBrushes[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET brushes = ? WHERE user_id = ?', (brushes + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[7]}` to {member.mention}!)")

    # endregion

    # region DUALIES

    cursor.execute(f'SELECT dualies FROM inv WHERE user_id = {member.id}')
    dualies = cursor.fetchone()

    try:
        dualies = dualies[0]
    except:
        dualies = dualies

    if dualies is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[8]:
        cursor.execute(f'SELECT dualies FROM inv WHERE user_id = {author.id}')
        authorDualies = cursor.fetchone()

        if authorDualies is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorDualies[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET dualies = ? WHERE user_id = ?', (authorDualies[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET dualies = ? WHERE user_id = ?', (dualies + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[8]}` to {member.mention}!)")

    # endregion

    # region CHARGERS

    cursor.execute(f'SELECT chargers FROM inv WHERE user_id = {member.id}')
    chargers = cursor.fetchone()

    try:
        chargers = chargers[0]
    except:
        chargers = chargers

    if chargers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[9]:
        cursor.execute(f'SELECT chargers FROM inv WHERE user_id = {author.id}')
        authorChargers = cursor.fetchone()

        if authorChargers is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorChargers[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET chargers = ? WHERE user_id = ?', (authorChargers[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET chargers = ? WHERE user_id = ?', (chargers + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[9]}` to {member.mention}!)")

    # endregion

    # region SLOSHERS

    cursor.execute(f'SELECT sloshers FROM inv WHERE user_id = {member.id}')
    sloshers = cursor.fetchone()

    try:
        sloshers = sloshers[0]
    except:
        sloshers = sloshers

    if sloshers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[10]:
        cursor.execute(f'SELECT sloshers FROM inv WHERE user_id = {author.id}')
        authorSloshers = cursor.fetchone()

        if authorSloshers is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorSloshers[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET sloshers = ? WHERE user_id = ?', (authorSloshers[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET sloshers = ? WHERE user_id = ?', (sloshers + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[10]}` to {member.mention}!)")

    # endregion

    # region BRELLAS

    cursor.execute(f'SELECT brellas FROM inv WHERE user_id = {member.id}')
    brellas = cursor.fetchone()

    try:
        brellas = brellas[0]
    except:
        brellas = brellas

    if brellas is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for their inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (member.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[11]:
        cursor.execute(f'SELECT brellas FROM inv WHERE user_id = {author.id}')
        authorBrellas = cursor.fetchone()

        if authorBrellas is None:
            msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
            sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
                  "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            cursor.execute(sql, val)
            db.commit()
            await asyncio.sleep(0.5)
            await msg.edit(content='Ay! (Complete adding new inventory data!)')
            return

        if authorBrellas[0] < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE inv SET brellas = ? WHERE user_id = ?', (authorBrellas[0] - amount, author.id))
        cursor.execute(f'UPDATE inv SET brellas = ? WHERE user_id = ?', (brellas + amount, member.id))
        db.commit()

        await ctx.send(f"Ay! (You've gifted `{amount}x {item_names[11]}` to {member.mention}!)")

    # endregion

    cursor.close()
    db.close()


# noinspection PyBroadException
# noinspection SpellCheckingInspection
async def sell_check(item_id: str, ctx, author, amount: int):
    db = sqlite3.connect('curr.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT enabled FROM system WHERE guild_id = {ctx.guild.id}')
    enabled = cursor.fetchone()
    if enabled and not enabled[0]:
        return await ctx.send('Ay.. (Economy is currently disabled for this server..)')

    item_ids = [
        'BMM_G_ZAPFISH',
        'BMM_CM_AMIIBOS',
        'BMM_PM_AMIIBOS',
        'BMM_SHOOTERS',
        'BMM_ROLLERS',
        'BMM_SPLATLINGS',
        'BMM_BLASTERS',
        'BMM_BRUSHES',
        'BMM_DUALIES',
        'BMM_CHARGERS',
        'BMM_SLOSHERS',
        'BMM_BRELLAS'
    ]
    item_names = [
        "Great Zapfish Replica (Statue)",
        "Callie & Marie (Amiibo)",
        "Pearl & Marina (Amiibo)",
        "Shooters (Weapon)",
        "Rollers (Weapon)",
        "Splatlings (Weapon)",
        "Blasters (Weapon)",
        "Brushes (Weapon)",
        "Dualies (Weapon)",
        "Chargers (Weapon)",
        "Sloshers (Weapon)",
        "Brellas (Weapon)"
    ]

    if item_id.upper() not in item_ids:
        return await ctx.send('Ay.. (I couldn\'t find that one.. Maybe your item id is wrong?)')

    # region ZAPFISH

    cursor.execute(f'SELECT zapfish FROM inv WHERE user_id = {author.id}')
    zapfish = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        zapfish = zapfish[0]
        wallet = wallet[0]
    except:
        zapfish = zapfish
        wallet = wallet

    if zapfish is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[0]:
        if zapfish < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.zapfish_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET zapfish = ? WHERE user_id = ?', (zapfish - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[0]}` for **{round(Costs.zapfish_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region CALLIE_MARIE_AMIIBO

    cursor.execute(f'SELECT cm_amiibos FROM inv WHERE user_id = {author.id}')
    cm_amiibos = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        cm_amiibos = cm_amiibos[0]
        wallet = wallet[0]
    except:
        cm_amiibos = cm_amiibos
        wallet = wallet

    if cm_amiibos is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[1]:
        if cm_amiibos < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.callie_marie_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET cm_amiibos = ? WHERE user_id = ?', (cm_amiibos - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[1]}` for **{round(Costs.callie_marie_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region PEARL_MARINA_AMIIBO

    cursor.execute(f'SELECT pm_amiibos FROM inv WHERE user_id = {author.id}')
    pm_amiibos = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        pm_amiibos = pm_amiibos[0]
        wallet = wallet[0]
    except:
        pm_amiibos = pm_amiibos
        wallet = wallet

    if pm_amiibos is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[2]:
        if pm_amiibos < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.pearl_marina_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET pm_amiibos = ? WHERE user_id = ?', (pm_amiibos - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[2]}` for **{round(Costs.pearl_marina_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region SHOOTERS

    cursor.execute(f'SELECT shooters FROM inv WHERE user_id = {author.id}')
    shooters = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        shooters = shooters[0]
        wallet = wallet[0]
    except:
        shooters = shooters
        wallet = wallet

    if shooters is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[3]:
        if shooters < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.shooters_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET shooters = ? WHERE user_id = ?', (shooters - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[3]}` for **{round(Costs.shooters_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region ROLLERS

    cursor.execute(f'SELECT rollers FROM inv WHERE user_id = {author.id}')
    rollers = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        rollers = rollers[0]
        wallet = wallet[0]
    except:
        rollers = rollers
        wallet = wallet

    if rollers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[4]:
        if rollers < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.rollers_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET rollers = ? WHERE user_id = ?', (rollers - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[4]}` for **{round(Costs.rollers_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region SPLATLINGS

    cursor.execute(f'SELECT splatlings FROM inv WHERE user_id = {author.id}')
    splatlings = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        splatlings = splatlings[0]
        wallet = wallet[0]
    except:
        splatlings = splatlings
        wallet = wallet

    if splatlings is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[5]:
        if splatlings < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.splatlings_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET splatlings = ? WHERE user_id = ?', (splatlings - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[5]}` for **{round(Costs.splatlings_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region BLASTERS

    cursor.execute(f'SELECT blasters FROM inv WHERE user_id = {author.id}')
    blasters = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        blasters = blasters[0]
        wallet = wallet[0]
    except:
        blasters = blasters
        wallet = wallet

    if blasters is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[6]:
        if blasters < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.blasters_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET blasters = ? WHERE user_id = ?', (blasters - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[6]}` for **{round(Costs.blasters_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region BRUSHES

    cursor.execute(f'SELECT brushes FROM inv WHERE user_id = {author.id}')
    brushes = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        brushes = brushes[0]
        wallet = wallet[0]
    except:
        brushes = brushes
        wallet = wallet

    if brushes is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[7]:
        if brushes < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.brushes_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET brushes = ? WHERE user_id = ?', (brushes - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[7]}` for **{round(Costs.brushes_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region DUALIES

    cursor.execute(f'SELECT dualies FROM inv WHERE user_id = {author.id}')
    dualies = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        dualies = dualies[0]
        wallet = wallet[0]
    except:
        dualies = dualies
        wallet = wallet

    if dualies is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[8]:
        if dualies < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.dualies_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET dualies = ? WHERE user_id = ?', (dualies - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[8]}` for **{round(Costs.dualies_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region CHARGERS

    cursor.execute(f'SELECT chargers FROM inv WHERE user_id = {author.id}')
    chargers = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        chargers = chargers[0]
        wallet = wallet[0]
    except:
        chargers = chargers
        wallet = wallet

    if chargers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[9]:
        if chargers < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.chargers_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET chargers = ? WHERE user_id = ?', (chargers - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[9]}` for **{round(Costs.chargers_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region SLOSHERS

    cursor.execute(f'SELECT sloshers FROM inv WHERE user_id = {author.id}')
    sloshers = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        sloshers = sloshers[0]
        wallet = wallet[0]
    except:
        sloshers = sloshers
        wallet = wallet

    if sloshers is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[10]:
        if sloshers < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.sloshers_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET sloshers = ? WHERE user_id = ?', (sloshers - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[10]}` for **{round(Costs.sloshers_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    # region BRELLAS

    cursor.execute(f'SELECT brellas FROM inv WHERE user_id = {author.id}')
    brellas = cursor.fetchone()
    cursor.execute(f'SELECT wallet FROM curr WHERE user_id = {author.id}')
    wallet = cursor.fetchone()

    try:
        brellas = brellas[0]
        wallet = wallet[0]
    except:
        brellas = brellas
        wallet = wallet

    if brellas is None:
        msg = await ctx.send("Ay.. (I can't seem to find any data for your inventory. I will be creating it now.. Try gifting again afterwards!)")
        sql = "INSERT INTO inv (user_id, zapfish, cm_amiibos, pm_amiibos, shooters, rollers, splatlings, blasters, brushes, dualies, chargers, sloshers, brellas) VALUES " \
              "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        val = (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        cursor.execute(sql, val)
        db.commit()
        await asyncio.sleep(0.5)
        await msg.edit(content='Ay! (Complete adding new inventory data!)')
        return

    if item_id.upper() == item_ids[11]:
        if brellas < amount:
            return await ctx.send('Ay.. (You don\'t have enough of this item..)')
        cursor.execute(f'UPDATE curr SET wallet = ? WHERE user_id = ?', (wallet + round(Costs.brellas_cost * 4 / 5 * amount), author.id))
        cursor.execute(f'UPDATE inv SET brellas = ? WHERE user_id = ?', (brellas - amount, author.id))
        db.commit()

        await ctx.send(f"Ay! (You've sold `{amount}x {item_names[11]}` for **{round(Costs.brellas_cost * 4 / 5 * amount)} BMD**!)")

    # endregion

    cursor.close()
    db.close()


async def start_turf(ctx):
    turf_battle = await ctx.send("Ay! (Turf War Begin!)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You ink base..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (Opponent goes straight for the middle..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You get to the middle..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You clash at each others heads..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (The timer is closer to running out..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (10..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (9..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (8..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (7..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (6..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (5..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (4..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (3..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (2..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (1..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay! (Results coming in..!)")
    await asyncio.sleep(1.5)


async def start_turf_extreme(ctx):
    turf_battle = await ctx.send("Ay! (Extreme Turf War Begin!)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You go straight for the middle..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (Opponent goes straight for the middle..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You both clash at each others heads..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You've been splatted 49 times..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (They've been splatted 49 times..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (The final splat before time goes out will determine the winner..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (6..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (5..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (4..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (3..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (2..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (1..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay! (Results coming in..!)")
    await asyncio.sleep(2.5)


async def start_cheat(ctx, member):
    turf_battle = await ctx.send("Ay..? (Cheating Begin..?)")
    await asyncio.sleep(1)
    await turf_battle.edit(content=f"Ay.. (You break into {member.name} home at night..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You hide from the cameras..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content=f"Ay.. ({member.name} wakes up..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You hide until they pass by..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You go to their room..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You grab their wallet..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (Something interesting happens..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (Time is almost out..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (5..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (4..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (3..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (2..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (1..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay..? (Your fate is coming in..?)")
    await asyncio.sleep(1.5)


async def start_blitz(ctx):
    turf_battle = await ctx.send("Ay! (Experience Blitz Begin!)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You ink the area to swim around looking for leftover XP..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (Opponent goes straight for your base..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You splat them, and grab their dropped experience..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (Opponent respawns and starts collecting XP again..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (The timer is closer to running out..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (You create an Experience Ball and throw it into their base defense systems..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (You wonder where your Opponent is, but they've already thrown an Experience Ball into yours as well..)")
    await asyncio.sleep(2)
    await turf_battle.edit(content="Ay.. (The battle goes from there..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (The timer is closer to running out..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (6..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (5..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (4..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (3..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (2..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay.. (1..)")
    await asyncio.sleep(1)
    await turf_battle.edit(content="Ay! (Results coming in..!)")
    await asyncio.sleep(1.5)

# async def start_cheat_bank(ctx, member):
#     turf_battle = await ctx.send("Ay..? (Cheating Begin..?)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (You break into Big Man Bank at night..)")
#     await asyncio.sleep(2)
#     await turf_battle.edit(content="Ay.. (You hide from the guards & cameras..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (Guards hear something..)")
#     await asyncio.sleep(2)
#     await turf_battle.edit(content="Ay.. (You hide until they pass by..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (You go to the backroom with the vault..)")
#     await asyncio.sleep(2)
#     await turf_battle.edit(content="Ay.. (You start unlocking it with your skills..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content=f"Ay.. (You find the one with {member.name} on it..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (Something interesting happens..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (Time is almost out..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (3..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (2..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay.. (1..)")
#     await asyncio.sleep(1)
#     await turf_battle.edit(content="Ay..? (Your fate is coming in..?)")
#     await asyncio.sleep(1.5)
