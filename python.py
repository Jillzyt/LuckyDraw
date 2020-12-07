from random import randrange
import pandas as pd
import random
import numpy as np
from datetime import date
from connection import MySQLDatabase

# Input
print("What's the name of the excel?")
excel_name = input()

# Read the csv
# print(excel_name)
df = pd.read_csv(excel_name)


# Convert dataframe to dict()
hashmap = df.to_dict('records')

totalPoints = 0
# Loop through dictionary
for entry in hashmap:
    totalPoints += entry['Total Points']

print(totalPoints)
for entry in hashmap:
    entry['probability'] = entry['Total Points'] / totalPoints


def get_winner(winning_probability):
    cumulative_probability = 0
    for entry in hashmap:
        cumulative_probability = cumulative_probability + \
            entry['probability']
        if winning_probability <= cumulative_probability and cumulative_probability != 0:
            return entry['First Name']

    return "no winner"


def convertTuple(winner_tuple):
    winner_tuple_in_str = ""
    winner_tuple_in_str = winner_tuple_in_str.join(str(winner_tuple))
    return winner_tuple_in_str


# Update in database
x = MySQLDatabase()
for entry in hashmap:
    if (pd.isnull(entry['First Name'])):
        entry['First Name'] = ""
    x.add_user(entry['First Name'], entry['Email'],
               entry['Total Points'], entry['probability'])


# Compute the winner
random.seed(a=date.today(), version=2)
winning_probability = random.uniform(0, 1)
name_of_winner = get_winner(winning_probability)
winner_tuple = x.retrieve_user(name_of_winner)
x.add_luckydrawrecord(name_of_winner)
winner_tuple_in_str = convertTuple(winner_tuple)


# Store in database
x = MySQLDatabase()
print("The winner is :", winner_tuple_in_str)
