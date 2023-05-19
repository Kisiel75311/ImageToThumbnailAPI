# urls.py

from django.urls import path
from .views import ImageUploadView, ImageListView, UserProfileView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload'),
    path('images/', ImageListView.as_view(), name='image_list'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
