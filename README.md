# Plated - Recipe Helper App

A web application that helps you create delicious recipes using ingredients you already have, with AI-powered recipe suggestions and automatic shopping list generation. Perfect for reducing food waste and making the most of what's in your kitchen!

## What This App Does

🍳 **Smart Recipe Generation**: Enter the ingredients you have, and the app suggests Indiana-inspired recipes tailored to your dietary needs and preferences.

🛒 **Shopping List Creation**: After getting a recipe, the app automatically generates a shopping list of ingredients you need to buy, comparing against what you already have.

🎯 **Dietary Accommodations**: Support for various dietary needs including gluten-free, vegetarian, low-sodium, dairy-free, and more.

💭 **Personal Touch**: Add notes about how you're feeling or special requirements to get more personalized recipe suggestions.

📱 **User-Friendly Interface**: Clean, accessible web interface designed for easy use on any device.

## Features

- **Ingredient Input**: Add your own ingredients or select from suggested sale items
- **AI-Powered Recipes**: Uses OpenAI's GPT-3.5-turbo to generate creative, Indiana-inspired recipes
- **Shopping List Management**: Automatically creates and saves shopping lists
- **Recipe History**: View your previous recipes and shopping lists
- **Dietary Filters**: Choose from multiple dietary restrictions and preferences
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Your OpenAI API Key

**Important**: You need to provide your own OpenAI API key to use this application.

1. Get an API key from [OpenAI's website](https://platform.openai.com/api-keys)
2. Open `chatbot_utils/chatgpt.py` in a text editor
3. Find line 7 and replace the placeholder with your actual API key:

```python
"Authorization": "Bearer YOUR_OPENAI_API_KEY_HERE",
```

## Running the Application

### Start the Web App

```bash
cd flask_app
python app.py
```

The application will be available at `http://localhost:8080`

### Using the App

1. **Add Ingredients**: Type in ingredients you have or click on suggested sale items
2. **Set Dietary Needs**: Check any dietary restrictions that apply
3. **Add Notes**: Tell the app how you're feeling or any special requirements
4. **Get Recipe**: Click "Get Recipe" to receive an AI-generated recipe
5. **Create Shopping List**: After reviewing the recipe, create a shopping list of missing ingredients
6. **View History**: Access your previous recipes and shopping lists from the navigation

## Project Structure

```
tp_hackathon/
├── flask_app/                 # Main web application
│   ├── app.py                # Flask server and routes
│   ├── templates/            # HTML templates
│   └── shopping_lists.json   # Shopping list storage
├── chatbot_utils/            # AI integration utilities
│   ├── chatgpt.py           # OpenAI API integration
│   └── requirements.txt     # Python dependencies
└── README.md                # This file
```

## API Key Requirements

- **OpenAI API Key**: Required for recipe generation
- **Credits**: Ensure your OpenAI account has sufficient credits
- **Rate Limits**: Be aware of OpenAI's rate limits for API calls

## Troubleshooting

- **API Key Issues**: Make sure your OpenAI API key is valid and has credits
- **Recipe Generation Fails**: Check your internet connection and API key status

## Requirements

- Python 3.7+
- OpenAI API key with credits
- Internet connection
- Web browser (Chrome, Firefox, Safari, Edge)

## License

This project is created for educational and demonstration purposes.