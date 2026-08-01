from django.urls import path

from . import views


app_name = "catalog"


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "calorie-calculator/",
        views.calorie_calculator,
        name="calorie_calculator",
    ),
    path(
        "ai-food-calories/",
        views.food_calorie_ai,
        name="food_calorie_ai",
    ),
    path(
        "walking-steps/",
        views.walking_steps,
        name="walking_steps",
    ),
    path(
        "weekly-plan/",
        views.weekly_plan,
        name="weekly_plan",
    ),
    path("exercises/", views.exercise_list, name="exercise_list"),
    path(
        "healthy-food/",
        views.healthy_food_list,
        name="healthy_food_list",
    ),
]
