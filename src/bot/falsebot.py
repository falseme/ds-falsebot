import nextcord
from nextcord import File, Permissions
from nextcord.ext import commands

from easy_pil import Editor, load_image_async
from PIL import ImageFont

from bot import intents
from api import keys as falseapi
from ai import gpt
from false_requests import nsfw_request

import random as py_random

class FalseBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	### EVENTS ###

	async def on_ready(self):
		print(f"Logged in as {self.user} (ID: {self.user.id})")

	async def on_member_join(self, member):
		await self.welcome_member(self, member)
		
	### UTIL ###

	async def welcome_member(self, member):
		background_width = 800 # background image width
		pfpsize = 230 # profile picture size (width = height)
		pfpx = int(background_width / 2 - pfpsize / 2) # centered profile picture
		pfpy = 20 # profile picture y position on background image
		textx = int(background_width / 2) # centered texts
		text1y = 270 # Title *
		text2y = 350 # user mention **
		text3y = 405 # user count ***

		channel = member.guild.system_channel
		welcome_msg = f"BIENVENID@!" # Title *
		welcome_mention = f"{member.display_name} ({member.name})" # user mention **
		num = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)
		welcome_count = f"ERES EL MIEMBRO #{num}" # user count ***

		font = ImageFont.truetype(font='res/fonts/StoryElement.ttf', size=100)
		font_small = ImageFont.truetype(font='res/fonts/StoryElement.ttf', size=40)
		font_count = ImageFont.truetype(font='res/fonts/StoryElement.ttf', size=25)

		background = Editor("res/imgs/bg.jpg").blur()
		background_frame = Editor("res/imgs/bg-frame.png")
		pfp = await load_image_async(str(member.display_avatar.url))
		profile = Editor(pfp).resize((pfpsize, pfpsize)).circle_image()

		background.paste(profile, (pfpx, pfpy))
		background.paste(background_frame, (0, 0))
		#background.ellipse((pfpx-5, pfpy-5), pfpsize+10, pfpsize+10, outline="white", stroke_width=7)
		background.text((textx, text1y), welcome_msg, color="white", font=font, align="center") # *
		background.text((textx, text2y), welcome_mention, color="white", font=font_small, align="center") # **
		#background.text((textx, text3y), welcome_count, color="white", font=font_count, align="center") # ***

		msgfile = File(fp=background.image_bytes, filename="bg.jpg")
		await channel.send(f"Bienvenid@ a {member.guild.name}! Esperamos que disfrutes mucho tu estancia.")
		await channel.send(file=msgfile)
			
