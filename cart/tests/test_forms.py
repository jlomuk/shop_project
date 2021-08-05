from django.test import TestCase

from cart.forms import CartAddProductForm


class CartAddProductFormTestCase(TestCase):

    def test_valid_form_with_correct_data(self):
        """Тест формы при передачи корректных данных"""
        form = CartAddProductForm(data={
            'quantity': '5', 'update': 'False'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual({}, form.errors)
        self.assertIn('form-control text-center px-3', form.as_p())

    def test_valid_form_without_update(self):
        """Тест формы при передачи корректных данных"""
        form = CartAddProductForm(data={
            'quantity': '5',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual({}, form.errors)

    def test_valid_form_with_incorrect_data(self):
        """Тест формы при передачи некорректных данных"""
        form = CartAddProductForm(data={
            'quantity': '0', 'update':'False'
        })
        error_data = {'quantity': ['Убедитесь, что это значение больше либо равно 1.']}
        self.assertFalse(form.is_valid())
        self.assertEqual(error_data, form.errors)