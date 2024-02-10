from django.urls import path, include
from . import views

urlpatterns = [
    path('details/<int:id>', views.post_details, name = 'details_post'),
]