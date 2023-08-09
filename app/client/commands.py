from app.client.bot import FalseBot
import discord
from discord import app_commands
from discord.ext import commands
from app.ai import gpt

from datetime import timedelta
import random

huglistmonkey = ["https://media.giphy.com/media/42YlR8u9gV5Cw/giphy.gif",
           "https://media.giphy.com/media/JcEbzHIM7lJBe/giphy.gif",
           "https://media.giphy.com/media/qv6M5EBN5fhMA/giphy.gif",
           "https://media.giphy.com/media/H6NkrhBaDEXQt8pwbD/giphy.gif",
           "https://media.giphy.com/media/tyttpHcMlSFsNSPpEmA/giphy-downsized-large.gif"]

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

    ### MODERATION COMMANDS ###

    ## WARN ##
    @bot.tree.command(name="warn")
    @app_commands.describe(member = "Usuario", reason = "Motivo")
    @is_owner()
    async def fwarn(interaction: discord.Interaction, member: discord.Member, reason: str):
        msg = discord.Embed(colour = discord.Colour.dark_orange(), title = "**Warn**", type = "rich")
        msg.add_field(name = f"Advertencia para el usuario {member.global_name}(@{member.display_name})", value = f"Motivo: {reason}")
        msg.set_thumbnail(url = "attachment://warn.png")
        
        await member.send(file = discord.File("res/icons/warn.png", filename= "warn.png"), embed = msg)
        await member.guild.get_channel(1138766110955667507).send(file = discord.File("res/icons/warn.png", filename= "warn.png"), embed = msg)
        await interaction.response.send_message(file = discord.File("res/icons/warn.png", filename= "warn.png"), embed = msg, ephemeral = True)
    ## ERROR ##
    @fwarn.error
    async def fwarn_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ### USER COMMANDS ###

    ## HELP ##

    @bot.tree.command(name="fhelp")
    async def fhelp(interaction: discord.Interaction):
        msg = discord.Embed(colour = discord.Colour.blue(), title = "**Lista de Comandos**", type = "rich")
        msg.add_field(inline = False, name = "**Interaccion entre usuarios**",
                      value = "- `/fhug [usuario]` - Envia un abrazo a otro usuario. 'monkey gif'\n")
        msg.add_field(inline = False, name = "**Interaccion con el bot (AI)**",
                      value = "- `Mention` - Menciona al bot en un mensaje para conversar")
        #msg.add_field(inline = False, name = "NSFW",
        #              value = "- `/fnsfw-rand` - Genera un codigo aleatorio\n")

        await interaction.response.send_message(embed = msg, ephemeral = True)
    ## ERROR ##
    @fhelp.error
    async def fhelp_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## HUG ##
    @bot.tree.command(name="fhug")
    @app_commands.describe(member = "Usuario a quien quieres enviar el abrazo")
    async def fhug(interaction: discord.Interaction, member: discord.Member):
        author = interaction.user
        embed = discord.Embed(colour = discord.Colour.blue(), description = f"{member.mention}! {author.mention} te ha enviado un abrazo!", type = "rich")

        url = huglistmonkey[random.randint(0, len(huglistmonkey)-1)]
        embed.set_footer(text="Reject humanity, become monkey!")

        embed.set_image(url = url)
        await interaction.response.send_message(embed = embed)
    ## ERROR ##
    @fhug.error
    async def fhug_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

