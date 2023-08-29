from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Author, Book, BookCopy, BookRequest
from django.urls import reverse


# Create your tests here.
class TestBook(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="Testuuser", email="testuser@book.com", password="secret"
        )
        self.author1 = Author.objects.create(names="Akinyemi David Mohniq")
        self.author2 = Author.objects.create(names="Mark Paul")
        self.book1 = Book.objects.create(
            title="The Genesis of Books", isbn="978-978-123-4", author=self.author1
        )
        self.book2 = Book.objects.create(
            title="The Exodus of Books", isbn="978-978-123-5", author=self.author2
        )
        self.book3 = Book.objects.create(
            title="The Lamentation of Books", isbn="978-978-123-4", author=self.author1
        )
        return super().setUp()

    def test_author_creation(self):
        self.assertEqual(Author.objects.count(), 2)

    def test_copy_creation_on_book_creation(self):
        """Test that a copy is created when a book is created"""
        copies = BookCopy.objects
        self.assertEqual(copies.count(), 3)
        self.assertTrue(copies.all().contains(self.book1.copies.get()))
        self.assertTrue(copies.all().contains(self.book2.copies.get()))
        self.assertTrue(copies.all().contains(self.book3.copies.get()))
        self.assertEqual(copies.filter(status__in=["b", "r"]).count(), 0)

    def test_author_books(self):
        """Test the number of books by author"""
        self.assertEqual(self.author1.books.count(), 2)

    # def test_due_date(self):
    #     copy = self.book1.copies.get()
    #     self.assertRaises(
    #         ValidationError,
    #         BookCopy.objects.create,
    #         book=self.book2,
    #         due_date=datetime.now().date() - timedelta(days=2),
    #     )

    def test_create_request(self):
        """Test a request for a copy. Initial request status should be  'a'"""
        request = BookRequest.objects.create(
            copy=BookCopy.objects.get(book=self.book1), requester=self.user
        )
        self.assertTrue(request.status == "w")
        # self.assertAlmostEqual(request.date_time_requested.time(), timezone.now().time())
        request.status = "a"
        request.save()
        self.assertEqual(request.copy.status, "r")
        request.status = "d"
        request.save()
        self.assertEqual(request.copy.status, "b")

    def test_book_list_view(self):
        resp = self.client.get(reverse("book_list"))
        self.assertContains(resp, "The Genesis of Books", count=1)
        self.assertContains(resp, self.book1.get_absolute_url(), count=1)

