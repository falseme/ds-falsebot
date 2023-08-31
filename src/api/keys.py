from dotenv import load_dotenv
import openai
import os

def load():
	load_dotenv()
	openai.api_key = get_openai_key()

def get_discord_token():
	return os.getenv('DISCORD_TOKEN')

def get_openai_key():
	return os.getenv('OPENAI_API_KEY')

def get_modlog_channel():
	return int(os.getenv('DS_CHANNEL_MOD_LOG_ID'))

def get_role_mod():
	return os.getenv('DS_ROLE_MOD')

def get_role_admin():
	return os.getenv('DS_ROLE_ADMIN')

def get_role_tester():
	return os.getenv('DS_ROLE_TESTER')


