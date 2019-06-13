from django.test import TestCase
from unittest import mock

# Local import
from . import products
from product.input import UserInput
from product.substitute import SubstituteQueries
from product.refine import RefineSubstitute


# Create your tests here.

""" Test every server side function (input.py , substitute.py, refine.py) """


class UserInputTestCase(TestCase):
    @mock.patch('openfoodfacts.products')
    def test_user_input(self, mock_off):
        mock_off.search.return_value = {'count': 16, 'products': products}

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
        self.assertEqual(len(advanced_search), 16)

        head = sub_query.get_head_product(advanced_search)
        # Test if the image of the first worst nutrition grades is the result
        # And test if others are not
        self.assertEqual(head['img'], 'some_img_4')
        ignored_img = [
            'some_img_1', 'some_img_2', 'some_img_3', 'some_img_5',
            'some_img_7', 'some_img_8', 'some_img_9', 'some_img_10',
            'some_img_11', 'some_img_12', 'some_img_13', 'some_img_14',
            'some_img_15', 'some_img_16',
        ]
        for img in ignored_img:
            self.assertNotEqual(img, head['img'])

        substitute = sub_query.get_substitute(products)
        # Make sure products with
        # no stores (or not in the constants.py STORE_LIST)
        # or nutrition grades
        # or is a duplicate ID aren't considered as substitute
        ignored_product = ['ID_3', 'ID_4', 'ID_5', 'Double_Product_2']
        for p in ignored_product:
            self.assertNotIn(p, substitute)
        # Make sure the function worked as intended
        self.assertEqual(len(substitute), 12)
        self.assertEqual(substitute[0]['id'], 'ID_1')


class RefineSubstituteTestCase(TestCase):
    def test_refine_substitute(self):
        refine = RefineSubstitute(products)
        result = refine.product_infos()

        # Second product (ID_2) should be first (best nutrition grades)
        # First product (ID_1) should be the last (worst nutrition grades)
        self.assertEqual(result[0]['id'], 'ID_2')
        self.assertEqual(result[11]['id'], 'ID_1')
        # All others products (ID_3 to ID_6) should be ignored
        #   => (not enough data to keep it)
        ignored_product = ['ID_3', 'ID_4', 'ID_5', 'ID_6']
        for p in ignored_product:
            self.assertNotIn(p, result)
