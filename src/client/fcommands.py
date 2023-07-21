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
async def command_error_message(interaction, error):
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
        await command_error_message(interaction = interaction, error = error)

    ### MODERATION COMMANDS ###

    ## TIMEOUT ##
    @bot.tree.command(name="ftimeout")
    @app_commands.describe(member = "Usuario", time = "Tiempo en minutos", reason = "Motivo")
    @is_owner()
    async def ftimeout(interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Silenciado**", type = "rich")
        msg.add_field(name = f"El usuario {member.global_name}(@{member.display_name}) ha sido silenciado", value = f"Motivo: {reason} \nTiempo: {time} minuto(s)")
        msg.set_thumbnail(url= "attachment://timeout.png")

        await member.timeout(timedelta(minutes = time), reason = reason)
        await interaction.response.send_message(file = discord.File("res/icons/timeout.png", filename= "timeout.png"), embed = msg)
    ## ERROR ##
    @ftimeout.error
    async def ftimeout_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## KICK ##
    @bot.tree.command(name="fkick")
    @app_commands.describe(member = "Usuario", reason = "Motivo")
    @is_owner()
    async def fkick(interaction: discord.Interaction, member: discord.Member, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Expulsado**", type = "rich")
        msg.add_field(name = f"El usuario {member.global_name}(@{member.display_name}) ha sido expulsado", value = f"Motivo: {reason}")
        msg.set_thumbnail(url= "attachment://kick.png")
        
        await member.send(file = discord.File("res/icons/kick.png", filename= "kick.png"), embed = msg)
        await member.kick(reason = reason)
        await interaction.response.send_message(file = discord.File("res/icons/kick.png", filename= "kick.png"), embed = msg)
    ## ERROR ##
    @fkick.error
    async def fkick_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## BAN ##
    @bot.tree.command(name="fban")
    @app_commands.describe(member= "Usuario", reason= "Motivo", time = "Tiempo en dias")
    @is_owner()
    @commands.has_permissions(ban_members=True)
    async def fban(interaction: discord.Interaction, member: discord.Member, time: int, reason: str):
        msg = discord.Embed(colour = discord.Colour.red(), title = "**Usuario Baneado**", type = "rich")
        msg.add_field(name = f"El usuario {member.global_name}(@{member.display_name}) ha sido baneado", value = f"Motivo: {reason} \nTiempo: {time} dia(s)")
        msg.set_thumbnail(url= "attachment://ban.png")

        await member.send(file = discord.File("res/icons/ban.png", filename= "ban.png"), embed = msg)
        await member.ban(reason = reason)
        await interaction.response.send_message(file = discord.File("res/icons/ban.png", filename= "ban.png"), embed = msg)
    ## ERROR ##
    @fban.error
    async def fban_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## WARN ##
    @bot.tree.command(name="fwarn")
    @app_commands.describe(member = "Usuario", reason = "Motivo")
    @is_owner()
    async def fwarn(interaction: discord.Interaction, member: discord.Member, reason: str):
        msg = discord.Embed(colour = discord.Colour.dark_orange(), title = "**Warn**", type = "rich")
        msg.add_field(name = f"Advertencia para el usuario {member.global_name}(@{member.display_name})", value = f"Motivo: {reason}")
        msg.set_thumbnail(url = "attachment://warn.png")
        
        await member.send(file = discord.File("res/icons/warn.png", filename= "warn.png"), embed = msg)
        await interaction.response.send_message(file = discord.File("res/icons/warn.png", filename= "warn.png"), embed = msg, ephemeral = True)
    ## ERROR ##
    @fwarn.error
    async def fwarn_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)



