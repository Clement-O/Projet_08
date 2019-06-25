from django.test import SimpleTestCase
from django.urls import reverse
from unittest import mock

# Local import
from . import products


# Create your tests here.

""" Test product's views """


class ProductViewsTests(SimpleTestCase):
    @mock.patch('openfoodfacts.products')
    def test_search(self, mock_off):
        mock_off.search.return_value = {'count': 16, 'products': products}
        mock_off.advanced_search.return_value = {'products': products}

        url = reverse('product:search')
        response = self.client.get(url, {'query': 'nutella'})

        # Tests mocks
        mock_off.search.assert_called_with('nutella')
        assert mock_off.advanced_search.called
        # Tests response & algos
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['name'], 'nutella')
        self.assertEqual(response.context[-1]['img'], 'some_img_4')

        # Tests pagination
        page_response = response.context[-1]['substitute'].paginator
        self.assertEqual(page_response.count, 12)
        self.assertTrue(page_response.page(1).has_next())
        self.assertFalse(page_response.page(1).has_previous())
        self.assertFalse(page_response.page(2).has_next())
        self.assertTrue(page_response.page(2).has_previous())
        self.assertEqual(len(page_response.page(1).object_list), 9)
        self.assertEqual(len(page_response.page(2).object_list), 3)
