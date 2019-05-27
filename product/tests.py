# Third party import
import openfoodfacts

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


def test_get_product(monkeypatch):
    def mockreturn(request):
        return {'count': 6, 'products': products}
    monkeypatch.setattr(openfoodfacts.products, 'search', mockreturn)

    user_input = UserInput('InputUser')

    p_param = user_input.get_product()
    # Make sure result are expected
    assert len(p_param) == 4
    assert p_param['cat_1'] == 'en:cat_1'
    assert p_param['cat_2'] == 'en:cat_3'
    assert p_param['cat_3'] == 'en:cat_4'
    assert p_param['ng'] == ['a', 'b', 'c', 'd']
    # Make sure minority 'cat' aren't in the result
    assert 'en:cat_5' not in p_param
    assert 'fr:cat_1' not in p_param
    assert 'fr:cat_2' not in p_param
    assert 'fr:cat_3' not in p_param
    assert 'de:cat_1' not in p_param
    assert 'es:cat_2' not in p_param


def test_substitute_queries(monkeypatch):
    def mockreturn(request):
        return {'products': products}
    monkeypatch.setattr(openfoodfacts.products, 'advanced_search', mockreturn)

    p_param = {
        'cat_1': 'value_1',
        'cat_2': 'value_2',
        'cat_3': 'value_3',
        'ng': ['a', 'b', 'c', 'd']
    }

    sub_query = SubstituteQueries(p_param)

    advanced_search = sub_query.query_off()
    # Make sure mock worked
    assert len(advanced_search) == 6

    head = sub_query.get_head_product(advanced_search)
    # Make sure it's the image of the first worst nutrition grades
    # (even if lacking some infos)
    assert {'img': 'some_img_4'} == head    # e, ID_4
    assert {'img': 'some_img_1'} != head    # d, ID_1
    assert {'img': 'some_img_2'} != head    # a, ID_2 & ID_6
    assert {'img': 'some_img_3'} != head    # b, ID_3
    assert {'img': 'some_img_5'} != head    # None, ID_5

    substitute = sub_query.get_substitute(products)
    # Make sure products with
    # no stores (or not in the constants.py STORE_LIST)
    # or nutrition grades
    # or is a duplicate ID aren't considered as substitute
    assert 'ID_1' not in substitute  # No stores
    assert 'ID_3' not in substitute  # Not in STORE_LIST
    assert 'ID_4' not in substitute  # No stores
    assert 'ID_5' not in substitute  # No nutrition grades
    assert 'Double_Product_2' not in substitute  # Duplicate ID
    # Make sure the function worked as intended
    assert len(substitute) == 1
    assert substitute[0]['id'] == 'ID_2'


def test_product_infos():

    refine = RefineSubstitute(products)
    result = refine.product_infos()

    # Second product (ID_2) should be first (best nutrition grades)
    # First product (ID_1) should be second (worst nutrition grades)
    assert result[0]['id'] == 'ID_2'
    assert result[1]['id'] == 'ID_1'
    # All others products (ID_3 to ID_6) should be ignored
    #   => (not enough data to keep it)
    assert 'ID_3' not in result
    assert 'ID_4' not in result
    assert 'ID_5' not in result
    assert 'ID_6' not in result
