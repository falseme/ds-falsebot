from client.fbot import FalseBot
import discord
from discord import app_commands
from discord.ext import commands

from datetime import timedelta

### CONDITIONALS ###

## SERVER OWNER ##
def is_owner():
    def predicate(interaction: discord.Interaction):
        if(interaction.user.id == interaction.guild.owner_id):
            return True
        return False
    return app_commands.check(predicate)

### FUNCTIONS ###
async def error_message_not_enough_permisions(interaction, error):
    await interaction.response.send_message(f"[!!] No es posible ejecutar este comando [!!] ({error.__cause__})", ephemeral=True)

def loadcommands(bot: FalseBot):

    ### TEST COMMANDS ###

    ## TEST WELCOME ##
    @bot.tree.command(name="testwelcome")
    @is_owner()
    async def testwelcome(interaction: discord.Interaction):
        await interaction.response.send_message("Testing welcome command", ephemeral=True)
        await bot.welcome_member(interaction.user)
    ## ERROR ##
    @testwelcome.error
    async def testwelcome_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)

    ### MODERATION COMMANDS ###

    ## TIMEOUT ##
    @bot.tree.command(name="ftimeout")
    @app_commands.describe(member = "Usuario", time = "Tiempo en minutos", reason = "Motivo")
    @is_owner()
    async def ftimeout(interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Silenciado**", type = "rich")
        msg.add_field(name = f"El usuario __{member.global_name}__ ha sido silenciado", value = f"Motivo: {reason} \nTiempo: {time} minuto(s)")
        msg.set_thumbnail(url= member.display_avatar.url)

        await member.timeout(timedelta(minutes = time))
        await interaction.response.send_message(embed = msg)
    ## ERROR ##
    @ftimeout.error
    async def ftimeout_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)

    ## KICK ##
    @bot.tree.command(name="fkick")
    @app_commands.describe(member = "Usuario", reason = "Motivo")
    @is_owner()
    async def fkick(interaction: discord.Interaction, member: discord.Member, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Expulsado**", type = "rich")
        msg.add_field(name = f"El usuario __{member.global_name}__ ha sido expulsado", value = f"Motivo: {reason}")
        msg.set_thumbnail(url= member.display_avatar.url)

        await member.kick()
        await interaction.response.send_message(embed = msg)
    ## ERROR ##
    @fkick.error
    async def fkick_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)

    ## BAN ##
    @bot.tree.command(name="fban")
    @app_commands.describe(member= "Usuario", reason= "Motivo", time = "Tiempo en dias")
    @is_owner()
    @commands.has_permissions(ban_members=True)
    async def fban(interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Baneado**", type = "rich")
        msg.add_field(name = f"El usuario __{member.global_name}__ ha sido baneado", value = f"Motivo: {reason} \nTiempo: {time} dia(s)")
        msg.set_thumbnail(url= member.display_avatar.url)

        await member.ban()
        await interaction.response.send_message(embed = msg)
    ## ERROR ##
    @fban.error
    async def fban_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)



