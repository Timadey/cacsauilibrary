from django import forms


class BookSearchForm(forms.Form):
    q = forms.CharField(required=True)


class AddBookByIsbnForm(forms.Form):
    isbn_list = forms.CharField(
        required=True, help_text="Enter ISBN of books to add one per line"
    )
