import discord

class FalseIntents():
    def intents():
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        return intents