from datetime import date
from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from books.models import BookCopy

from .decorators import book_is_available
from .forms import BookRequestForm
from .models import BookRequest


# Create your views here.
class BorrowBookView(LoginRequiredMixin, DetailView):
    """View that handles the request for borrowing books"""

    model = BookCopy
    form_class = BookRequestForm
    template_name = "loans/detail.html"

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

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return render(request, self.template_name, context={"copy": self.get_object()})


class LoanListView(LoginRequiredMixin, ListView):
    model = BookRequest
    context_object_name = "loans"
    template_name = "loans/list.html"
    status_label = {
        "awaiting": "w",
        "approved": "a",
        "delivered": "d",
        "declined": "x",
    }

    def get_queryset(self) -> QuerySet[Any]:
        if self.kwargs.get("status") is not None:
            status = self.status_label.get(self.kwargs["status"])
            return BookRequest.objects.filter(
                requester=self.request.user, status=status
            )
        else:
            return BookRequest.objects.filter(requester=self.request.user)
