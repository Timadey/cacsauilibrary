from django import forms

from .models import BookRequest


class BookRequestForm(forms.ModelForm):
    """A form for managing book request"""
    class Meta:
        model = BookRequest
        fields = []

class LoanFilterForm(forms.Form):
    status = forms.CharField(required=True, max_length=2)