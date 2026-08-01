from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class AuthenticationFlowTests(TestCase):
    def test_home_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('catalog:home')}",
        )

    def test_all_customer_pages_require_login(self):
        protected_pages = (
            "catalog:calorie_calculator",
            "catalog:walking_steps",
            "catalog:weekly_plan",
            "catalog:exercise_list",
            "catalog:healthy_food_list",
        )

        for page_name in protected_pages:
            with self.subTest(page=page_name):
                response = self.client.get(reverse(page_name))
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("accounts:login")))

    def test_user_can_register_and_is_logged_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newclient",
                "password1": "SafePass-2026!",
                "password2": "SafePass-2026!",
            },
        )

        self.assertRedirects(response, reverse("catalog:home"))
        self.assertTrue(User.objects.filter(username="newclient").exists())
        self.assertEqual(self.client.session["_auth_user_id"], str(User.objects.get(username="newclient").pk))

    def test_user_can_log_in_and_log_out(self):
        User.objects.create_user(username="client", password="SafePass-2026!")

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "client", "password": "SafePass-2026!"},
        )
        self.assertRedirects(response, reverse("catalog:home"))

        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))

    def test_authenticated_home_contains_coach_chat(self):
        user = User.objects.create_user(username="client", password="SafePass-2026!")
        self.client.force_login(user)

        response = self.client.get(reverse("catalog:home"))

        self.assertContains(response, "مساعد المدرب")
        self.assertContains(response, "sports-reel")
        self.assertContains(response, 'data-coach-number="966533625844"')
        for video_name in (
            "workout-weights.mp4",
            "workout-battle-ropes.mp4",
            "workout-dynamic.mp4",
            "workout-boxing.mp4",
        ):
            self.assertContains(response, f"videos/{video_name}")

        self.assertContains(response, "20 ثانية")
