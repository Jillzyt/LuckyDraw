# Randomizer

Randomizer is an application that helps to draw a winner base on the number of lots he have.

A excel sheet is to be parsed with the following columns:
Position,First Name,Email,Total Points

The randomizer used the roulette wheel selection to ensure all the probabilities based on the number of lots.

https://en.wikipedia.org/wiki/Fitness_proportionate_selection

## Installation

Use the package manager [pip] to install the required dependencies.

```bash
pipenv install
```

Create a virtual environment to run your python

```
pipenv shell
```

## Usage

To set up the database, modify the configurations in connection.py under config

Set up the database:

```
python connection.py
```

Run the file:

```
python python.py
```
