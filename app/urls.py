from rest_framework import routers
from django.urls import path
from . import views

router = routers.DefaultRouter()
router.register("dishmodel", views.DishModelView, basename="dishmodel"),
urlpatterns = [
    path("categorycreate/", views.CategoryCreateView.as_view(), name="categorycreate"),
    path("category/<int:pk>/", views.CategoryViewFunctionDishes, name="category"),
    path("dishes/<int:pk>/", views.DishViewFunction, name="dishes"),
    path("updatedish/<int:pk>/", views.DishUpdateViewFunction, name="updatedish"),
    path("updatecategory/<int:pk>/", views.CategoryUpdateViewFunction, name="updatecategory"),
        path("alldishes/<int:state>/", views.AllDishViewFunction, name="alldishes"),
        path("dishPrice/<int:price>/", views.DishByPriceFunc, name="dishPrice"),
        path("allcategories/", views.AllCategoryViewFunction, name="allcategories"),
        path("addfeedback/", views.AddFeedBack, name="addfeedback"),
        path("allfeedback/", views.AllFeedback, name="allfeedback"),
        path("feedback/<int:pk>/", views.FeedbackById, name="feedback"),
        path("editfeedback/<int:pk>/", views.EditFeedbackById, name="editfeedback"),
    path("featuredishes/", views.FeaturedDishesView, name="featuredishes"),
] + router.urls