from django.urls import path, include 
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include('myapp.api.urls', namespace='api')),   
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('items/', views.item_list, name='item_list'),
    path('items/new/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_update, name='item_update'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]