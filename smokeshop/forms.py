from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """Форма для oтзывов и оценок на товар"""
    class Meta:
        model = Feedback
        fields = ('text', 'rating')
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control shadow px-2',
                'rows': 6}
            ),
            'rating': forms.RadioSelect
        }
