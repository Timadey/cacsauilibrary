# from django.test import TestCase
# from django.urls import reverse, resolve
# from .views import HomepageView


# # Create your tests here.
# class HomepageTest(TestCase):
#     def setUp(self) -> None:
#         self.resp = self.client.get(reverse("home"))

#     def test_homepage_url(self):
#         self.assertEqual(self.resp.status_code, 200)

#     def test_homepage_template(self):
#         self.assertTemplateUsed("home.html")
#         self.assertContains(self.resp, "Homepage")
#         self.assertNotContains(self.resp, "Not an homapage")

#     def test_homepage_view(self):
#         view = resolve("/")
#         self.assertEqual(view.func.__name__, HomepageView.as_view().__name__)
