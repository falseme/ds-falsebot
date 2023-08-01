from app.client import intents, bot, commands

def run(bot_token: str):
    false_command = '&'
    false_desc = "Falseme Mod Bot"
    false_intents = intents.intents()
    # init bot
    falsebot = bot.FalseBot(command_prefix=false_command, description=false_desc, intents=false_intents)
    # init commands
    commands.loadcommands(falsebot)
    # run bot
    falsebot.run(bot_token)

