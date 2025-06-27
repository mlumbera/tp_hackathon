from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe', methods=['POST'])
def recipe():
    ingredient_str = request.form.get('ingredients', '')
    notes = request.form.get('notes', '')
    ingredients = [i.strip() for i in ingredient_str.split(',') if i.strip()]
    
    # Normally you would now call your LLM/helper to generate the recipe from ingredients+notes!
    # Here, just render a simple result page.
    return render_template('recipe.html', ingredients=ingredients, notes=notes, recipe="(Placeholder recipe here!)")

if __name__ == '__main__':
    app.run(debug=True, port=8080)