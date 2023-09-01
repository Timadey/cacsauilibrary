import os
import shutil
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from bookstore_project.settings import BASE_DIR

from .models import Author, Book, BookCopy, BookRequest


# Create your tests here.
@override_settings(
    MEDIA_ROOT=os.path.join(BASE_DIR, "tmp/media"), MEDIA_URL="/tmp/media/"
)
class TestBook(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="Testuuser", email="testuser@book.com", password="secret"
        )
        self.author1 = Author.objects.create(names="Akinyemi David Mohniq")
        self.author2 = Author.objects.create(names="Mark Paul")
        image = SimpleUploadedFile("book_cover.jpg", b"image content", "image/jpeg")
        self.book1 = Book.objects.create(
            title="The Genesis of Books",
            isbn="978-978-123-4",
            author=self.author1,
            cover=image,
        )
        self.book2 = Book.objects.create(
            title="The Exodus of Books",
            isbn="978-978-123-5",
            author=self.author2,
            cover=image,
        )
        self.book3 = Book.objects.create(
            title="The Lamentation of Books",
            isbn="978-978-123-4",
            author=self.author1,
            cover=image,
        )
        return super().setUp()

    # def test_book_cover_upload_dir(self):
    # self.assertEqual(self.book1.cover.upload_to, 'tmp/media/covers')
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
        # create a request
        request = BookRequest.objects.create(
            copy=BookCopy.objects.get(book=self.book1), requester=self.user
        )
        # test initial status is 'w'
        self.assertTrue(request.status == "w")
        #  find the difference between timme requested and now and test that they are not far
        time_diff = request.date_time_requested - timezone.now()
        max_diff = timedelta(minutes=1)
        self.assertLessEqual(time_diff, max_diff)
        # test that copy status is updated in request status update
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
        self.assertContains(resp, "tmp/media/covers/book_cover")
        # test search by string
        resp = self.client.get(reverse("book_list"), data={"q": "genesis"})
        self.assertEqual(resp.context["books"].count(), 1)
        self.assertContains(resp, self.book1.title)
        resp = self.client.get(reverse("book_list"), data={"q": "booknotinlibrary"})
        self.assertEqual(resp.context["books"].count(), 0)
        resp = self.client.get(reverse("book_list"), data={"isbn": "978-978-123-5"})
        self.assertIsNone(resp.context["books"])

    # def test_borrow_book(self):
    #     book3_copies = self.book3.copies
    #     copy = book3_copies.get()
    #     status = self.client.login(
    #         email=self.user.email, password=self.user.password
    #     )
    #     print(status)
    #     resp = self.client.post(reverse("borrow_book", args=[copy.pk]))

    def tearDown(self) -> None:
        if os.path.exists("tmp") and os.path.isdir("tmp"):
            shutil.rmtree("tmp")
        return super().tearDown()
