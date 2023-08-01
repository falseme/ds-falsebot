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

huglist = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTB2c3M0Mm8wMXNqZ24xaDBkenRicThsd210eTI3YzQxdjFmbnB2cSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/u9BxQbM5bxvwY/giphy.gif",
           "https://media.giphy.com/media/LWTxLvp8G6gzm/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdmdDFqdGh2aXA1NG42bXgweWFjdTVuZ3djY24yazRyMWY0c21teiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5eyhBKLvYhafu/giphy.gif"]

patlist = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYm4yeWE1dDZtZno1YjQ0cDZqOWhjYXZnZ21qZXg2c2VzcTg1eGczeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/M3a51DMeWvYUo/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMmI1MnQ3YTVnc2tnMjdlcDh0ZzZxdHI1Z3U2ZHc5MmM5ZXpkb25wciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/4HP0ddZnNVvKU/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjQ0Zjlncno0dTEwY21ncm55anUxdmJwdnpqZXMxcTRlZG5sbmt1ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5tmRHwTlHAA9WkVxTU/giphy.gif",
           "https://media.giphy.com/media/SSPW60F2Uul8OyRvQ0/giphy.gif"]

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

    ### USER COMMANDS ###

    ## HELP ##

    @bot.tree.command(name="fhelp")
    async def fhelp(interaction: discord.Interaction):
        msg = discord.Embed(colour = discord.Colour.blue(), title = "**Lista de Comandos**", type = "rich")
        if(interaction.user.get_role(859958148625203201) != None):
            msg.add_field(inline = False, name = "**Moderacion**",
                          value = "- `/fwarn [usuario] [motivo]` - Da una advertencia por md a un usuario\n" + 
                          "- `/ftimeout [usuario] [minutos] [motivo]` - Silencia un usuario por un tiempo determinado\n" + 
                          "- `/fkick [usuario] [motivo]` - Expulsa a un usuario\n" + 
                          "- `/fban [usuario] [dias] [motivo]` - Banea a un usuario por un tiempo determinad\n")
        msg.add_field(inline = False, name = "**Interaccion entre usuarios**",
                      value = "- `/fhug [usuario] [monkey]` - Envia un abrazo a otro usuario. 'monkey' es opcional\n" + 
                      "- `/fpat [usuario]` - Envia un \"pat\" a otro usuario\n")
        msg.add_field(inline = False, name = "**Interaccion con el bot (AI)**",
                      value = "- `/falsebot [prompt/message]` - El bot responde a lo que sea que le envies\n")
        #msg.add_field(inline = False, name = "NSFW",
        #              value = "- `/fnsfw-rand` - Genera un codigo aleatorio\n")

        await interaction.response.send_message(embed = msg, ephemeral = True)
    ## ERROR ##
    @fhelp.error
    async def fhelp_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## HUG ##
    @bot.tree.command(name="fhug")
    @app_commands.describe(member = "Usuario a quien quieres enviar el abrazo", monkey = "Verdadero SOLO si desea que el gif sea de un mono")
    async def fhug(interaction: discord.Interaction, member: discord.Member, monkey: bool = False):
        author = interaction.user
        embed = discord.Embed(colour = discord.Colour.blue(), description = f"{member.mention}! {author.mention} te ha enviado un abrazo!", type = "rich")

        if(monkey):
            url = huglistmonkey[random.randint(0, len(huglistmonkey)-1)]
            embed.set_footer(text="Reject humanity, become monkey!")
        else:
            url = huglist[random.randint(0, len(huglist)-1)]

        embed.set_image(url = url)
        await interaction.response.send_message(embed = embed)
    ## ERROR ##
    @fhug.error
    async def fhug_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)

    ## PAT ##
    @bot.tree.command(name="fpat")
    @app_commands.describe(member = "Ususario a quien quieres enviar el 'pat'")
    async def fpat(interaction: discord.Interaction, member: discord.Member):
        author = interaction.user
        embed = discord.Embed(colour = discord.Colour.blue(), description = f"{member.mention}! {author.mention} te ha enviado un pat!", type = "rich")

        url = patlist[random.randint(0, len(patlist)-1)]
        embed.set_image(url = url)
        await interaction.response.send_message(embed = embed)
    ## ERROR ##
    @fpat.error
    async def fpat_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)


    ### OPENAI ###

    ## RESPONSE ##
    @bot.tree.command(name="falsebot")
    @app_commands.describe(message = "Mensaje o \"Prompt\" a enviar al bot para que este responda")
    async def falsebot(interaction: discord.Interaction, message: str):
        response = gpt.response(prompt = message)
        await interaction.response.send_message(response)
    ## ERROR ##
    @falsebot.error
    async def falsebot_error(interaction: discord.Interaction, error):
        await command_error_message(interaction = interaction, error = error)
