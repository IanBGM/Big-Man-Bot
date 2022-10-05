import datetime
import time

import nextcord
import External
from nextcord.ext import commands
from External import Colors

start_time = time.time()


class Common(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(usage="ay")
    async def ay(self, ctx):
        """Ay!"""
        await ctx.reply("Ay! (Ay!)", mention_author=False)

    @commands.command(usage='help')
    async def help(self, ctx):
        """This isn't the right command!"""
        await ctx.send("Ay! (This isn't the right command! Please use `assistance` instead!)")

    @commands.command(aliases=['assist', 'commands', 'cmds'], usage="assistance")
    async def assistance(self, ctx: commands.Context):
        """Help on all my command names!"""

        assistanceEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Assistance!)",
                                         description="*Ay? (Need some help with that?)*", timestamp=ctx.message.created_at)

        assistanceEmbed.add_field(name="Ay (Common)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Common"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Management)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Management"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Entertainment)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Entertainment"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Economy)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Economy"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Leveling)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Leveling"))) + "\n```")
        assistanceEmbed.add_field(name="Ay (Holder)", value="```\n" + " \n".join(map(str, External.get_commands(self.client, "Holder"))) + "\n```")

        try:
            await ctx.author.send(embed=assistanceEmbed)
            await ctx.message.add_reaction(f"{External.Emojis.big_man_icon}")
            await ctx.reply("Ay! (I messaged you my commands!)", mention_author=False)
        except nextcord.Forbidden:
            await ctx.reply("Ay.. (I can't DM you.. are your DMs disabled?)")

    @commands.command(aliases=["cmd"], usage="command <name>")
    async def command(self, ctx, *, name):
        """Get further assistance on commands!"""
        command = self.client.get_command(name)

        if command is None:
            return await ctx.send("Ay.. (I can't find that command in my code..)")

        commandEmbed = nextcord.Embed(color=Colors.dark_grey, title="Ay! (Command Assistance!)", timestamp=ctx.message.created_at)
        commandEmbed.add_field(
            name=f"Ay ({command.name} Command)",
            value=f"*Ay!* ```\n({command.help})\n```\n*Ay!* ```\n({command.usage})\n```\n*Ay!* ```\n({', '.join(command.aliases)})\n```"
        )

        await ctx.send(embed=commandEmbed)

    @commands.command(aliases=['running'], usage='uptime')
    async def uptime(self, ctx):
        """Shows how long I've been running!"""
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))

        await ctx.send(f"Ay! (My Uptime is: **{text}**!)")

    @commands.command(name='server-info', aliases=['guild-info', 'si'], usage='server-info [guild]')
    async def server_info(self, ctx: commands.Context, guild: nextcord.Guild = None):
        """Sends info on the current server!"""
        if guild is None:
            guild = ctx.guild

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

        serverEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=ctx.message.created_at,
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
        await ctx.send(embed=serverEmbed)

    @commands.command(name='user-info', aliases=['member-info', 'ui'], usage='user-info [member]')
    async def user_info(self, ctx: commands.Context, member: nextcord.Member = None):
        """Sends info on the user!"""
        if member is None:
            member = ctx.author

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
            userEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=ctx.message.created_at,
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
            userEmbed = nextcord.Embed(color=Colors.dark_grey, timestamp=ctx.message.created_at,
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
        await ctx.send(embed=userEmbed)

    @commands.command(usage='emoji <emoji>')
    async def emoji(self, ctx, emoji: nextcord.Emoji):
        """Get info on an emoji!"""

        emoji = await emoji.guild.fetch_emoji(emoji.id)

        emojiEmbed = nextcord.Embed(title=f"Ay! (\"{emoji.name}\" Information!)", color=Colors.dark_grey, timestamp=ctx.message.created_at,
                                    description=f"Ay \n```(\n"
                                                f"Name : \"{emoji.name}\"\n"
                                                f"Guild : \"{emoji.guild.name}\"\n"
                                                f"Uploaded By : \"{emoji.user.name + emoji.user.discriminator}\"\n"
                                                f"Creation Time : {emoji.created_at.strftime('%b %d, %Y, %T')}\n)\n```")
        emojiEmbed.set_footer(text=f"Ay! (ID: {emoji.id}!)")
        await ctx.send(embed=emojiEmbed)

    # @commands.command(aliases=['servers', 'count'], usage='guilds')
    # async def guilds(self, ctx):
    #     """Sends guild count for me!"""
    #     return await ctx.send(f"Ay! (I'm currently in **{len(self.client.guilds)} guild(s)**!)")

    async def cog_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f'Ay!? (This command is missing arguments!? Use `manta cmd` to get arguments on commands!)')

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f'Ay!? (This command needs to cooldown!? Try in {round(error.retry_after, 2)} seconds)')

        if isinstance(error, commands.GuildNotFound):
            return await ctx.send("Ay!? (Where is this mystery place!? I don't think I've been there before..)")

        if isinstance(error, commands.EmojiNotFound):
            return await ctx.send("Ay.. (I couldn't find that emoji..)")

        await ctx.send(f"Ay.. (An error has occurred in my Common Code.. I have sent the error out for assistance.)")

        occurredEmbed = nextcord.Embed(color=Colors.dark_grey,
                                       title="Ay.. (An error has occurred in my Common Code..)", timestamp=ctx.message.created_at)
        occurredEmbed.add_field(name="Ay..! (Error Message!)",
                                value=f"*Ay..!?* ```py\n({error})\n```\n*Ay! (Error was in `{ctx.invoked_with}` command!)*", inline=False)
        occurredEmbed.add_field(name="Ay..! (Occurred Where!)",
                                value=f"*[Ay! (**{ctx.guild.name}**)]({await ctx.channel.create_invite()})*", inline=False)

        await self.client.get_channel(1024070867057123399).send(embed=occurredEmbed)


def setup(client):
    client.add_cog(Common(client))
