import re

# Third party import
import openfoodfacts

# Local import
from product import REGEX_STORES


class SubstituteQueries:
    # p = product(s).

    def __init__(self, product_param):
        self.p_param = product_param
        self.head_p = {}
        self.products = []

    def query_off(self):
        advanced_search = openfoodfacts.products.advanced_search({
            "search_terms": "",
            "tagtype_0": "countries",
            "tag_contains_0": "contains",
            "tag_0": "france",
            "tagtype_1": "states",
            "tag_contains_1": "contains",
            "tag_1": "complete",
            "tagtype_2": "categories",
            "tag_contains_2": "contains",
            "tag_2": self.p_param['cat_1'],
            "tagtype_3": "categories",
            "tag_contains_3": "contains",
            "tag_3": self.p_param['cat_2'],
            "page_size": 150,
            "page": "1",
            "json": "1"
        })
        return advanced_search['products']

    def get_head_product(self, products):
        for p in products:
            try:
                if p['nutrition_grades'] not in self.p_param['ng']:
                    self.head_p = {
                        'img': p['selected_images']['front']['display']['fr']
                    }
                    break
            except KeyError:
                continue
        return self.head_p

    def get_substitute(self, products):
        p_id = []
        for p in products:
            try:
                if p['nutrition_grades'] in self.p_param['ng']:
                    if p['id'] not in p_id:
                        stores = ' '.join(p['stores_tags'])
                        if stores:
                            if re.search(REGEX_STORES, stores, flags=re.I):
                                p_id.append(p['id'])
                                self.products.append(p)
            except KeyError:
                continue
        return self.products
