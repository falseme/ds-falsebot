import nextcord

def get_intents():
	intents = nextcord.Intents.default()
	intents.members = True
	intents.message_content = True
	return intents