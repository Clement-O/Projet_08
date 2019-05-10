from .input import UserInput
from .substitute import SubstituteQueries
from .refine import RefineSubstitute


# Create your tests here.


def test_get_product(monkeypatch):
    query = "nutella"
    result = {
        'cat_1': 'value_1',
        'cat_2': 'value_2',
        'cat_3': 'value_3',
        'ng': 'ng',
    }

    def mockreturn(query):
        return result

    path = 'product.input.UserInput.get_product'
    monkeypatch.setattr(path, mockreturn)
    assert UserInput.get_product(query) == result


def test_query_off(monkeypatch):
    product = {
        'cat_1': 'value_1',
        'cat_2': 'value_2',
        'cat_3': 'value_3',
        'ng': 'ng',
    }
    result = {
        'id': 123456,
        'name': 'sub',
        'img': 'link_off'
    }

    def mockreturn(product):
        return result

    path = 'product.substitute.SubstituteQueries.query_off'
    monkeypatch.setattr(path, mockreturn)
    assert SubstituteQueries.query_off(product) == result


def test_product_infos(monkeypatch):
    products = [
        {'product_name': 'p_D', 'nutrition_grades': 'd'},
        {'product_name': 'p_B', 'nutrition_grades': 'b'},
        {'product_name': 'p_A', 'nutrition_grades': 'a'}
    ]
    result = [
        {'product_name': 'p_A', 'nutrition_grades': 'a'},
        {'product_name': 'p_B', 'nutrition_grades': 'b'},
        {'product_name': 'p_D', 'nutrition_grades': 'd'}
    ]

    def mockreturn(products):
        return result

    path = 'product.refine.RefineSubstitute.product_infos'
    monkeypatch.setattr(path, mockreturn)
    assert RefineSubstitute.product_infos(products) == result
