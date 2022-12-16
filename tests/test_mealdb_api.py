from mealdb_api import mealdb_api
import pytest
from mealdb_api import list_all, define_ingredient, filter_recipes, recipe_ingredients

# test functions for list_all
def test_list_all_assert():
    with pytest.raises(Exception):
        list_all('hello')

# test functions for define_ingredient
def test_define_ingredient_assert():
    with pytest.raises(Exception):
        define_ingredient(5)

@pytest.mark.parametrize('example_def, expected_def', [
    ('milk', 'No definition avaliable'),
    ('sugar', 'No definition avaliable'),
    ('ice', 'No definition avaliable'),
    ('chili','No definition avaliable')
])

def test_define_ingredient(example_def, expected_def):
    define = define_ingredient(example_def)
    key = list(define.keys())
    assert expected_def == define[key[0]]

# test functions for filter_recipes
def test_filter_recipe_assertion():
    with pytest.raises(AssertionError):
        filter_recipes('table')

@pytest.mark.parametrize('example_fil, expected_fil', [
    ('blackberries', ['Fruit and Cream Cheese Breakfast Pastries', 'Summer Pudding']),
    ('sardine', ['Fresh sardines', 'Grilled Portuguese sardines']),
    ('oregano', ['Braised Beef Chilli', 'Pizza Express Margherita'])
])

def test_filter_recipes(example_fil, expected_fil):
    assert expected_fil == filter_recipes(example_fil)

# test functions for recipe_ingredients
def test_recipe_ingredients_assert():
    with pytest.raises(AssertionError):
        recipe_ingredients(900)

@pytest.mark.parametrize('example_rec, expected_rec', [
    ('Pizza Express Margherita', 11),
    ('Massaman Beef curry', 13),
    ('Cajun spiced fish tacos', 12),
    ('Sushi', 7),
    ('Duck Confit', 6)
])

def test_recipe_ingredients(example_rec, expected_rec):
    df = recipe_ingredients(example_rec)[0]
    assert expected_rec == len(df)
