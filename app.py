import streamlit as st
from utils.data import load_and_preprocess_data
from utils.recommender import filter_recipes, get_excluded_ingredients

st.title("Recipe Recommender")

# load preprocessed data
df = load_and_preprocess_data()
st.write(df.head(5))

# Prompt the user to enter several ingredients and dietary restrictions. Conver this to individual ingredients to exclude in the recipe.
ingredients_input = st.text_input("Enter the ingredients (comma separated): ")
included_ingredients = [token.strip().lower() for token in ingredients_input.split(',') if token.strip()]

excluded_input = st.text_input("Enter ingredients to exclude. You can also enter dietary restrictions (comma separated): ")
excluded_tokens = [token.strip().lower() for token in excluded_input.split(',') if token.strip()]

selected_diets = [] # ingredients excluded under known dietary restrictions

for token in excluded_tokens:
  selected_diets.append(token)

excluded_ingredients = get_excluded_ingredients(selected_diets)

st.write(f"\nIngredients to include: {included_ingredients}")
st.write(f"Ingredients to exclude (including dietary restrictions): {sorted(excluded_ingredients)}")

filtered_recipes = filter_recipes(df, excluded_ingredients)
st.write(filtered_recipes.head())
# # top_5_recipes = recommend_recipe(filter_recipes(df['ingredients_clean'], excluded_ingredients), included_ingredients)
# # print(top_5_recipes)