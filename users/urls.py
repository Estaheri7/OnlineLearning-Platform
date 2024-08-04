from django.urls import path

from .views import RegisterView, LoginView, UserView, UserProfileView, UserDetailView, TokenGeneratorView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('get-token/', TokenGeneratorView.as_view()),
    path('users/', UserView.as_view()),
    path('users/<str:username>/', UserDetailView.as_view()),
    path('user-profile/<str:username>/', UserProfileView.as_view()),
]