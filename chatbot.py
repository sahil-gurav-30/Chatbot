from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# ─── Recipe Database ──────────────────────────────────────────────────────────
RECIPES = {
    "pasta": {
        "name": "Classic Spaghetti Carbonara",
        "emoji": "🍝",
        "time": "25 mins",
        "difficulty": "Medium",
        "ingredients": [
            "400g spaghetti",
            "200g pancetta or guanciale",
            "4 large eggs",
            "100g Pecorino Romano (grated)",
            "50g Parmesan (grated)",
            "Black pepper (freshly ground)",
            "Salt"
        ],
        "steps": [
            "Boil a large pot of salted water and cook spaghetti until al dente.",
            "Fry pancetta in a pan over medium heat until crispy. Set aside, keep the fat.",
            "Whisk eggs with grated Pecorino and Parmesan. Season with black pepper.",
            "Drain pasta, reserving 1 cup of pasta water.",
            "Off the heat, add pasta to the pan with pancetta. Pour egg mixture and toss quickly.",
            "Add splashes of pasta water to loosen. The heat of pasta cooks the eggs gently.",
            "Serve immediately with extra cheese and pepper."
        ],
        "tips": "Never add cream! The secret is tossing off the heat so eggs don't scramble. Work fast."
    },
    "chicken": {
        "name": "Lemon Herb Roast Chicken",
        "emoji": "🍗",
        "time": "1 hr 30 mins",
        "difficulty": "Easy",
        "ingredients": [
            "1 whole chicken (1.5–2 kg)",
            "2 lemons (zested and halved)",
            "4 cloves garlic",
            "Fresh rosemary and thyme",
            "3 tbsp olive oil",
            "Salt and black pepper",
            "1 onion (quartered)"
        ],
        "steps": [
            "Preheat oven to 200°C (400°F).",
            "Pat chicken dry with paper towels. Season generously inside and out with salt.",
            "Mix olive oil, lemon zest, minced garlic, and chopped herbs into a paste.",
            "Rub the herb mixture under and over the skin.",
            "Stuff cavity with lemon halves, garlic cloves, and herb sprigs.",
            "Place on a bed of quartered onion in a roasting pan.",
            "Roast for 1 hour 20 mins or until juices run clear. Rest for 15 mins before carving."
        ],
        "tips": "Letting the chicken rest is crucial — it redistributes juices and keeps the meat succulent."
    },
    "salad": {
        "name": "Mediterranean Feta Salad",
        "emoji": "🥗",
        "time": "15 mins",
        "difficulty": "Easy",
        "ingredients": [
            "200g mixed greens",
            "150g cherry tomatoes (halved)",
            "1 cucumber (diced)",
            "100g Kalamata olives",
            "150g feta cheese (crumbled)",
            "Red onion (thinly sliced)",
            "3 tbsp olive oil, 1 tbsp red wine vinegar",
            "Dried oregano, salt, pepper"
        ],
        "steps": [
            "Wash and dry all vegetables thoroughly.",
            "Combine greens, tomatoes, cucumber, olives, and red onion in a large bowl.",
            "Whisk together olive oil, red wine vinegar, oregano, salt, and pepper.",
            "Drizzle dressing over the salad and toss gently.",
            "Top with crumbled feta cheese.",
            "Serve immediately, or chill for 10 mins to let flavours meld."
        ],
        "tips": "Add the dressing just before serving to keep the greens crisp and vibrant."
    },
    "soup": {
        "name": "Creamy Tomato Basil Soup",
        "emoji": "🍲",
        "time": "40 mins",
        "difficulty": "Easy",
        "ingredients": [
            "800g canned crushed tomatoes",
            "1 onion (diced)",
            "4 cloves garlic",
            "200ml heavy cream",
            "500ml vegetable stock",
            "Fresh basil (large handful)",
            "2 tbsp olive oil",
            "Salt, pepper, pinch of sugar"
        ],
        "steps": [
            "Heat olive oil in a large pot. Sauté onion until softened, about 5 mins.",
            "Add garlic and cook for another minute until fragrant.",
            "Pour in crushed tomatoes and vegetable stock. Bring to a simmer.",
            "Cook for 20 minutes, stirring occasionally.",
            "Add fresh basil leaves and blend until smooth with an immersion blender.",
            "Stir in heavy cream and season with salt, pepper, and a pinch of sugar.",
            "Simmer gently for 5 more mins. Serve with crusty bread."
        ],
        "tips": "The pinch of sugar balances the acidity of tomatoes. Use fresh basil — dried won't give the same brightness."
    },
    "cake": {
        "name": "Classic Chocolate Lava Cake",
        "emoji": "🍫",
        "time": "30 mins",
        "difficulty": "Medium",
        "ingredients": [
            "200g dark chocolate (70%)",
            "150g unsalted butter",
            "4 eggs + 4 egg yolks",
            "150g caster sugar",
            "50g plain flour",
            "Cocoa powder (for dusting)",
            "Pinch of salt"
        ],
        "steps": [
            "Preheat oven to 220°C (425°F). Butter and dust ramekins with cocoa powder.",
            "Melt chocolate and butter together in a heatproof bowl over simmering water. Cool slightly.",
            "Whisk eggs, yolks, and sugar until pale and thick.",
            "Fold melted chocolate into egg mixture.",
            "Sift in flour and salt, fold gently until just combined.",
            "Fill ramekins ¾ full. At this point, you can refrigerate up to 24 hours.",
            "Bake for exactly 12 minutes. The edges should be set but the centre soft.",
            "Rest 1 minute, then invert onto a plate. Serve immediately."
        ],
        "tips": "The baking time is everything. 12 mins for a liquid centre — a minute more and you lose the magic lava effect."
    },
    "curry": {
        "name": "Coconut Chickpea Curry",
        "emoji": "🍛",
        "time": "35 mins",
        "difficulty": "Easy",
        "ingredients": [
            "2 cans (800g) chickpeas (drained)",
            "1 can (400ml) coconut milk",
            "400g canned chopped tomatoes",
            "1 large onion",
            "4 garlic cloves, 1 inch ginger",
            "2 tbsp curry powder",
            "1 tsp each: turmeric, cumin, coriander",
            "Fresh coriander, lime juice",
            "2 tbsp vegetable oil"
        ],
        "steps": [
            "Finely dice onion. Mince garlic and grate ginger.",
            "Heat oil in a wide pan, sauté onion for 8 minutes until golden.",
            "Add garlic, ginger, and all spices. Cook 2 minutes until fragrant.",
            "Pour in chopped tomatoes and cook down for 5 minutes.",
            "Add coconut milk and chickpeas. Stir to combine.",
            "Simmer for 15 minutes until sauce thickens.",
            "Season with salt, lime juice. Garnish with fresh coriander.",
            "Serve with basmati rice or warm naan."
        ],
        "tips": "Let the onions caramelise properly — this is the flavour base. Don't rush this step!"
    }
}

