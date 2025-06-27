from flask import Flask, render_template, request, jsonify, redirect, url_for
import sys
import os
import re
from datetime import datetime
import json

# Add the chatbot_utils directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'chatbot_utils'))
from chatgpt import ask_llm

app = Flask(__name__)

# Simple in-memory storage for shopping lists (in production, use a database)
SHOPPING_LISTS_FILE = 'shopping_lists.json'

def load_shopping_lists():
	"""
	Load shopping lists from file
	"""
	try:
		if os.path.exists(SHOPPING_LISTS_FILE):
			with open(SHOPPING_LISTS_FILE, 'r') as f:
				return json.load(f)
	except Exception as e:
		print(f"Error loading shopping lists: {e}")
	return []

def save_shopping_lists(shopping_lists):
	"""
	Save shopping lists to file
	"""
	try:
		with open(SHOPPING_LISTS_FILE, 'w') as f:
			json.dump(shopping_lists, f, indent=2)
	except Exception as e:
		print(f"Error saving shopping lists: {e}")

def extract_recipe_ingredients(recipe_text):
	"""
	Extract ingredients from recipe text using LLM
	Returns a list of ingredient strings
	"""
	prompt = f"""Extract ONLY the ingredients needed for this recipe. 
	Return them as a simple comma-separated list with no additional text.
	Recipe: {recipe_text}"""
	
	ingredients_response = ask_llm(prompt)
	# Clean up the response and split by commas
	ingredients = [i.strip() for i in ingredients_response.split(',') if i.strip()]
	return ingredients

def generate_shopping_list(recipe_text, user_ingredients):
	"""
	Generate shopping list by comparing recipe ingredients with user ingredients
	Returns list of ingredients user needs to buy
	"""
	recipe_ingredients = extract_recipe_ingredients(recipe_text)
	user_ingredients_lower = [i.lower().strip() for i in user_ingredients]
	
	shopping_list = []
	for ingredient in recipe_ingredients:
		ingredient_lower = ingredient.lower().strip()
		# Check if user has this ingredient (simple substring matching)
		has_ingredient = any(user_ingredient in ingredient_lower or ingredient_lower in user_ingredient 
						   for user_ingredient in user_ingredients_lower)
		if not has_ingredient:
			shopping_list.append(ingredient)
	
	return shopping_list

def extract_recipe_name(recipe_text):
	"""
	Extract recipe name from recipe text using LLM
	"""
	prompt = f"""Extract ONLY the name/title of this recipe. 
	Return just the name, no additional text.
	Recipe: {recipe_text}"""
	
	name_response = ask_llm(prompt)
	return name_response.strip()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recipe', methods=['POST'])
def recipe():
	ingredient_str = request.form.get('ingredients', '')
	notes = request.form.get('notes', '')
	# Get possible multiple dietary needs, as a list
	diets = request.form.getlist('diet')
	ingredients = [i.strip() for i in ingredient_str.split(',') if i.strip()]
	
	# Generate recipe using LLM
	if ingredients:
		prompt = f"Suggest a local Indiana-inspired recipe using {', '.join(ingredients)}"
		if diets:
			prompt += f", meeting these dietary needs: {', '.join(diets)}"
		if notes:
			prompt += f", with the following notes: {notes}"
		prompt += ". Provide ingredients and simple, numbered steps."
		
		recipe = ask_llm(prompt)
	else:
		recipe = "Please provide some ingredients to generate a recipe."
	
	# Check if the recipe is the error message
	is_error = recipe == "Sorry, I couldn't find a recipe right now."
	
	return render_template('recipe.html', ingredients=ingredients, notes=notes, recipe=recipe, diets=diets, is_error=is_error)

@app.route('/shopping-list', methods=['POST'])
def shopping_list():
	"""
	Generate shopping list and redirect to shopping list page
	"""
	recipe_text = request.form.get('recipe', '')
	user_ingredients = request.form.get('ingredients', '').split(',')
	user_ingredients = [i.strip() for i in user_ingredients if i.strip()]
	notes = request.form.get('notes', '')
	
	# Check if recipe is the error message
	if not recipe_text or recipe_text == "Sorry, I couldn't find a recipe right now.":
		return redirect(url_for('recipe_error'))
	
	# Generate shopping list
	shopping_items = generate_shopping_list(recipe_text, user_ingredients)
	recipe_name = extract_recipe_name(recipe_text)
	
	# Create shopping list entry
	shopping_list_entry = {
		'id': datetime.now().strftime('%Y%m%d_%H%M%S'),
		'recipe_name': recipe_name,
		'recipe_text': recipe_text,
		'user_ingredients': user_ingredients,
		'notes': notes,
		'shopping_items': shopping_items,
		'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	}
	
	# Load existing lists and add new one
	shopping_lists = load_shopping_lists()
	shopping_lists.insert(0, shopping_list_entry)  # Add to beginning
	save_shopping_lists(shopping_lists)
	
	return redirect(url_for('shopping_lists'))

@app.route('/recipe-error')
def recipe_error():
	"""
	Error page when recipe generation fails
	"""
	return render_template('recipe_error.html')

@app.route('/shopping-lists')
def shopping_lists():
	"""
	Shopping list page with history
	"""
	shopping_lists = load_shopping_lists()
	
	# Get current list (most recent)
	current_list = shopping_lists[0] if shopping_lists else None
	
	# Get history (all except current)
	history_lists = shopping_lists[1:] if len(shopping_lists) > 1 else []
	
	return render_template('shopping_list.html', 
						 current_list=current_list, 
						 shopping_lists=history_lists)

if __name__ == '__main__':
	app.run(debug=True, port=8080)