def run(token:str):
	bot_intents = intents.get_intents()
	command_prefix = "&"

	bot = FalseBot(command_prefix=command_prefix, intents=bot_intents)
	
	### UTIL ###

	huglist = ["https://media.tenor.com/-rW7zgTPkkwAAAAi/hug.gif", "https://media.tenor.com/c3CBzmFnqHYAAAAi/hug.gif"]

	async def mod_send_embed(embed_interaction: nextcord.Interaction, embed_member: nextcord.Member, embed_title: str, description: str, extra_description: str, iconfile: str, notify: bool = True):
		msg = nextcord.Embed(colour = nextcord.Colour.dark_orange(), title = f"**{embed_title}**", type = "rich")
		msg.add_field(name = description, value = extra_description)
		msg.set_thumbnail(url = f"attachment://{iconfile}")

		await embed_member.send(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg)
		await embed_member.guild.get_channel(falseapi.get_modlog_channel()).send(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg)
		await embed_interaction.send(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg, delete_after = 4.0, ephemeral = not notify)

	### TEST COMMANDS ###

	@bot.slash_command(description="Test Commands", dm_permission=False)
	async def test(interaction: nextcord.Interaction):
		pass
		
	@test.subcommand(description="Test welcome funciton")
	async def welcome(interaction: nextcord.Interaction):
		await bot.welcome_member(interaction.user)
		await interaction.send("Welcome user", ephemeral=True)
	
	### MODERATION COMMANDS ###        

	@bot.slash_command(description="Moderation Commands", dm_permission=False, default_member_permissions=Permissions(ban_members=True))
	async def mod(interaction: nextcord.Interaction):
		pass
	
	@mod.subcommand(description="Banea un usuario")
	async def ban(interaction: nextcord.Interaction, member: nextcord.Member, time: int, reason: str):
		print(f"[MOD] {member.display_name} > banned")
		await mod_send_embed(interaction, member, "Usuario Baneado", f"El usuario **{member.display_name}** ha sido baneado", f"Motivo: {reason}\nTiempo: {time} dia(s)", "ban.png")
		
	@mod.subcommand(description="Echa un usuario")
	async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
		print(f"[MOD] {member.display_name} > kicked")
		await mod_send_embed(interaction, member, "Usuario Expulsado", f"El usuario **{member.display_name}** ha sido expulsado", f"Motivo: {reason}", "kick.png")
		
	@mod.subcommand(description="Mutea un usuario")
	async def timeout(interaction: nextcord.Interaction, member: nextcord.Member, time: int, reason: str):
		print(f"[MOD] {member.display_name} > timeout")
		await mod_send_embed(interaction, member, "Usuario Muteado", f"El usuario **{member.display_name}** ha sido muteado", f"Motivo: {reason}\nTiempo: {time} minuto(s)", "timeout.png")
		
	@mod.subcommand(description="Da una advertencia a un usuario")
	async def warn(interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
		print(f"[MOD] {member.display_name} > warn")
		await mod_send_embed(interaction, member, "Warn", f"El usuario **{member.display_name}** ha recibido una advertencia", f"Motivo: {reason}", "warn.png", False)
		
	
	### USER INTERACTION COMMANDS ###

	@bot.slash_command(description="Interact with other users", dm_permission=False)
	async def user(interaction: nextcord.Interaction):
		pass

	@user.subcommand(description="Envia un abrazo")
	async def hug(interaction: nextcord.Interaction, member: nextcord.Member):
		print(f"[USER] {interaction.user.display_name} > sent a hug to {member.display_name}")
		author = interaction.user
		msg = nextcord.Embed(colour = nextcord.Colour.blue(), description = f"{member.mention}! {author.mention} te ha enviado un abrazo!", type = "rich")
		url = huglist[py_random.randint(0, len(huglist)-1)]

		msg.set_image(url = url)
		await interaction.send(embed = msg)

	### NSFW COMMANDS ###

	@bot.slash_command(description="nsfw", dm_permission=False, nsfw=True)
	async def nsfw(interaction: nextcord.Interaction):
		pass
	
	@nsfw.subcommand(description="Recomienda un doujin aleatorio")
	async def random(interaction: nextcord.Interaction):
		print(f"[NSFW] {interaction.user.display_name} > random doujin")
		print(nsfw_request.get_random())
		await interaction.send("CMD")
		
	@nsfw.subcommand(description="Lista los doujins mas leidos de esta semana")
	async def top(interaction: nextcord.Interaction):
		await interaction.send("TOP")
		
	### AI COMMANDS ###

	@bot.slash_command(description="AI commands")
	async def ai(interaction: nextcord.Interaction):
		pass
	
	@ai.subcommand(description="Pregunta lo que sea")
	async def askgpt(interaction: nextcord.Interaction, message: str):
		print(f"[AI] {interaction.user.display_name} > askgpt")
		response = gpt.generate_response(prompt=message)
		print(f"[AI] {message} > {response}")
		await interaction.send(f"{interaction.user.mention}: {message}\n{response}")
		
	@ai.subcommand(description="Responde al mensaje anterior")
	async def replygpt(interaction: nextcord.Interaction):
		print(f"[AI] {interaction.user.display_name} > replygpt")
		author = interaction.channel.last_message.author
		msg = interaction.channel.last_message.content
		response = gpt.generate_response(prompt=msg)
		print(f"[AI] {msg} > {response}")
		await interaction.send(f"{author.mention}: {msg}\n{response}")

	### HELP COMMANDS ###

	@bot.slash_command(description="ayuda")
	async def falsehelp(interaction: nextcord.Interaction):
		pass

	@falsehelp.subcommand(description = "ayuda general", name = "all")
	async def help_all(interaction: nextcord.Interaction):
		print(f"[FALSE-BOT] {interaction.user.display_name} > /help")
		
		msg = nextcord.Embed(colour = nextcord.Colour.blue(), title = f"**Falsa tabla de una no real ayuda**", type = "rich")
		#MOD#
		role = interaction.user.top_role
		if(role.name == falseapi.get_role_mod() or role.name == falseapi.get_role_admin()):
			msg.add_field(inline = False, name = "Para Mods:", value =
		 "- **/mod warn [usuario] [motivo]** - Advertencia por md\n" +
		 "- **/mod timeout [usuario] [tiempo] [motivo]** - Timeout por 'x' minutos\n" +
		 "- **/mod kick [usuario] [motivo]** - Un kick sin mas\n" +
		 "- **/mod ban [usuario] [dias] [motivo]** - Ban por 'x' dias\n")

		#USERS#
		msg.add_field(inline = False, name = "Interacciones:", value =
		 "- **/user hug [usuario]** - Envia un gif de un abrazo\n")

		#AI#
		msg.add_field(inline = False, name = "Inteligencia Artificial:", value =
		 "- **/ai ask [mensaje]** - Recibe una respuesta generada con GPT\n" +
		 "- **/ai reply** - Responde el mensaje de arriba\n")

		#NSFW#
		msg.add_field(inline = False, name = "NSFW:", value =
		 "- **/falsehelp ['nsfw']**\n")
		
		file = File(f"res/icons/help.png", filename= "help.png")
		msg.set_thumbnail(url = f"attachment://help.png")
		
		await interaction.send(file = file, embed = msg)

	@falsehelp.subcommand(description = "ayuda nsfw", name = "nsfw")
	async def help_nsfw(interaction: nextcord.Interaction):
		msg = nextcord.Embed(colour = nextcord.Colour.blue(), title = f"**Falsa tabla de una no real ayuda**", type = "rich")
		msg.add_field(inline = False, name = "NSFW:", value =
		 "- **Solo disponible en canales 'nsfw'**\n" + 
		 "- **/nsfw random ** - Muestra un doujin aleatorio\n" +
		 "- **/nsfw top ** - Muestra el top semanal\n")
		
		file = File(f"res/icons/help.png", filename= "help.png")
		msg.set_thumbnail(url = f"attachment://help.png")
		
		await interaction.send(file = file, embed = msg)

	bot.run(token)