from flask import Flask, render_template, request
import sys
import os

# Add the chatbot_utils directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'chatbot_utils'))
from chatgpt import ask_llm

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe', methods=['POST'])
def recipe():
    ingredient_str = request.form.get('ingredients', '')
    notes = request.form.get('notes', '')
    ingredients = [i.strip() for i in ingredient_str.split(',') if i.strip()]
    
    # Generate recipe using LLM
    if ingredients:
        prompt = f"Suggest a local Indiana-inspired recipe using {', '.join(ingredients)}"
        if notes:
            prompt += f", with the following notes: {notes}"
        prompt += ". Provide ingredients and simple, numbered steps."
        
        recipe = ask_llm(prompt)
    else:
        recipe = "Please provide some ingredients to generate a recipe."
    
    return render_template('recipe.html', ingredients=ingredients, notes=notes, recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True, port=8080)