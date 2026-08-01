import io
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.templatetags.static import static
from PIL import Image

from .services import analyze_food_image


TEST_STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class AuthenticatedCatalogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="catalog-client",
            password="SafePass-2026!",
        )
        self.client.force_login(self.user)


class ExerciseListViewTests(AuthenticatedCatalogTestCase):
    def test_exercise_list_page_loads(self):
        response = self.client.get(
            reverse("catalog:exercise_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/exercise_list.html",
        )

    def test_exercise_list_contains_home_and_gym_exercises(self):
        response = self.client.get(
            reverse("catalog:exercise_list")
        )
        exercises = response.context["exercises"]
        home_exercises = [
            exercise
            for exercise in exercises
            if exercise["location"] == "home"
        ]
        gym_exercises = [
            exercise
            for exercise in exercises
            if exercise["location"] == "gym"
        ]

        self.assertEqual(len(exercises), 42)
        self.assertEqual(len(home_exercises), 6)
        self.assertEqual(len(gym_exercises), 36)

        for muscle_group in (
            "chest",
            "back",
            "shoulders",
            "legs",
            "biceps",
            "triceps",
        ):
            self.assertEqual(
                len(
                    [
                        exercise
                        for exercise in gym_exercises
                        if exercise["muscle_group"] == muscle_group
                    ]
                ),
                6,
            )

        for exercise in exercises:
            self.assertTrue(exercise["steps"])
            self.assertTrue(exercise["image"])

    def test_every_exercise_image_is_rendered(self):
        response = self.client.get(
            reverse("catalog:exercise_list")
        )

        for exercise in response.context["exercises"]:
            self.assertContains(
                response,
                static(exercise["image"]),
            )

    def test_every_exercise_has_an_arabic_narrated_video(self):
        response = self.client.get(reverse("catalog:exercise_list"))
        exercises = response.context["exercises"]

        for exercise in exercises:
            self.assertTrue(exercise["video"])
            self.assertTrue(
                exercise["video"].endswith("-90s.mp4")
            )
            self.assertEqual(len(exercise["narration"]), 5)
            self.assertContains(response, static(exercise["video"]))

        self.assertContains(
            response,
            "شاهد الشرح الاحترافي بالعربي",
            count=42,
        )
        self.assertNotContains(response, "window.speechSynthesis")
        self.assertContains(
            response,
            '<span class="sound-status">الصوت مفعّل</span>',
            count=42,
            html=True,
        )
        self.assertContains(
            response,
            'title="عرض الفيديو بملء الشاشة"',
            count=42,
        )
        self.assertContains(
            response,
            'aria-label="التقديم أو الرجوع في الفيديو"',
            count=42,
        )
        self.assertContains(
            response,
            'aria-label="تشغيل الفيديو"',
            count=42,
        )
        self.assertContains(
            response,
            'aria-label="التقديم عشر ثوانٍ"',
            count=42,
        )
        self.assertContains(
            response,
            'aria-label="سرعة تشغيل الفيديو"',
            count=42,
        )
        self.assertContains(
            response,
            'controlslist="nodownload"',
            count=42,
        )


class HealthyFoodListViewTests(AuthenticatedCatalogTestCase):
    def test_healthy_food_list_page_loads(self):
        response = self.client.get(
            reverse("catalog:healthy_food_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/healthy_food_list.html",
        )

    def test_page_contains_food_and_drinks_with_benefits(self):
        response = self.client.get(
            reverse("catalog:healthy_food_list")
        )
        nutrition_items = response.context["nutrition_items"]
        food_items = [
            item
            for item in nutrition_items
            if item["category"] == "food"
        ]
        drink_items = [
            item
            for item in nutrition_items
            if item["category"] == "drink"
        ]

        self.assertEqual(len(nutrition_items), 21)
        self.assertEqual(len(food_items), 10)
        self.assertEqual(len(drink_items), 11)

        item_names = {item["name"] for item in nutrition_items}
        self.assertIn("سلطة التونة والحمص", item_names)
        self.assertIn("لفائف الدجاج والخضروات", item_names)
        self.assertIn("زبادي يوناني بالفواكه والمكسرات", item_names)
        self.assertIn("سموذي التوت والزبادي", item_names)
        self.assertIn("شاي الزنجبيل والليمون", item_names)
        self.assertIn("لبن بالخيار والنعناع", item_names)
        self.assertIn("شرائح اللحم قليلة الدهون", item_names)
        self.assertIn("كفتة لحم مشوية مع الأرز البني", item_names)
        self.assertIn("مياه غازية بالليمون والنعناع", item_names)
        self.assertIn("مياه غازية بالتوت والليمون الأخضر", item_names)
        self.assertIn("مشروب غازي خالٍ من السكر", item_names)

        subcategories = {
            item["subcategory"] for item in nutrition_items
        }
        self.assertEqual(
            subcategories,
            {
                "meat",
                "chicken",
                "fish",
                "vegetarian",
                "healthy_drink",
                "carbonated",
            },
        )
        self.assertEqual(
            len(response.context["nutrition_categories"]),
            2,
        )
        self.assertEqual(
            [
                category["slug"]
                for category in response.context["nutrition_categories"]
            ],
            ["food", "drink"],
        )
        self.assertTrue(
            all(item["category"] == "food" for item in nutrition_items[:10])
        )
        self.assertTrue(
            all(item["category"] == "drink" for item in nutrition_items[10:])
        )

        for item in nutrition_items:
            self.assertTrue(item["benefits"])
            self.assertTrue(item["subcategory_label"])
            self.assertContains(
                response,
                static(item["image"]),
            )

        self.assertContains(response, 'data-filter="food"')
        self.assertContains(response, 'data-filter="drink"')
        self.assertContains(response, "جميع الوجبات")
        self.assertContains(response, "جميع المشروبات")


class HomePageTests(AuthenticatedCatalogTestCase):
    def test_calorie_calculator_button_links_to_calculator(self):
        response = self.client.get(reverse("catalog:home"))
        calculator_url = reverse(
            "catalog:calorie_calculator"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'href="{calculator_url}"',
        )
        self.assertContains(
            response,
            "احسب سعراتك الآن",
        )

    def test_brand_logo_and_favicon_are_rendered(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(
            response,
            static("images/brand/sehaty-logo.png"),
        )
        self.assertContains(
            response,
            static("images/brand/sehaty-favicon.png"),
        )

    def test_home_page_links_to_ai_food_calorie_analyzer(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(
            response,
            f'href="{reverse("catalog:food_calorie_ai")}"',
        )
        self.assertContains(response, "حلّل وجبتك الآن")

    def test_whatsapp_launcher_uses_brand_icon_on_right(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(response, 'aria-label="شعار واتساب"')
        self.assertContains(response, "right: 24px")
        self.assertContains(response, "transform-origin: bottom right")

    def test_home_page_contains_water_benefits_video_section(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(response, "فوائد شرب الماء لصحتك وأدائك")
        self.assertContains(response, "تنظيم حرارة الجسم")
        self.assertContains(response, "دعم الأداء الرياضي")
        self.assertContains(response, "التركيز والنشاط")
        self.assertContains(response, "الهضم وانتظام الجسم")
        self.assertContains(
            response,
            static("videos/water-benefits-professional.mp4"),
        )
        self.assertContains(
            response,
            static("images/water-benefits-poster.webp"),
        )
        self.assertContains(response, "controls")

    def test_coach_bot_uses_requested_confirmation_reply(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(response, "👋 أهلاً بك في صحتي.")
        self.assertContains(response, "سعداء بتواصلك معنا! 💪")
        self.assertContains(
            response,
            "تم استلام رسالتك، وسيتم الرد عليك في أقرب وقت من قبل المدرب.",
        )
        self.assertContains(
            response,
            "إلى أن يتم الرد، يمكنك كتابة استفسارك بالتفصيل أو إرسال أي صور أو معلومات تساعدنا على فهم حالتك بشكل أفضل.",
        )
        self.assertContains(response, "نتمنى لك رحلة صحية موفقة 🌿")


class CalorieCalculatorViewTests(AuthenticatedCatalogTestCase):
    def test_calorie_calculator_page_loads(self):
        response = self.client.get(
            reverse("catalog:calorie_calculator")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/calorie_calculator.html",
        )


class FoodCalorieAIViewTests(AuthenticatedCatalogTestCase):
    @staticmethod
    def make_food_photo():
        output = io.BytesIO()
        Image.new("RGB", (640, 480), "orange").save(output, format="JPEG")
        return SimpleUploadedFile(
            "meal.jpg",
            output.getvalue(),
            content_type="image/jpeg",
        )

    def test_food_calorie_ai_page_loads(self):
        response = self.client.get(reverse("catalog:food_calorie_ai"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/food_calorie_ai.html")
        self.assertContains(response, "تحليل الوجبة وحساب السعرات")
        self.assertContains(response, 'enctype="multipart/form-data"')

    @override_settings(
        OPENAI_API_KEY="test-key",
        OPENAI_VISION_MODEL="gpt-5.6-terra",
    )
    @patch("catalog.views.analyze_food_image")
    def test_valid_food_photo_renders_structured_estimate(self, analyze_mock):
        analyze_mock.return_value = {
            "meal_name": "أرز ودجاج",
            "total_calories": 640,
            "confidence": "متوسطة",
            "items": [
                {
                    "name": "أرز",
                    "portion": "كوب واحد",
                    "calories": 240,
                },
                {
                    "name": "دجاج",
                    "portion": "150 غرامًا",
                    "calories": 400,
                },
            ],
            "assumptions": ["تم استخدام كمية متوسطة من الزيت"],
            "notes": ["اذكر وزن الدجاج لنتيجة أدق"],
        }

        response = self.client.post(
            reverse("catalog:food_calorie_ai"),
            {
                "photo": self.make_food_photo(),
                "meal_context": "طبق متوسط",
                "accept_ai_processing": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "أرز ودجاج")
        self.assertContains(response, "640")
        self.assertContains(response, "درجة الثقة: متوسطة")
        analyze_mock.assert_called_once()

    @override_settings(OPENAI_API_KEY="test-key")
    @patch("catalog.views.analyze_food_image")
    def test_invalid_upload_never_calls_ai_service(self, analyze_mock):
        response = self.client.post(
            reverse("catalog:food_calorie_ai"),
            {
                "photo": SimpleUploadedFile(
                    "not-food.txt",
                    b"not an image",
                    content_type="text/plain",
                ),
                "accept_ai_processing": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
        analyze_mock.assert_not_called()

    @patch("catalog.services.requests.post")
    def test_ai_service_sends_private_structured_vision_request(self, post_mock):
        api_response = Mock()
        api_response.raise_for_status.return_value = None
        api_response.json.return_value = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": (
                                '{"meal_name":"سلطة","total_calories":180,'
                                '"confidence":"متوسطة","items":[],'
                                '"assumptions":[],"notes":[]}'
                            ),
                        }
                    ],
                }
            ]
        }
        post_mock.return_value = api_response

        result = analyze_food_image(
            self.make_food_photo(),
            "طبق صغير",
            api_key="test-key",
            model="gpt-5.6-terra",
        )

        self.assertEqual(result["total_calories"], 180)
        request_kwargs = post_mock.call_args.kwargs
        self.assertFalse(request_kwargs["json"]["store"])
        self.assertEqual(request_kwargs["json"]["model"], "gpt-5.6-terra")
        self.assertEqual(
            request_kwargs["json"]["text"]["format"]["type"],
            "json_schema",
        )
        self.assertTrue(
            request_kwargs["json"]["input"][0]["content"][1][
                "image_url"
            ].startswith("data:image/jpeg;base64,")
        )


class WalkingStepsViewTests(AuthenticatedCatalogTestCase):
    def test_walking_steps_page_loads(self):
        response = self.client.get(
            reverse("catalog:walking_steps")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/walking_steps.html",
        )

    def test_home_page_links_to_walking_steps_page(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(
            response,
            f'href="{reverse("catalog:walking_steps")}"',
        )
        self.assertContains(response, "تابع خطواتك الآن")


class WeeklyPlanViewTests(AuthenticatedCatalogTestCase):
    def test_weekly_plan_page_loads(self):
        response = self.client.get(
            reverse("catalog:weekly_plan")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/weekly_plan.html",
        )

    def test_weekly_plan_contains_separate_detailed_schedules(self):
        response = self.client.get(
            reverse("catalog:weekly_plan")
        )
        training_plans = response.context["training_plans"]

        self.assertEqual(len(training_plans), 2)
        self.assertEqual(
            {plan["slug"] for plan in training_plans},
            {"home", "gym"},
        )

        for plan in training_plans:
            self.assertEqual(len(plan["days"]), 7)
            self.assertTrue(plan["level"])
            self.assertTrue(plan["equipment"])
            for day in plan["days"]:
                self.assertTrue(day["warmup"])
                self.assertTrue(day["cooldown"])
                self.assertTrue(day["note"])
                for exercise in day["exercises"]:
                    self.assertTrue(exercise["sets"])
                    self.assertTrue(exercise["repetitions"])
                    self.assertTrue(exercise["rest"])
                    self.assertTrue(exercise["coaching"])

        self.assertContains(response, "جدول تمارين المنزل")
        self.assertContains(response, "جدول تمارين النادي")
        self.assertContains(response, "المجموعات")
        self.assertContains(response, "توجيه الأداء الصحيح")
        self.assertContains(response, "طباعة الجدول")

    def test_home_page_links_to_weekly_plan(self):
        response = self.client.get(reverse("catalog:home"))

        self.assertContains(
            response,
            f'href="{reverse("catalog:weekly_plan")}"',
        )
        self.assertContains(
            response,
            "ابدأ الخطة الأسبوعية",
        )
