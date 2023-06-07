from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("newuser/", views.AuthSerializerView.as_view(), name="newuser"),
        path(
        "customerupdate/<int:user__id>/",
        views.CustomerProfileUpdateView.as_view(),
        name="customerupdate",
    ),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]