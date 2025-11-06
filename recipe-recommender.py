# Imports
import numpy as np
import pandas as pd

# #Data set
# URL: https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life \\
# 
# Relevant columns: Ingredients \\
# 
# For dietary restrictions: determine whether the recipe meets dietary restrictions based on the ingredients list. For example, you know that refried beans recipe is vegan if the recipe does not use lard. \\
# 
#   Question: what learning algorithm should be used to have AI recognize that
# the recipe meets dietary restrictions?

# ## Load and inspect the dataset

#Load CSV into DataFrame
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/recipes.csv')
df.head()

# ##Check the dataframe for null values and duplicates in recipe_name and ingredients column


# check the DataFrame for columns, null values and duplicates.
#recipe_name had some duplicate values. ingredients column did not have null or duplicate values
# df.info()

# null_ingredients = int(df['ingredients'].isnull().sum())
# duplicate_ingredients = int(df.duplicated().sum())

# null_names = int(df['recipe_name'].isnull().sum())
# duplicate_names = int(df['recipe_name'].duplicated().sum())
# print(f"recipe_name - Null values: {null_names}, Duplicates: {duplicate_names} ")
# print(f"ingredients - Null values: {null_ingredients}, Duplicates: {duplicate_ingredients} ")


# Find and delete recipes with duplicated names.

# Find recipe names that appear more than once
name_counts = df['recipe_name'].value_counts()
duplicates = name_counts[name_counts > 1]

# Display them
# print(f"Duplicate recipe names:\n{duplicates}")

# # Filter rows with duplicate recipe names
# df_duplicates = df[df['recipe_name'].isin(duplicates.index)]

# # Sort for easier viewing
# df_duplicates = df_duplicates.sort_values('recipe_name')

# # View a sample
# df_duplicates[['recipe_name', 'ingredients']].tail(10)


# # check if duplicate recipes also have the same ingredient list (true duplicates)

# # Group by recipe name and count unique ingredients per group
# duplicates_with_diff = df.groupby('recipe_name')['ingredients'].nunique()

# # Filter to show recipe names that have more than 1 unique ingredients entry
# conflicting_duplicates = duplicates_with_diff[duplicates_with_diff > 1]

# # Display them
# print(f"Number of recipe names with different ingredients: {len(conflicting_duplicates)}")
# print(conflicting_duplicates.head())

# Since all the recipes with duplicate names also have duplicate ingredient list, drop recipes with duplicate names.
df = df.drop_duplicates(subset='recipe_name').reset_index(drop=True)
print(f"Remaining duplicate names: {df['recipe_name'].duplicated().sum()}")

# ## Format ingredients column to a list

#Preprocess ingredients column in DataFrame to create a list of ingredients for the algorithm to use
import re

cleaned_ingredients = []

for row in df['ingredients']:
  ingredients = row.lower()
  ingredients = re.sub(r'[^\w\s,]','',ingredients).split(',')
  ingredients = [item.strip() for item in ingredients if item.strip()]
  cleaned_ingredients.append(ingredients)

df['ingredients_clean'] = cleaned_ingredients
print(cleaned_ingredients[0])

# show example of ingredients column. They are a string of comma-separated items, lower case except for proper capitalization (e.g. Granny Smith apples)
df['ingredients'].head(2)

# # Implement Backend Functions
# === Constants: Dietary Rules and Ingredient Traits ===
# Ingredient tags of common allergens and dietary restriction foods
INGREDIENT_TRAITS = {
    "dairy": ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'ghee'],
    "meat": ['chicken', 'beef', 'pork', 'lamb', 'bacon', 'chicken stock', 'beef stock'],
    "seafood": ['fish', 'shrimp', 'crab', 'lobster', 'anchovy', 'squid', 'clam', 'surimi'],
    "eggs": ['egg', 'egg whites', 'egg yolk'],
    "gluten": ['wheat', 'barley', 'rye', 'malt'],
    "nuts": ['almonds', 'peanuts', 'walnuts', 'cashews'],
    "animal_products": ['gelatin', 'honey', 'lard'],  # for vegan
    "soy": ['soy', 'tempeh', 'tofu', 'soy milk', 'soy sauce', 'miso', 'edamame']
}

