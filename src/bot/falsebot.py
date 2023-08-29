import nextcord
from nextcord import File
from nextcord.ext import commands

from easy_pil import Editor, load_image_async
from PIL import ImageFont

from bot import intents

class FalseBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_member_join(self, member):
        await self.welcome_member(self, member)
        
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

    @bot.slash_command(description="Replies with pong!")
    async def ping(interaction: nextcord.Interaction):
        await interaction.send("Pong!", ephemeral=True)
        
    @bot.slash_command(description="Test welcome funciton")
    async def testwelcome(interaction: nextcord.Interaction):
        await bot.welcome_member(interaction.user)
        await interaction.send("Welcome user", ephemeral=True)
    
    ### MODERATION COMMANDS ###        

    @bot.slash_command(description="Moderation Commands")
    async def mod(interaction: nextcord.Interaction):
        pass
    
    @mod.subcommand(description="Ban a user")
    async def ban(interaction: nextcord.Interaction):
        await interaction.send("BANNED")
        
    @mod.subcommand(description="Kick a user")
    async def kick(interaction: nextcord.Interaction):
        await interaction.send("KICKED")
        
    @mod.subcommand(description="Timeout a user")
    async def timeout(interaction: nextcord.Interaction):
        await interaction.send("TIMEOUT")
        
    @mod.subcommand(description="Warn a user")
    async def warn(interaction: nextcord.Interaction):
        await interaction.send("WARNED")
        
    
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