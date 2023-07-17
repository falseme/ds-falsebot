from client import fintents, fbot
import config

false_command = '&'
false_desc = "Falseme Mod Bot"
false_intents = fintents.intents()

falsebot = fbot.FalseBot(command_prefix=false_command, description=false_desc, intents=false_intents)

falsebot.run(config.TOKEN)

