# RecipeRecommender
A Streamlit application that suggests recipes based on the ingredients and dietary restrictions.

## Features 
- Filters recipes by excluded ingredients and dietary restrictions.
- Recommends top 5 recipes based on included ingredients.
- Download recommended recipes as a text file.
- Handles both single and multiple ingredient inputs.

## How to use
1. Enter the ingredients you want to use.
2. Enter the ingredients or ingredient categories you want to skip.
3. The app shows top 5 recipes that best match the criteria. You can download the list of recipes via "Download Recipe" button.

### Examples

**1. Exclude specific ingredients**  
- Included ingredients: `apple, sugar, cinnamon`  
- Excluded ingredients: `dairy`  
- The app will suggest recipes containing apple, sugar, and cinnamon, while skipping recipes that contain dairy.

**2. Exclude an ingredient group**  
- Included ingredients: `tofu, rice`  
- Excluded ingredient category: `soy`  
- The app will suggest recipes with tofu and rice, but skip recipes that contain any soy-based ingredients.

## Dataset
- Uses Better Recipe Dataset on Kaggle: 
    - URL: https://www.kaggle.com/datasets/thedevastator/better-recipes-for-a-better-life

## Requirements / Setup
Install dependencies using the following command: 
```pip install -r requirements.txt```