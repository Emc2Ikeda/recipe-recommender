# Preprocesses data for recipe recommender

import numpy as np
import pandas as pd
import re

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

    # # Filter rows with duplicate recipe names
    df_duplicates = df[df['recipe_name'].isin(duplicates.index)]
    df_duplicates = df_duplicates.sort_values('recipe_name')
    df_duplicates[['recipe_name', 'ingredients']].tail(10)

    # check if duplicate recipes also have the same ingredient list (true duplicates)

    # Group by recipe name and count unique ingredients per group
    duplicates_with_diff = df.groupby('recipe_name')['ingredients'].nunique()

    # Filter to show recipe names that have more than 1 unique ingredients entry
    conflicting_duplicates = duplicates_with_diff[duplicates_with_diff > 1]

    # Since all the recipes with duplicate names also have duplicate ingredient list, drop recipes with duplicate names.
    df = df.drop_duplicates(subset='recipe_name').reset_index(drop=True)
    print(f"Remaining duplicate names: {df['recipe_name'].duplicated().sum()}")
    return df

df = load_data()
print(len(df))

deleted_duplicate_df = delete_duplicate(df)
print(len(deleted_duplicate_df))

# Format ingredients column to a list
def get_ingredients_list(df):
    cleaned_ingredients = []

    for row in df['ingredients']:
        ingredients = row.lower()
        ingredients = re.sub(r'[^\w\s,]','',ingredients).split(',')
        ingredients = [item.strip() for item in ingredients if item.strip()]
        cleaned_ingredients.append(ingredients)

    df['ingredients_clean'] = cleaned_ingredients
    return cleaned_ingredients

cleaned_ingredients = get_ingredients_list(df)
print(cleaned_ingredients)