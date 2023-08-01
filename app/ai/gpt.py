import openai

def response(prompt):
	response = openai.Completion.create(
		model = "text-davinci-003",
		prompt = prompt,
		temperature = 1,
		max_tokens = 100
	)
	responses = response.get("choices")
	if responses and len(responses) > 0:
		prompt_response = responses[0]["text"]
	return prompt_response