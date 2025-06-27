import requests
import time
from voice_input import voice_input

def ask_llm(prompt):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    system_prompt = "You are a supportive, expert chef with a focus on Indiana flavors. Respond in simple, step-by-step instructions using large, clear language."
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return reply
    else:
        return "Sorry, I couldn't find a recipe right now."

def voice_to_llm():
	"""
	Captures voice input and sends it to the LLM
	Returns the LLM response
	"""
	# Get voice input
	voice_prompt = voice_input()
	
	if voice_prompt:
		# Send to LLM
		response = ask_llm(voice_prompt)
		return response
	else:
		return "No voice input received. Please try again."

if __name__ == "__main__":
    # Usage examples:

    # 1. Text-based prompt (original functionality)
    ingredients = ['corn', 'tomatoes', 'chicken']
    dietary = 'gluten-free'
    prompt = f"Suggest a local Indiana-inspired recipe using {', '.join(ingredients)}, suitable for {dietary}. Provide ingredients and simple, numbered steps."
    print("Text-based prompt:")
    print(ask_llm(prompt))
    print("\n" + "="*50 + "\n")