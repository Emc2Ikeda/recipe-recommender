# Stores all constants used in the app, including list of allergens & ingredient types

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