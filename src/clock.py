import os
import json


# read the quotes to a python dict
with open("quotes.json", "r") as f:
    quotes = json.load(f)