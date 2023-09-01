import secrets
from django.utils import timezone
from datetime import timedelta


from bookstore_project.settings import MAX_DUE_DAY


def due_date(days: float = MAX_DUE_DAY):
    """Date when a book is due for returning"""
    return timezone.now() + timedelta(days)


def gen_rand_four():
    """Generate four random character for primary id"""
    return secrets.token_urlsafe(3)
