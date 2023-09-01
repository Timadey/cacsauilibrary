from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def book_is_available(func):
    """A decorator that checks that the book is available before processing the request"""

    def wrapper(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        # check that the book is available
        copy = self.get_object()
        if not copy.status == "a":
            messages.error(request, "This book copy is not available for borrowing")
            return redirect(copy.book.get_absolute_url())
        return func(self, request, *args, **kwargs)

    return wrapper
