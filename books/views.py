from typing import Any, Dict
from datetime import date
from django import http

from django.contrib import messages
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.db.models import Q, QuerySet

from .forms import BookRequestForm, BookSearchForm
from .helpers import due_date
from .models import Book, BookCopy, BookRequest


# Create your views here.
class BookListView(ListView):
    model = Book
    context_object_name = "books"
    template_name = "books/list.html"

    def get_queryset(self) -> QuerySet[Any]:
        if self.request.GET:
            lookup = BookSearchForm(self.request.GET)
            # search book by title and author
            if lookup.is_valid():
                print(lookup)
                query = lookup.cleaned_data["q"].split(" ")
                qset = Q()
                for q in query:
                    qset |= Q(title__icontains=q) | Q(author__names__icontains=q) | Q(isbn__exact=q)
                return Book.objects.filter(qset)
        else:
            return super().get_queryset()

class BookDetailView(DetailView):
    model = Book
    context_object_name = "book"
    template_name = "books/detail.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        copies = self.get_object().copies.all()
        # available_copies = list(filter(lambda x: x.status == "a", copies))
        # context["available_copies"] = available_copies
        # context["other_copies"] = set(copies) - set(available_copies)
        return context


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


class BorrowBookView(View):
    """View that handles the request for borrowing books"""

    # model = BookCopy
    # # pk_url_kwarg = "copy_id"
    # context_object_name = "copy"
    # template_name = "borrow_book/confirm.html"
    form_class = BookRequestForm

    # @book_is_available
    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     context["due_date"] = due_date()
    #     return context

    @book_is_available
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Send a request to borrow a book to the server"""
        form = self.form_class(request.POST)
        book_request = form.save(commit=False)
        copy = self.get_object()
        # check if user has pending requests for same book
        pending_request = BookRequest.objects.filter(
            status__in=["w", "a"], copy__book=copy.book, requester=request.user
        )
        on_loan_by_user = BookRequest.objects.filter(
            status="d",
            copy__book=copy.book,
            requester=request.user,
            copy__due_date__gt=date.today(),
        )
        if pending_request:
            messages.error(self.request, "You have a pending request for this book.")
            return redirect(copy.book.get_absolute_url())
        if on_loan_by_user:
            messages.error(
                self.request, "You currently have a copy of this book with you."
            )
            return redirect(copy.book.get_absolute_url())
        book_request.requester = request.user
        book_request.copy = copy
        book_request.save()
        # future: Notify admin also about book request
        messages.success(
            self.request, "Your book request has been submitted successfully"
        )
        return redirect(copy.book.get_absolute_url())


# class SearchBookView(ListView):
#     context_object_name = "books"
#     template_name = "books/list.html"

#     def get_queryset(self) -> QuerySet[Any]:
#         if self.request.GET:
#             lookup = BookSearchForm(self.request.GET)
#             # search book by title and author
#             if lookup.is_valid():
#                 print(lookup)
#                 query = lookup.cleaned_data["q"].split(" ")
#                 qset = Q()
#                 for q in query:
#                     qset |= Q(title__icontains=q) | Q(author__first_name__icontains=q) | Q(isbn__exact=q)
#                 return Book.objects.filter(qset)
