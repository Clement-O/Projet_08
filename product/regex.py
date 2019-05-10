import re

# Local import
from constants import STORE_LIST


def build_regex():
    # Replace any non word character by his regular expression value ( \W )
    # Escaped two times otherwise there is an error
    store_list = [re.sub(r'\W', '\\\W', store) for store in STORE_LIST]
    regex_stores = r'(' + "|".join(store_list) + r')'
    return regex_stores
