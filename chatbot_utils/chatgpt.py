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

    # 2. Voice-based prompt (new functionality)
    print("Voice-based prompt:")
    print("Speak your recipe request when prompted...")
    voice_response = voice_to_llm()
    print(f"LLM Response: {voice_response}")