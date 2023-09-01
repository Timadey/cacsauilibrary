from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from books.models import BookCopy


# Create your models here.
class BookRequest(models.Model):
    """A user's request to borrow a book. Request can be approved or declined or deleivered
    if the book has been lent to the user"""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    requester = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    copy = models.ForeignKey(to=BookCopy, on_delete=models.CASCADE)
    REQUEST_STATUS = (
        ("w", "Awaiting Approval"),
        ("a", "approved"),
        ("d", "delivered"),
        ("x", "declined"),
    )
    status = models.CharField(max_length=1, default="w", choices=REQUEST_STATUS)
    date_time_requested = models.DateTimeField(auto_now_add=True, null=True)
    date_time_delivered = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.copy.__str__()}:Request"

    # def get_absolute_url(self):
    #     return reverse("book", args=[self.id])
