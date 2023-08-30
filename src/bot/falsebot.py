import nextcord
from nextcord import File
from nextcord.ext import commands
from api import keys as falseapi

from easy_pil import Editor, load_image_async
from PIL import ImageFont

from bot import intents

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

	async def mod_send_embed(embed_interaction: nextcord.Interaction, embed_member: nextcord.Member, embed_title: str, description: str, extra_description: str, iconfile: str):
		msg = nextcord.Embed(colour = nextcord.Colour.dark_orange(), title = f"**{embed_title}**", type = "rich")
		msg.add_field(name = description, value = extra_description)
		msg.set_thumbnail(url = f"attachment://{iconfile}")

		await embed_member.send(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg)
		await embed_member.guild.get_channel(falseapi.get_modlog_channel()).send(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg)
		await embed_interaction.response.send_message(file = File(f"res/icons/{iconfile}", filename= iconfile), embed = msg, delete_after = 4.0)

	### TEST COMMANDS ###

	@bot.slash_command(description="Test Commands")
	async def test(interaction: nextcord.Interaction):
		pass
		
	@test.subcommand(description="Test welcome funciton")
	async def welcome(interaction: nextcord.Interaction):
		await bot.welcome_member(interaction.user)
		await interaction.send("Welcome user", ephemeral=True)
	
	### MODERATION COMMANDS ###        

	@bot.slash_command(description="Moderation Commands")
	async def mod(interaction: nextcord.Interaction):
		pass
	
	@mod.subcommand(description="Ban a user")
	async def ban(interaction: nextcord.Interaction, member: nextcord.Member, time: int, reason: str):
		print(f"[MOD] {member.display_name} - banned")
		await mod_send_embed(interaction, member, "Usuario Baneado", f"El usuario {member.display_name}(@{member.name}) ha sido baneado", f"Motivo: {reason}\nTiempo: {time} dia(s)", "ban.png")
		
	@mod.subcommand(description="Kick a user")
	async def kick(interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
		print(f"[MOD] {member.display_name} - kicked")
		await mod_send_embed(interaction, member, "Usuario Expulsado", f"El usuario {member.display_name}(@{member.name}) ha sido expulsado", f"Motivo: {reason}", "kick.png")
		
	@mod.subcommand(description="Timeout a user")
	async def timeout(interaction: nextcord.Interaction, member: nextcord.Member, time: int, reason: str):
		print(f"[MOD] {member.display_name} - timeout")
		await mod_send_embed(interaction, member, "Usuario Muteado", f"El usuario {member.display_name}(@{member.name}) ha sido muteado", f"Motivo: {reason}\nTiempo: {time} minuto(s)", "timeout.png")
		
	@mod.subcommand(description="Warn a user")
	async def warn(interaction: nextcord.Interaction, member: nextcord.Member, reason: str):
		print(f"[MOD] {member.display_name} - warn")
		await mod_send_embed(interaction, member, "Warn", f"El usuario {member.display_name}(@{member.name}) ha recibido una advertencia", f"Motivo: {reason}", "warn.png")
		
	
	### USER INTERACTION COMMANDS ###

	@bot.slash_command(description="Interact with other users")
	async def user(interaction: nextcord.Interaction):
		pass

	@user.subcommand(description="Send a hug")
	async def hug(interaction: nextcord.Interaction):
		await interaction.send("HUG!")
		

	### NSFW COMMANDS ###

	@bot.slash_command(description="nsfw")
	async def nsfw(interaction: nextcord.Interaction):
		pass
	
	@nsfw.subcommand(description="Get a random manga code")
	async def random(interaction: nextcord.Interaction):
		await interaction.send("RANDOM")
		
	@nsfw.subcommand(description="Get the week top")
	async def top(interaction: nextcord.Interaction):
		await interaction.send("TOP")
		
	### AI COMMANDS ###

	@bot.slash_command(description="AI commands")
	async def ai(interaction: nextcord.Interaction):
		pass
	
	@ai.subcommand(description="generate a response")
	async def gpt(interaction: nextcord.Interaction):
		await interaction.send("GPT")
		
	@ai.subcommand(description="Reply the message above")
	async def replygpt(interaction: nextcord.Interaction):
		await interaction.send("REPLYGPT")

	bot.run(token)