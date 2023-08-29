# from django.test import TestCase
# from django.urls import reverse, resolve
# from django.contrib.auth import get_user_model
# from .views import SignUpView
# # from .forms import CustomUserCreationForm


# # Create your tests here.
# class TestUser(TestCase):
#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(
#             username="Test user", email="testuser@email.com", password="secret"
#         )
#         self.assertEqual(user.username, "Test user")
#         self.assertEqual(user.email, "testuser@email.com")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)

#     def test_create_superuser(self):
#         User = get_user_model()
#         adm = User.objects.create_superuser(
#             username="Super", email="super@email.com", password="secret"
#         )
#         self.assertTrue(adm.is_active)
#         self.assertTrue(adm.is_staff)
#         self.assertTrue(adm.is_superuser)
#         self.assertEqual(adm.email, "super@email.com")
#         self.assertTrue(adm.username, "Super")


# class TestUserSignup(TestCase):
#     def setUp(self) -> None:
#         self.resp = self.client.get(reverse("account_signup"))

#     def test_signup_page_success(self):
#         self.assertTrue(self.resp.status_code, 200)

#     def test_signup_template(self):
#         self.assertTemplateUsed("account/signup.html")
#         self.assertContains(self.resp, "Sign Up")
#         self.assertNotContains(self.resp, "This is not a sign up page")
