import re

# Local import
from constants import STORE_LIST


""" 
Module to build the regex used to search 
matching product's stores with constants.py 
"""


def build_regex():
    """
    Class to build the regex used to search
    matching product's stores with constants.py
    Info: Allow the use of any non letter in the constants.py stores list.
    """
    # Replace any non word character by his regular expression value ( \W )
    # Escaped two times otherwise there is an error
    store_list = [re.sub(r'\W', '\\\\W', store) for store in STORE_LIST]
    regex_stores = r'(' + "|".join(store_list) + r')'
    return regex_stores
