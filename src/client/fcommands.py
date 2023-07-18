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

### FUNCTION ###
async def error_message_not_enough_permisions(interaction, error):
    await interaction.response.send_message(f"[!!] No es posible ejecutar este comando [!!] ({error.__cause__})", ephemeral=True)

def loadcommands(bot: FalseBot):

    ### TEST COMMANDS ###

    ## TEST WELCOME ##
    @bot.tree.command(name="testwelcome")
    @is_owner()
    async def testwelcome(interaction: discord.Interaction):
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
        await member.timeout(timedelta(minutes=time))
        await interaction.response.send_message(f"El usuario {member.global_name} a sido silenciado por {time} minuto(s). Motivo: {reason}")
    ## ERROR ##
    @ftimeout.error
    async def ftimeout_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)

    ## KICK ##
    @bot.tree.command(name="fkick")
    @app_commands.describe(member = "Usuario", reason = "Motivo")
    @is_owner()
    async def fkick(interaction: discord.Interaction, member: discord.Member, reason: str):
        await member.kick()
        await interaction.response.send_message(f"El usuario {member.global_name} a sido expulsado. Motivo: {reason}")
    ## ERROR ##
    @fkick.error
    async def fkick_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)

    ## BAN ##
    @bot.tree.command(name="fban")
    @app_commands.describe(member= "Usuario", reason= "Motivo", time = "Tiempo en dias")
    @is_owner()
    @commands.has_permissions(ban_members=True)
    async def fban(interaction: discord.Interaction, member: discord.Member, reason: str, time: int):
        await member.ban()
        await interaction.response.send_message(f"El usuario {member.global_name} a sido baneado permanentemente. Motivo: {reason}")
    ## ERROR ##
    @fban.error
    async def fban_error(interaction: discord.Interaction, error):
        await error_message_not_enough_permisions(interaction, error)



