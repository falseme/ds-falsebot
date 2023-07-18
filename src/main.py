from client import fintents, fbot, fcommands
import config

false_command = '&'
false_desc = "Falseme Mod Bot"
false_intents = fintents.intents()

# init bot
falsebot = fbot.FalseBot(command_prefix=false_command, description=false_desc, intents=false_intents)
# init commands
fcommands.loadcommands(falsebot)

falsebot.run(config.TOKEN)

