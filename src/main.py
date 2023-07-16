from falsebot.falsebot import FalseBot
from falsebot.falseintents import FalseIntents

false_command = '&'
false_desc = "Falseme Mod Bot"
false_intents = FalseIntents.intents()

falsebot = FalseBot(command_prefix=false_command, description=false_desc, intents=false_intents)

falsebot.runbot()

