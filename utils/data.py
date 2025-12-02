# Preprocesses data for recipe recommender

import numpy as np
import pandas as pd
import re
import io

# #Data set
# URL: https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life \\
# 
# Relevant columns: Ingredients \\
# 
# For dietary restrictions: determine whether the recipe meets dietary restrictions based on the ingredients list. For example, you know that refried beans recipe is vegan if the recipe does not use lard. \\

#Load CSV into DataFrame
def load_data():
    return pd.read_csv('utils/recipes.csv')

# Find and delete recipes with duplicated names. Return updated dataframe.
def delete_duplicate(df):
    # Find recipe names that appear more than once
    name_counts = df['recipe_name'].value_counts()
    duplicates = name_counts[name_counts > 1]

    # Filter rows with duplicate recipe names
    df_duplicates = df[df['recipe_name'].isin(duplicates.index)]
    df_duplicates = df_duplicates.sort_values('recipe_name')

    # Since all the recipes with duplicate names also have duplicate ingredient list, drop recipes with duplicate names.
    df = df.drop_duplicates(subset='recipe_name').reset_index(drop=True)
    return df

# Format ingredients column to a list and add to the DataFrame
def add_ingredients_clean(df):
    cleaned_ingredients = []

    for row in df['ingredients']:
        ingredients = row.lower()
        ingredients = re.sub(r'[^\w\s,]','',ingredients).split(',')
        ingredients = [item.strip() for item in ingredients if item.strip()]
        cleaned_ingredients.append(ingredients)

    df['ingredients_clean'] = cleaned_ingredients

# Return preprocessed data to Streamlit app
def load_and_preprocess_data():
    df = load_data()
    df = delete_duplicate(df)
    add_ingredients_clean(df)
    return df

# Convert Dataframe from recommend_recipe() to downloadable txt file
def save_recipes(df):
    text_data = df.to_string(index=False)
    return text_data