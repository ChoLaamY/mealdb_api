# mealdb_api 

![](https://github.com/ChoLaamY/mealdb_api/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ChoLaamY/mealdb_api/branch/main/graph/badge.svg)](https://codecov.io/gh/ChoLaamY/mealdb_api) ![Release](https://github.com/ChoLaamY/mealdb_api/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/mealdb_api/badge/?version=latest)](https://mealdb_api.readthedocs.io/en/latest/?badge=latest)

Python package that allows users to interact with The MealDB API, filtering by ingredients, obtaining recipe instrictions, and other functions.
Find more details on The MealDB documentation [here](https://www.themealdb.com/api.php) and access the webpage [here](https://www.themealdb.com/). 

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ mealdb_api
```

## Features

* API wrapper for the free MealDB API
* access to ingredients, categories, and areas from the MealDB
* filter for recipes by ingredient, category, and area
* returns recipe ingredients and instructions as a dataframe and dictionary respectiviely

## Dependencies

* request
* re
* pandas

## Usage

see [vignette](vignettes/how_to_mealdb_api.ipynb) for examples of using mealdb_api functions


## Documentation

The official documentation is hosted on Read the Docs: https://mealdb_api.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/ChoLaamY/mealdb_api/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
