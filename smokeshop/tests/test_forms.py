from django.test import TestCase

from smokeshop.forms import FeedbackForm


class FeedbackFormTestCase(TestCase):

    def test_valid_form_with_correct_data(self):
        """Тест формы при передачи корректных данных"""
        form = FeedbackForm(data={
            'text': 'Some text', 'rating': 4
        })
        self.assertTrue(form.is_valid())
        tag_data = '<textarea name="text" cols="40" rows="6" class="form-control shadow px-2" id="id_text">'
        self.assertIn(tag_data, form.as_p())

    def test_valid_form_with_incorrect_data(self):
        """Тест формы при передачи некорректных данных"""
        form = FeedbackForm(data={
            'text': 'Some text', 'wrong_rating': 'wrong text'
        })
        error_data = {'rating': ['Обязательное поле.']}
        self.assertFalse(form.is_valid())
        self.assertEqual(error_data, form.errors)
