# 🍳 Chef Bot — Your Personal Recipe Assistant

Chef Bot is a lightweight, conversational web application built using **Flask** and **vanilla JavaScript**. It acts as an interactive culinary companion, letting users look up specific recipes, filter by dietary requirements (like vegetarian), search by skill level, or find meal ideas based on specific ingredients they have left in the fridge.

---

## ✨ Features

* **Smart Conversational Flow:** Recognizes user intent including greetings, recipe keywords, ingredient lists, and specific requests like "easy recipes" or "vegetarian options."
* **Ingredient-Based Filtering:** Tell the bot what you have (e.g., *"I have chicken and lemon"*), and it will suggest matching recipes.
* **Rich UI Cards:** Renders clean, interactive recipe formats containing localized metadata (prep time, difficulty), structured ingredient checklists, sequential step guides, and italicized chef tips.
* **Quick UI Actions:** Includes sidebar shortcut buttons and responsive suggestion chips that update the chat flow with a single click.
* **Dynamic Typing Indicators:** Delivers a smooth user experience mimicking a real-time messaging environment.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.x, Flask
* **Frontend:** HTML5, CSS3, JavaScript (ES6+ Vanilla)
* **Fonts Used:** *Playfair Display* (elegant serif headers) and *DM Sans* (clean modern typography)

---

## 📁 Project Structure

```text
chef-bot/
│
├── app.py                  # Main Flask server & conversational logic/database
├── templates/
│   └── index.html          # Main web application layout
└── static/
    ├── css/
    │   └── style.css       # Complete application styling & styling rules
    └── js/
        └── chat.js         # DOM manipulation, fetch requests, and response routing

```

---

## 🚀 Getting Started

Follow these steps to run the Chef Bot application locally on your machine.

### 1. Prerequisites

Make sure you have Python installed on your system. You can verify this by running:

```bash
python --version

```

### 2. Install Flask

If you don't have Flask installed yet, install it via `pip`:

```bash
pip install Flask

```

### 3. Run the Application

Navigate to the root directory containing `app.py` and execute the application:

```bash
python app.py

```

### 4. Open in Browser

Once the local development server starts, open your browser and navigate to:

```text
http://127.0.0.1:5000/

```

---

## 🤖 Supported Queries & Keywords

Chef Bot's simple matching algorithm allows you to interact with it using natural phrases. Here are a few examples you can try typing:

* **General Lookups:** `"Show me all recipes"`, `"What's on the menu?"`
* **Specific Dishes:** `"I want pasta"`, `"How do I make chocolate lava cake?"`
* **Ingredient Matching:** `"I have tomatoes and basil"`, `"What can I make with eggs?"`
* **Dietary / Level Filters:** `"Vegetarian options"`, `"Give me something easy to cook"`
