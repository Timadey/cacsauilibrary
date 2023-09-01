from typing import Collection, Union
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from helpers.helpers import due_date, gen_rand_four


# Create your models here.
class Author(models.Model):
    """The author of a book"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    names = models.CharField(max_length=256, blank=False, default="Alex John")


    class Meta:
        ordering = ["names"]

    def __str__(self) -> str:
        return f"{self.names}"

    @property
    def name(self):
        return f"{self.names}"


class BookCopy(models.Model):
    """A single copy of a book that can be borrowed from the library"""

    id = models.CharField(
        primary_key=True, default=gen_rand_four, editable=False, max_length=4
    )
    book = models.ForeignKey("Book", related_name="copies", on_delete=models.CASCADE)
    due_date = models.DateField(
        null=True, blank=True, help_text="When the book is due for returning"
    )
    LOAN_STATUS = (("a", "available"), ("b", "borrowed"), ("r", "reserved"))
    status = models.CharField(max_length=1, default="a", choices=LOAN_STATUS)

    class Meta:
        ordering = ["status"]

    def __str__(self) -> str:
        return f"{self.book.title}#{self.id}"

    def clean_fields(self, exclude: Union[Collection[str], None]) -> None:
        if not self.due_date is None and self.due_date < due_date().date():
            raise ValidationError(
                {
                    "due_date": "Due date must be up to the maximum day allowed for borrowing"
                }
            )
        return super().clean_fields(exclude)


class Book(models.Model):
    """A book object with a title, author"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.PROTECT)
    summary = models.TextField(max_length=1024, null=True, blank=True)
    isbn = models.CharField("ISBN", max_length=13, blank=True)
    cover = models.ImageField(blank=True, upload_to="covers/")
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", args=[self.pk])


# class BookRequest(models.Model):
#     """A user's request to borrow a book. Request can be approved or declined or deleivered
#     if the book has been lent to the user"""

#     id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
#     requester = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
#     copy = models.ForeignKey(to=BookCopy, on_delete=models.CASCADE)
#     REQUEST_STATUS = (
#         ("w", "Awaiting Approval"),
#         ("a", "approved"),
#         ("d", "delivered"),
#         ("x", "declined"),
#     )
#     status = models.CharField(max_length=1, default="w", choices=REQUEST_STATUS)
#     date_time_requested = models.DateTimeField(auto_now_add=True, null=True)
#     date_time_delivered = models.DateTimeField(null=True, blank=True)

#     def __str__(self) -> str:
#         return f"{self.copy.__str__()}:Request"

#     # def get_absolute_url(self):
#     #     return reverse("book", args=[self.id])
