from django.urls import path
from .views import UserProfileView, UserImageView, UserImageDetailView, UserListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('images/', UserImageView.as_view(), name='user_images'),
    path('images/<int:image_id>/', UserImageDetailView.as_view(), name='user_image_detail'),
    path('chat-users/', UserListView.as_view(), name='chat-users'),

] 