import discord
from discord.ext import commands

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
    #async def on_member_join(self, member):


    # Bot read message
    # ctx = context
    async def on_message(ctx):
        print("test-borrar")