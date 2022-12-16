import requests
import re
import pandas as pd

def list_all(search='Ingredient'):
    '''
    Searches for either all the possible 'Category', 'Area', or 'Ingredient' from TheMealDB API.

    Parameters
    ----------
    search: str
        A string, from one of the 3 search filters.

    Returns
    -------
    search_list: list[str]
        A list, returns a list of all the possible searches from 'Category', 'Area', or 'Ingredient' from TheMealDB API

    Example
    -------
    >>> search = str('Ingredient')
    >>> list_all('Ingredient')
        output: list[str]
            ['Tomato',
            'Chicken',
            'Lettuce']
    '''

    search_list = ['Category', 'Area', 'Ingredient']
    assert isinstance(search, str) and search in search_list, f'search is {search}, search should be one of {search_list}'

    params = {'i': 'list'}
    if search == 'Category': 
        params['c'] = params.pop('i')
    elif search == 'Area':
        params['a'] = params.pop('i')
    elif search == 'Ingredient':
        params = params

    try:
        req = requests.get(url='https://www.themealdb.com/api/json/v1/1/list.php', params=params)
        
        # create a dictionary from the request
        search_dict = dict(req.json())['meals']
        search_str = 'str' + search
        search_range = range(0, len(search_dict), 1)
        search_list = []

        # iterate through all the values in dictionary
        for i in search_range:
            search_list.append(search_dict[i][search_str])

        # sort list alphabetically
        search_list.sort()

        return search_list
        
    except:
        if req.status_code == 404:
            print(f'Error: {req.status_code}, the URL is invalid')
        elif req.status_code >= 500:
            print(f'Error: {req.status_code}, server side issue')
        else:
            print(f'Error: {req.status_code}')



def define_ingredient(ingredient=''):
    '''
    Provides the definition of an ingredient if avaliable from TheMealDB API, also returns ingredients synonomous to input if no direct match is found. 
    
    Parameters
    ----------
    ingredient: str
        A string, an ingredient.

    Returns
    -------
    search_list: dict[str]
        A dictionary, returns a dictionary with the name of the ingredient as the key and the definition as the value.

    Example
    -------
    >>> ingredient = str('beef')
    >>> define_ingredient(ingredient='beef')
        output: dict[str]
            {'Beef': 'Beef is the culinary name for meat from cattle, particularly skeletal muscle.'}
    '''

    assert isinstance(ingredient, str), f'ingredient is {ingredient}, ingredient should a string'
    
    # lowercase search
    ing = ingredient.lower()

    # make api request for all the ingredients
    req = requests.get(url='https://www.themealdb.com/api/json/v1/1/list.php', params={'i': 'list'})
    # raise exception for HTTP error
    if req.status_code != 200:
        raise Exception(f'Error: {req.status_code}')
        
    # create a dictionary from the request
    ing_dict = dict(req.json())['meals']
    ing_range = range(0, len(ing_dict), 1)
    ing_list = []

    # iterate through all the values in dictionary
    for i in ing_range:
        ing_list.append(ing_dict[i]['strIngredient'])

    # lowercase all the words in list
    ing_list = [c.lower() for c in ing_list]

    # find the index for ingredient being searched
    # 2 conditions: one on one match or if word is general returns all the ingredients that contains searched word
    ind_list = []
    if (ing in ing_list):
        ing_index = ing_list.index(ing)
        ind_list.append(ing_index)
    elif (ing not in ing_list): 
        # ind_list = [ing_list.index(a) for a in ing_list if ing in a]
        exp = r'.*?\b' + re.escape(ing) + r'[s|es]?\b.*?'
        ind_list = [a for a, x in enumerate(ing_list) if re.match(exp, x)]
        
    # find definition using index
    definition_dict = {}
    for l in range(0, len(ind_list)):
        ind = ind_list[l]
        name = ing_dict[ind]['strIngredient']
        definition = ing_dict[ind]['strDescription']
        
        # clean up definition string
        if definition == None:
            definition = 'No definition avaliable'
        else:
            definition = re.sub('\r\n', ' ', definition)

        definition_dict.update({name: definition})

    # catch all for empty response
    assert len(definition_dict) > 0, f'{ingredient} is not an ingredient found on TheMealBD\'s list of ingredients, alternatively please check your spelling'

    return definition_dict



