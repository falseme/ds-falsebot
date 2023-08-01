import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async
from PIL import ImageFont

class FalseBot(commands.Bot):

    # Bot Events
    # Bot initialized
    async def on_ready(self):
        print(f'Logged as {self.user}')
        
        # Sync commands
        try:
            synced = await self.tree.sync()
            for s in synced:
                print(s.name)
        except Exception as ex:
            print(ex)

    # New Member
    # Generates a welcome embed message
    async def on_member_join(self, member):
        await self.welcome_member(member)

    # Bot read message
    async def on_message(self, message):
        if(message.author == self):
            return

    # Methods
    # welcome_member: welcomes a new member using an image
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
        welcome_msg = f"¡BIENVENID@!" # Title *
        welcome_mention = f"{member.global_name} ({member.name})" # user mention **
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


