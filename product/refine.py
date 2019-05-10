class RefineSubstitute:
    # sub = substitute(s).

    def __init__(self, products):
        self.products = products

    def product_infos(self):
        sub = []
        for p in self.products:
            try:
                product_info = {
                    "id": p['id'],
                    "name": p['product_name'],
                    "ng": p['nutrition_grades'],
                    "img": p['selected_images']['front']['display']['fr'],
                    "link_off": p['url'],
                    'energy': p['nutriments']['energy_100g'],
                    'fat': p['nutriments']['fat_100g'],
                    'saturated_fat': p['nutriments']['saturated-fat_100g'],
                    'carbohydrate': p['nutriments']['carbohydrates_100g'],
                    'sugars': p['nutriments']['sugars_100g'],
                    'proteins': p['nutriments']['proteins_100g'],
                    'salt': p['nutriments']['salt_100g'],
                }
                sub.append(product_info)
            except KeyError:
                continue
        sub = sorted(sub, key=lambda s: s['ng'])
        return sub
