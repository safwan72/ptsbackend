from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register("dishmodel", views.DishModelView, basename="dishmodel"),
urlpatterns = [
    path("categorycreate/", views.CategoryCreateView.as_view(), name="categorycreate"),
    path("category/<int:pk>/", views.CategoryViewFunctionDishes, name="category"),
    path("dishes/<int:pk>/", views.DishViewFunction, name="dishes"),
        path("alldishes/", views.AllDishViewFunction, name="alldishes"),
    path("featuredishes/", views.FeaturedDishesView, name="featuredishes"),
] + router.urls