from django.urls import path
from .views import ProfileDetailView, UpdateProfileView, following_list


urlpatterns = [
    path('followings/', following_list, name='following_list'),

    path('<slug>/', ProfileDetailView.as_view(), name='profile_page'),



    path('<str:slug>/update_profile/', UpdateProfileView.as_view(), name='update_profile'),


]