INGREDIENT_RECIPES = {
    "egg": ["pasta", "cake"],
    "tomato": ["salad", "soup", "curry"],
    "chicken": ["chicken"],
    "pasta": ["pasta"],
    "chocolate": ["cake"],
    "coconut": ["curry"],
    "chickpea": ["curry"],
    "basil": ["soup", "salad"],
    "lemon": ["chicken", "salad"],
    "feta": ["salad"]
}

GREETINGS = [
    "Hello! I'm Chef Bot, your personal recipe assistant. 👨‍🍳 Tell me what you'd like to cook, or ask me what to make with ingredients you have!",
    "Welcome to the kitchen! I'm here to help you cook something delicious. What are you craving today? 🍽️",
    "Ciao! Ready to cook something wonderful? Tell me a dish you love or what's in your fridge! 🧑‍🍳"
]

def find_recipe_by_keyword(text):
    text_lower = text.lower()
    for key in RECIPES:
        if key in text_lower:
            return RECIPES[key]
    keyword_map = {
        "spaghetti": "pasta", "carbonara": "pasta", "noodle": "pasta",
        "roast": "chicken", "poultry": "chicken",
        "salad": "salad", "mediterranean": "salad",
        "soup": "soup", "tomato": "soup",
        "cake": "cake", "chocolate": "cake", "lava": "cake", "dessert": "cake",
        "curry": "curry", "indian": "curry", "chickpea": "curry", "vegan": "curry",
        "vegetarian": "curry"
    }
    for keyword, recipe_key in keyword_map.items():
        if keyword in text_lower:
            return RECIPES[recipe_key]
    return None

