from django import forms
from .models import BookRequest

class BookRequestForm(forms.ModelForm):
    """A form for managing book request"""
    class Meta:
        model = BookRequest
        fields = []

class BookSearchForm(forms.Form):
    q = forms.CharField(required=True)