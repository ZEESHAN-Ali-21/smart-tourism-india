from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for submitting destination reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'visit_date']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title',
                'maxlength': 200,
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...',
                'required': True
            }),
            'visit_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class SearchForm(forms.Form):
    """Form for searching destinations"""
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control search-bar',
            'placeholder': 'Search destinations, cities, states...',
            'id': 'searchInput'
        })
    )