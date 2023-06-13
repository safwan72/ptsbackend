from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("allusers/", views.Allusers, name="allusers"),
    path("newuser/", views.AuthSerializerView.as_view(), name="newuser"),
    path("newadmin/", views.CustomAdminCreateView.as_view(), name="newadmin"),
    path("newcustomer/", views.CustomCustomerCreateView.as_view(), name="newcustomer"),
        path(
        "customerupdate/<int:user__id>/",
        views.CustomerProfileUpdateView.as_view(),
        name="customerupdate",
    ),
        path(
        "adminupdate/<int:user__id>/",
        views.adminProfileUpdateView.as_view(),
        name="adminupdate",
    ),
    path("token/", views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]