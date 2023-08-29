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