def filter_recipes(ingredient=''):
    '''
    Filter recipes on The MealDB by an ingredient. 

    Parameters
    ----------
    ingredient: str
        A string, an ingredient.

    Returns
    -------
    recipe_list: list[str]
        A list, returns a list of all the recipe names from The MealDB that contains the ingredient that is searched for.

    Example
    -------
    >>> ingredient = str('chilli')
    >>> filter_recipies(ingredient='chilli')
        output: list[str]
            ['Kung Po Prawns', 'Mee goreng mamak', 'Roti john']
    '''
    
    assert isinstance(ingredient, str), f'ingredient is {ingredient}, ingredient should a string'
    
    req = requests.get(url='https://www.themealdb.com/api/json/v1/1/filter.php', params={'i': ingredient})
    if req.status_code != 200:
        raise Exception(f'Error: {req.status_code}')

    dict_ingredient = dict(req.json())['meals']
    recipe_list = []

    if dict_ingredient != None:
        for m in dict_ingredient:
            recipe_list.append(m['strMeal'])
    else:
        # if there is no one on one match
        # find exact term using define_ingredient
        gen_ing = define_ingredient(ingredient)
        gen_list = []
        for g in gen_ing:
            gen_list.append(g)
            
        # iterate through the list of ingredients
        for i in gen_list:
            req_general = requests.get(url='https://www.themealdb.com/api/json/v1/1/filter.php', params={'i': i})
            if req_general.status_code != 200:
                raise Exception(f'Error: {req_general.status_code}')

            dict_general = dict(req_general.json())['meals']
            if dict_general != None:
                for n in dict_general:
                    recipe_list.append(n['strMeal'])

    return recipe_list



def recipe_ingredients(recipe_name=''):
    '''
    Provides the ingredients and instructions for a specific recipe from The MealDB. Takes single string output from filter_recipes() as input.

    Parameters
    ----------
    recipe_name: str
        A string, name of a recipe. 

    Returns
    -------
    ingredients_measurement: pandas.DataFrame
        A DataFrame, returns a dataframe with 2 columns for a specific recipe.

    instructions: dict[str]
        A Dictionary, returns a dictionary containing the the name of the recipe as the key and the instructions for the recipe as the value.

    Example
    -------
    >>> recipe_name = str('Fresh sardines')
    >>> recipe_ingredients(recipe_name='Fresh sardines')
        output: 
            list[str]
                Index:
                    RangeIndex
                Columns:
                    Name: Ingredients, dtype=object
                    Name: Measurement, dtype=object
            dict[str]
                {'Fresh sardines': 'Wash the fish under the cold tap. Roll in the flour and deep fry in oil until crispy. Lay on kitchen towel to get rid of the excess oil and serve hot or cold with a slice of lemon.'}
    '''
    
    assert isinstance(recipe_name, str), f'ingredient is {recipe_name}, ingredient should a string'

    try:
        req = requests.get(url='https://www.themealdb.com/api/json/v1/1/search.php', params={'s': recipe_name})
        dict_recipe = dict(req.json())['meals'][0]
        
        ingredients_list = []
        measurement_list = []

        for i in range(1, 21, 1):
            ingredient = 'strIngredient' + str(i)
            measurement = 'strMeasure' + str(i)

            # extract ingredients
            if dict_recipe[ingredient] != '' and dict_recipe[ingredient] != None:
                ingredients_list.append(dict_recipe[ingredient])

            # extract measurment for ingredients
            if dict_recipe[measurement] != '' and dict_recipe[measurement] != None:
                measurement_list.append(dict_recipe[measurement])

        # create dataframe
        ingredients_measurement = pd.DataFrame(list(zip(ingredients_list, measurement_list)), 
                                    columns=['Ingredients', 'Measurements'])

        # obtain recipe instructions and recipe name
        instructions_raw = dict_recipe['strInstructions']
        recipe_name = dict_recipe['strMeal']
        # clean up instructions
        instructions_c = re.sub(r'\r\n', ' ', instructions_raw)
        instructions = {recipe_name: instructions_c}

        return ingredients_measurement, instructions
        
    except:
        if req.status_code == 404:
            print(f'Error: {req.status_code}, the URL is invalid')
        elif req.status_code >= 500:
            print(f'Error: {req.status_code}, server side issue')
        else:
            print(f'Error: {req.status_code}')