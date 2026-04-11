import streamlit as st
from utils.data import load_and_preprocess_data, trim_recipe_df, format_recipe_for_download
from utils.recommender import filter_recipes, get_excluded_ingredients, tf_idf_recommend, recommend_recipe_embeddings, tf_idf_recommend

st.title("Recipe Recommender")

model_choice = st.radio(
    "Choose ranking method",
    ["TF-IDF", "Sentence Embeddings"]
)

# load preprocessed data
df = load_and_preprocess_data()
st.write("Recipe dataset loaded.")

# Prompt the user to enter several ingredients and dietary restrictions. Conver this to individual ingredients to exclude in the recipe.
ingredients_input = st.text_input("Enter the ingredients (comma separated): ")
included_ingredients = [token.strip().lower() for token in ingredients_input.split(',') if token.strip()]

excluded_input = st.text_input("Enter ingredients to exclude. You can also enter dietary restrictions (comma separated): ")
excluded_tokens = [token.strip().lower() for token in excluded_input.split(',') if token.strip()]

selected_diets = [] # ingredients excluded under known dietary restrictions

for token in excluded_tokens:
  selected_diets.append(token)

# List of all the ingredients to exclude
excluded_ingredients = get_excluded_ingredients(selected_diets)

st.write(f"\nIngredients to include: {included_ingredients}")
st.write(f"Ingredients to exclude (including dietary restrictions): {sorted(excluded_ingredients)}")

if excluded_ingredients:
  filtered_recipes = filter_recipes(df, excluded_ingredients)
else:
  filtered_recipes = df

# checkbox to include all ingredients in the recipe recommendations
require_all_ingredients = st.checkbox("Include all ingredients in the recipe recommendations")

if st.button("Get Recipe Recommendations"):
  results = None
  if model_choice == "Sentence Embeddings":
    st.write("Using Sentence Embeddings for recommendation...")
    results = recommend_recipe_embeddings(
        filtered_recipes,
        included_ingredients,
        require_all_ingredients
    )
  else:
    st.write("Using TF-IDF for recommendation...")
    results = tf_idf_recommend(
        filtered_recipes,
        included_ingredients,
        require_all_ingredients
    )

  st.write("Recommendations: ")
  if results.empty or results is None:
    st.write("No recipes found with the given criteria.")
  else:
    st.write(results.head())
  
  # st.write("Trimmed Recipes for Download: ")
  # trimmed_recipes = trim_recipe_df(top_5_recipes)
  # st.write(trimmed_recipes.head())

  # text_file = format_recipe_for_download(trimmed_recipes)
  # st.download_button(data=text_file, label="Download Recipes", file_name="recipes.txt")