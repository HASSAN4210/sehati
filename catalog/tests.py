from django.test import TestCase
from django.urls import reverse
from django.templatetags.static import static


class ExerciseListViewTests(TestCase):
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

        self.assertEqual(len(exercises), 12)
        self.assertEqual(len(home_exercises), 6)
        self.assertEqual(len(gym_exercises), 6)

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


class HealthyFoodListViewTests(TestCase):
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

        self.assertEqual(len(nutrition_items), 10)
        self.assertEqual(len(food_items), 5)
        self.assertEqual(len(drink_items), 5)

        for item in nutrition_items:
            self.assertTrue(item["benefits"])
            self.assertContains(
                response,
                static(item["image"]),
            )


class HomePageTests(TestCase):
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


class CalorieCalculatorViewTests(TestCase):
    def test_calorie_calculator_page_loads(self):
        response = self.client.get(
            reverse("catalog:calorie_calculator")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/calorie_calculator.html",
        )


class WalkingStepsViewTests(TestCase):
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


class WeeklyPlanViewTests(TestCase):
    def test_weekly_plan_page_loads(self):
        response = self.client.get(
            reverse("catalog:weekly_plan")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog/weekly_plan.html",
        )

    def test_weekly_plan_contains_seven_complete_days(self):
        response = self.client.get(
            reverse("catalog:weekly_plan")
        )
        plan_days = response.context["plan_days"]

        self.assertEqual(len(plan_days), 7)

        for day in plan_days:
            self.assertTrue(day["exercise"])
            self.assertTrue(day["meals"])
            self.assertTrue(day["calories"])
            self.assertGreater(day["steps_value"], 0)

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
