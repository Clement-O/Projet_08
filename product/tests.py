from django.test import TestCase
from unittest import mock

# Local import
from .input import UserInput
from .substitute import SubstituteQueries
from .refine import RefineSubstitute


# Create your tests here.

""" Test every server side function (input.py , substitute.py, refine.py) """

products = [
    {
        'id': 'ID_1',
        'product_name': 'Product_1',
        'nutrition_grades': 'd',
        'selected_images': {'front': {'display': {'fr': 'some_img_1'}}},
        'url': 'off_url_1',
        'nutriments': {
            'energy_100g': 100,
            'fat_100g': 100,
            'saturated-fat_100g': 100,
            'carbohydrates_100g': 100,
            'sugars_100g': 100,
            'proteins_100g': 100,
            'salt_100g': 100},
        'categories_hierarchy': ['en:cat_1', 'it:cat_2', 'en:cat_3', 'en:cat_4'],
        'stores_tags': []
    },
    {
        'id': 'ID_2',
        'product_name': 'Product_2',
        'nutrition_grades': 'a',
        'selected_images': {'front': {'display': {'fr': 'some_img_2'}}},
        'url': 'off_url_2',
        'nutriments': {
            'energy_100g': 100,
            'fat_100g': 100,
            'saturated-fat_100g': 100,
            'carbohydrates_100g': 100,
            'sugars_100g': 100,
            'proteins_100g': 100,
            'salt_100g': 100},
        'categories_hierarchy': ['en:cat_1', 'fr:cat_2', 'en:cat_3', 'en:cat_4'],
        'stores_tags': ["Aldi", "Auchan"]
    },
    {
        'id': 'ID_3',
        'product_name': 'Product_3',
        'nutrition_grades': 'b',
        'selected_images': {'front': {'display': {'fr': 'some_img_3'}}},
        'url': 'off_url_3',
        'categories_hierarchy': ['en:cat_1', 'en:cat_2', 'fr:cat_3', 'en:cat_5'],
        'stores_tags': ["None", "Foreign"]
    },
    {
        'id': 'ID_4',
        'product_name': 'Product_4',
        'nutrition_grades': 'e',
        'selected_images': {'front': {'display': {'fr': 'some_img_4'}}},
        'url': 'off_url_4',
        'categories_hierarchy': ['fr:cat_1', 'es:cat_2', 'de:cat_3'],
        'stores_tags': []
    },
    {
        'id': 'ID_5',
        'product_name': 'Product_5',
        'nutrition_grades': '',
        'selected_images': {'front': {'display': {'fr': 'some_img_5'}}},
        'url': 'off_url_5',
        'categories_hierarchy': ['de:cat_1', 'en:cat_2', 'fr:cat_3'],
        'stores_tags': ["Aldi"]
    },
    {
        'id': 'ID_2',
        'product_name': 'Double_Product_2',
        'nutrition_grades': 'a',
        'selected_images': {'front': {'display': {'fr': 'some_img_2'}}},
        'url': 'off_url_2',
        'categories_hierarchy': ['en:cat_1', 'fr:cat_2', 'en:cat_3', 'en:cat_4'],
        'stores_tags': ["Auchan"]
    }
]


class UserInputTestCase(TestCase):
    @mock.patch('openfoodfacts.products')
    def test_user_input(self, mock_off):
        mock_off.search.return_value = {'count': 6, 'products': products}

        user_input = UserInput('InputUser')
        p_param = user_input.get_product()

        # Assert
        mock_off.search.assert_called_once_with('InputUser')
        mock_off.search.status_code = 200
        self.assertEqual(len(p_param), 4)
        self.assertEqual(p_param['cat_1'], 'en:cat_1')
        self.assertEqual(p_param['cat_2'], 'en:cat_3')
        self.assertEqual(p_param['cat_3'], 'en:cat_4')
        self.assertEqual(p_param['ng'], ['a', 'b', 'c', 'd'])
        # Test if minority categories ('cat') aren't in the result
        ignored_cat = [
            'en:cat_5', 'fr:cat_1', 'fr:cat_2',
            'fr:cat_3', 'de:cat_1', 'es:cat_2'
        ]
        for cat in ignored_cat:
            self.assertNotIn(cat, p_param)


class SubstituteQueriesTestCase(TestCase):
    @mock.patch('openfoodfacts.products')
    def test_substitute_queries(self, mock_off):
        mock_off.advanced_search.return_value = {'products': products}

        p_param = {
            'cat_1': 'value_1',
            'cat_2': 'value_2',
            'cat_3': 'value_3',
            'ng': ['a', 'b', 'c', 'd']
        }

        sub_query = SubstituteQueries(p_param)
        advanced_search = sub_query.query_off()
        # Make sure mock worked
        mock_off.advanced_search.status_code = 200
        self.assertEqual(len(advanced_search), 6)

        head = sub_query.get_head_product(advanced_search)
        # Test if the image of the first worst nutrition grades is the result
        # And test if others are not
        self.assertEqual(head['img'], 'some_img_4')
        ignored_img = ['some_img_1', 'some_img_2', 'some_img_3', 'some_img_5']
        for img in ignored_img:
            self.assertNotEqual(img, head['img'])

        substitute = sub_query.get_substitute(products)
        # Make sure products with
        # no stores (or not in the constants.py STORE_LIST)
        # or nutrition grades
        # or is a duplicate ID aren't considered as substitute
        ignored_product = ['ID_1', 'ID_3', 'ID_4', 'ID_5', 'Double_Product_2']
        for p in ignored_product:
            self.assertNotIn(p, substitute)
        # Make sure the function worked as intended
        self.assertEqual(len(substitute), 1)
        self.assertEqual(substitute[0]['id'], 'ID_2')


class RefineSubstituteTestCase(TestCase):
    def test_refine_substitute(self):
        refine = RefineSubstitute(products)
        result = refine.product_infos()

        # Second product (ID_2) should be first (best nutrition grades)
        # First product (ID_1) should be second (worst nutrition grades)
        self.assertEqual(result[0]['id'], 'ID_2')
        self.assertEqual(result[1]['id'], 'ID_1')
        # All others products (ID_3 to ID_6) should be ignored
        #   => (not enough data to keep it)
        ignored_product = ['ID_3', 'ID_4', 'ID_5', 'ID_6']
        for p in ignored_product:
            self.assertNotIn(p, result)