def find_recipes_by_ingredients(text):
    text_lower = text.lower()
    matched_keys = set()
    for ingredient, recipe_keys in INGREDIENT_RECIPES.items():
        if ingredient in text_lower:
            matched_keys.update(recipe_keys)
    return [RECIPES[k] for k in matched_keys] if matched_keys else []

def get_bot_response(user_message):
    text = user_message.lower().strip()

    # Greetings
    if any(w in text for w in ["hello", "hi", "hey", "hola", "howdy", "start", "help"]):
        return {
            "type": "greeting",
            "message": random.choice(GREETINGS)
        }

    # Ask for all recipes
    if any(w in text for w in ["what can you make", "all recipes", "list recipes", "show me recipes", "what recipes", "menu"]):
        recipe_list = [f"{r['emoji']} **{r['name']}** ({r['time']}, {r['difficulty']})" for r in RECIPES.values()]
        return {
            "type": "list",
            "message": "Here's what I can help you cook today:",
            "items": recipe_list
        }

    # Ingredient-based search
    if any(w in text for w in ["have", "fridge", "use", "with", "ingredient", "got", "only"]):
        matched = find_recipes_by_ingredients(text)
        if matched:
            return {
                "type": "suggestions",
                "message": f"Great news! I found {len(matched)} recipe{'s' if len(matched) > 1 else ''} using those ingredients:",
                "suggestions": [{"name": r["name"], "emoji": r["emoji"], "time": r["time"]} for r in matched]
            }

    # Recipe request
    recipe = find_recipe_by_keyword(text)
    if recipe:
        return {
            "type": "recipe",
            "recipe": recipe
        }

    # Tips / difficulty
    if any(w in text for w in ["easy", "quick", "fast", "simple", "beginner"]):
        easy_recipes = [r for r in RECIPES.values() if r["difficulty"] == "Easy"]
        return {
            "type": "suggestions",
            "message": "Here are some easy, quick recipes perfect for any skill level:",
            "suggestions": [{"name": r["name"], "emoji": r["emoji"], "time": r["time"]} for r in easy_recipes]
        }

    if any(w in text for w in ["dessert", "sweet", "bake", "baking"]):
        return {
            "type": "recipe",
            "recipe": RECIPES["cake"]
        }

    if any(w in text for w in ["vegetarian", "vegan", "plant"]):
        return {
            "type": "suggestions",
            "message": "Here are some delicious plant-based options:",
            "suggestions": [
                {"name": RECIPES["salad"]["name"], "emoji": RECIPES["salad"]["emoji"], "time": RECIPES["salad"]["time"]},
                {"name": RECIPES["soup"]["name"], "emoji": RECIPES["soup"]["emoji"], "time": RECIPES["soup"]["time"]},
                {"name": RECIPES["curry"]["name"], "emoji": RECIPES["curry"]["emoji"], "time": RECIPES["curry"]["time"]}
            ]
        }

    # Fallback
    return {
        "type": "fallback",
        "message": "Hmm, I'm not sure about that one! 🤔 Try asking me for a specific dish like **pasta**, **chicken**, **curry**, or **cake** — or tell me what ingredients you have and I'll find something for you!"
    }


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
    response = get_bot_response(user_message)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
