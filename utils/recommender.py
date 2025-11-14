# Core logic of the app. Covers filtering, recommending, and similarity scoring of the recipes

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.constants import DIETARY_RESTRICTIONS, INGREDIENT_TRAITS

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

"""
Return a DataFrame with recipes that do NOT contain any excluded ingredients.

Args:
    df (DataFrame): The full recipes dataset with 'ingredients_clean' column.
    excluded_ingredients (list or set): Ingredients to avoid.

Returns:
    DataFrame: Filtered recipes.
"""
def filter_recipes(df, excluded_ingredients):
    excluded_lower = [ex.lower() for ex in excluded_ingredients]
    # Boolean mask: True for rows we want to keep
    mask = df['ingredients_clean'].apply(
        lambda ingr_list: not any(ex in ing.lower() for ing in ingr_list for ex in excluded_lower)
    )
    # Return copy of masked dataframe
    return df[mask].copy()

"""
    Recommend top 5 recipes based on user-provided ingredients and dietary restrictions.
    This function assumes that recipes are filtered to remove recipes that contain excluded ingredients.
    Uses bag-of-words model with cosine similarity to match the user's desired ingredients against the ingredient list of recipes.

    Args:
       1. recipes (list of dict): Recipe dataset filtered by excluded ingredients
       2. included_ingredients (list of str): Ingredients the user wants to include
    Returns:
       DataFrame: Top 5 recipes ranked by similarity to the included ingredients.
"""
def recommend_recipe(df, included_ingredients):
  # Convert list of ingredients to a single string for each recipe
  texts = [' '.join(ingr) for ingr in df['ingredients_clean']]
  vectorizer = CountVectorizer()
  recipe_vectors = vectorizer.fit_transform(texts)

  user_query = ' '.join(included_ingredients)
  user_vector = vectorizer.transform([user_query])

  similarities = cosine_similarity(user_vector, recipe_vectors).flatten()

  # Add similarity scores to DataFrame
  df = df.copy()
  df['similarity'] = similarities

  # Return top 5 recipes
  return df.sort_values('similarity', ascending=False).head(5)