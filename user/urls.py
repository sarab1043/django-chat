# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('',views.signin,name="signin"),
    path('signout/',views.signout,name="signout"),
    # path('user_profile/<int:id>/', views.user_profile, name = "user_profile")
]