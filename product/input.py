from collections import Counter

# Third party import
import openfoodfacts

# Local import
from constants import NUTRITION_GRADES_LIST

""" Module to determine the product researched by the user """


class UserInput:
    """
    Class to determine the product researched by the user.
    1. Query OpenFoodFacts.
    2. Loop over the (max) 20 products returned
    3. For each product save the first and 2 last english categories &
        nutrition grades
    4. Finally use Counter to get the most used categories & nutrition grades
    """
    # cat = category(ies). ng = nutrition grades. p = product(s).
    # tmp = temporary. lst = list(s). qry = query(ies).

    def __init__(self, query):
        self.qry = query

    @staticmethod
    def recursive_count(lst):
        lst_counts = Counter(lst)
        return lst_counts.most_common(1)[0][0]

    def get_product(self):
        cat_first = []
        cat_second = []
        cat_third = []
        ng_p = []

        # API Query
        p = openfoodfacts.products.search(self.qry)
        if p['count'] > 0:
            for i in range(0, len(p['products'])):
                try:
                    cat_en = [
                        category for category in
                        p['products'][i]['categories_hierarchy']
                        if category[:2] == "en"
                    ]
                    if len(cat_en) >= 3:
                        cat_first.append(cat_en[0])
                        cat_second.append(cat_en[len(cat_en) - 2])
                        cat_third.append(cat_en[len(cat_en) - 1])
                except KeyError:
                    continue

                try:
                    tmp_ng = p['products'][i]['nutrition_grades']
                    if tmp_ng not in ng_p:
                        ng_p.append(tmp_ng)
                except KeyError:
                    continue

            # Substitute nutrition_grade determination
            try:
                ng_sorted = sorted(ng_p)
                ng_worst = ng_sorted[len(ng_sorted) - 1]
                ng_index = NUTRITION_GRADES_LIST.index(ng_worst)
                nutrition_grades = NUTRITION_GRADES_LIST[:ng_index]

                p_param = {
                    "cat_1": self.recursive_count(cat_first),
                    "cat_2": self.recursive_count(cat_second),
                    "cat_3": self.recursive_count(cat_third),
                    "ng": nutrition_grades
                }
            except IndexError:
                p_param = {}

            return p_param
