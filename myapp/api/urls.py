# myapp/api/urls.py
from django.urls import path
from .views import (
    ItemListCreateAPIView,
    ItemRetrieveUpdateDestroyAPIView,
    ChatMessageListCreateAPIView,
    ActivityListAPIView,
    UserProfileRetrieveUpdateAPIView
)

app_name = 'api'

urlpatterns = [
    path('items/', ItemListCreateAPIView.as_view(), name='item-list'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyAPIView.as_view(), name='item-detail'),
    path('chat/', ChatMessageListCreateAPIView.as_view(), name='chat-list'),
    path('activity/', ActivityListAPIView.as_view(), name='activity-list'),
    path('profile/', UserProfileRetrieveUpdateAPIView.as_view(), name='profile'),
]