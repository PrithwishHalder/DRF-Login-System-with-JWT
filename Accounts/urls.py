from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    # Simple-JWT views from Login and Token Refresh

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Routes
    path('', views.index, name="routes"),

    # Register User
    path('register/', views.Register, name="Register user"),

    # Reset Password
    path('reset/', views.Reset, name="Reset user"),

    # Forget Psssword
    path('forget/', views.ForgotPass, name="Forget Password"),
    # Forget Psssword Reset
    path('passReset/', views.ForgetPassReset, name="Forget Password Reset"),

    # User info if Loged In
    path('pages/', views.pages, name="Pages"),

    # Logout User
    path('logout/', views.logout, name="Logout"),
]
