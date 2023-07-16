import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async
from PIL import ImageFont

class FalseBot(commands.Bot):

    # Run Bot
    def runbot(self):
        filename = ".token"

        try:
            with open(filename, 'r') as file:
                token = file.readline()
                self.run(token)
        except Exception:
            print("ERROR: COULD NOT READ BOT TOKEN FILE (.token). Assure .token file is in the root directory of the project")
        finally:
            file.close()


    # Bot Events
    # Bot initialized
    async def on_ready(self):
        print(f'Logged as {self.user}')

    # New Member
    # Generates a welcome embed message
    async def on_member_join(self, member):
        background_width = 800 # background image width
        pfpsize = 240 # profile picture size (width = height)
        pfpx = int(background_width / 2 - pfpsize / 2) # centered profile picture
        pfpy = 20 # profile picture y position on background image
        textx = int(background_width / 2) # centered texts
        text1y = 280 # Title *
        text2y = 370 # user mention **

        channel = member.guild.system_channel
        welcome_msg = f"BIENVENID@!" # Title *
        welcome_mention = f"{member.global_name} ({member.name})" # user mention **

        font = ImageFont.truetype(font='res/fonts/StoryElement.ttf', size=100)
        font_small = ImageFont.truetype(font='res/fonts/StoryElement.ttf', size=40)

        background = Editor("res/imgs/bg.jpg").blur()
        pfp = await load_image_async(str(member.display_avatar.url))
        profile = Editor(pfp).resize((pfpsize, pfpsize)).circle_image()

        background.paste(profile, (pfpx, pfpy))
        background.ellipse((pfpx, pfpy), pfpsize, pfpsize, outline="white", stroke_width=7)
        background.text((textx, text1y), welcome_msg, color="white", font=font, align="center") # *
        background.text((textx, text2y), welcome_mention, color="white", font=font_small, align="center") # **

        msgfile = File(fp=background.image_bytes, filename="bg.jpg")
        await channel.send(f"Bienvenid@ a {member.guild.name}! Esperamos que disfrutes mucho tu estancia.")
        await channel.send(file=msgfile)

    # Bot read message
    async def on_message(self, message):
        if(message.author == self):
            return