# Dietary restrictions from ingredient tags. EX: vegan diet would exclude meat, seafood, dairy, and animal products
DIETARY_RESTRICTIONS = {
    "vegan": ['dairy', 'meat', 'seafood', 'eggs', 'animal_products'],
    "vegetarian": ['meat', 'seafood'],
    "gluten_free": ['gluten'],
    "nut_free": ['nuts'],
    "dairy_free": ['dairy']
}


"""
Accepts a list of user-provided restrictions (e.g. 'vegan', 'dairy', 'soy')
and returns a full list of excluded ingredients.
"""
def get_excluded_ingredients(selected_diets):
  excluded = set()
  for item in selected_diets:
    item = item.lower().strip()

    if item in DIETARY_RESTRICTIONS:
      traits = DIETARY_RESTRICTIONS.get(item, [])
      for trait in traits:
          excluded.update(INGREDIENT_TRAITS.get(trait, []))

    elif item in INGREDIENT_TRAITS:
      excluded.update(INGREDIENT_TRAITS[item])

    else:
      excluded.add(item)
  return excluded

# Filter out recipes in the dataset containing ingredients excluded by the user
def filter_recipes(recipes, excluded_ingredients):
    filtered = []
    for recipe in recipes:
        ingredients = [i.lower() for i in recipe['ingredients']]
        if not any(ingredient in ingredients for ingredient in excluded_ingredients):
            filtered.append(recipe)
    return filtered


# TODO: Incorporate this to the rest of the source code. Reorganize cells in this project first

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

"""
    Recommend top 5 recipes based on user-provided ingredients and dietary restrictions.
    This function assumes that recipes are filtered to remove recipes that contain excluded ingredients.
    Uses bag-of-words model with cosine similarity to match the user's desired ingredients against the ingredient list of recipes.

    Args:
       1. recipes (list of dict): Recipe dataset filtered by excluded ingredients
       2. included_ingredients (list of str): Ingredients the user wants to include
    Returns:
       List of dict: Top 5 recipe dictionaries ranked by similarity to the included ingredients.
"""
def recommend_recipe(recipes, included_ingredients):
  texts = [' '.join(r['ingredients']) for r in recipes]

  vectorizer = CountVectorizer()
  recipe_vectors = vectorizer.fit_transform(texts)

  user_query = ' '.join(included_ingredients)
  user_vector = vectorizer.transform([user_query])

  similarities = cosine_similarity(user_vector, recipe_vectors).flatten()
  ranked = sorted(zip(recipes, similarities), key=lambda x:x[1], reverse=True)
  return ranked[:5]

# # Implement UI
# 
# For future iterations: consider using AI to guess user's restricted ingredients.

# Prompt the user to enter several ingredients and dietary restrictions. Conver this to individual ingredients to exclude in the recipe.
ingredients_input = input("Enter the ingredients (comma separated): ")
included_ingredients = [token.strip().lower() for token in ingredients_input.split(',') if token.strip()]

excluded_input = input("Enter ingredients to exclude. You can also enter dietary restrictions (comma separated): ")
excluded_tokens = [token.strip().lower() for token in excluded_input.split(',') if token.strip()]

selected_diets = [] # ingredients excluded under known dietary restrictions

for token in excluded_tokens:
  selected_diets.append(token)

excluded_ingredients = get_excluded_ingredients(selected_diets)

print(f"\nIngredients to include: {included_ingredients}")
print(f"Ingredients to exclude (including dietary restrictions): {sorted(excluded_ingredients)}")

filter_recipes(df['ingredients_clean'], excluded_ingredients)
# top_5_recipes = recommend_recipe(filter_recipes(df['ingredients_clean'], excluded_ingredients), included_ingredients)
# print(top_5_recipes)
