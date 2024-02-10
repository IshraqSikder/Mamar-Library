from django.urls import path
from .views import UserRegistrationView, UserLoginView ,UserLibraryAccountUpdateView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', UserLibraryAccountUpdateView.as_view(), name='profile' ),
    path('change_password/', views.pass_change, name='change_password'),
]