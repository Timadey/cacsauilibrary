from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Book, BookCopy


@receiver(post_save, sender=Book, dispatch_uid="create-book-copy")
def create_book_copy(sender, instance, created, **kwargs):
    """Create a book copy each time a book is created and saved"""
    if created:
        BookCopy.objects.create(book=instance)


# @receiver(post_save, sender=BookRequest, dispatch_uid="change-request-status")
# def change_request_status(sender, instance, created, **kwargs):
#     """Change book copy status in respect to change in request status.
#     If the book request is approved, then the book copy status is changed to reserved.
#     If request status is delivered, copy's status is changed to borrowed.
#     """
#     copy = instance.copy
#     if not created:
#         # this is should be done when an existing request status is changed
#         if instance.status == "a":
#             copy.status = "r"
#             copy.save()
#             # Send approval mail
#             send_mail(
#                 "Your request has been approved",
#                 f"""Your request to borrow {copy} has been approved.
#             Please go to the Library to get the copy you have requested for.
#             Title: {copy} by {copy.book.author}
#             Due date: {MAX_DUE_DAY} days from delivery""",
#                 from_email=None,
#                 recipient_list=[instance.requester.email],
#             )
#         elif instance.status == "d":
#             copy.status = "b"
#             if copy.due_date is None:
#                 copy.due_date = due_date()
#             copy.save()
#             # Send delivery mail
#             send_mail(
#                 "Your book has been delivered",
#                 f"""You have successfully borrowed {copy} from the library.
#             Title: {copy} by {copy.book.author}
#             Due date: {copy.due_date}
#             Please return the book before due date. Thank you!""",
#                 from_email=None,
#                 recipient_list=[instance.requester.email],
#             )
#     else:
#         # Notify user of their request via email
#         send_mail(
#             "Your request has been received",
#             f"""We have received your request to borrow {copy}.
#             Please wait for approval and this book will be reserved for you.""",
#             from_email=None,
#             recipient_list=[instance.requester.email],
#         )
#         # Notify admin of a new request


# @receiver(pre_save, sender=BookRequest, dispatch_uid="set-datetime-delivered")
# def set_datetime_delivered(sender, instance, **kwargs):
#     if instance.status == "d" and not instance.date_time_delivered:
#         instance.date_time_delivered = timezone.now()
