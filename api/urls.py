from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )

from .views import ( 
    SignupView,
    ProfileView,
    FollowersView,
    FollowingsView,
    PostRetrieveView,
    PostDeleteView,
    PostUpdateView,
    PostCreateView
    )


urlpatterns = [
    # token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('signup/', SignupView.as_view()),
    
    path('<str:username>/', ProfileView.as_view()),
    
    path('followers/<str:username>/', FollowersView.as_view()),
    path('followings/<str:username>/', FollowingsView.as_view()),
    
    

    path('posts/<str:username>/', PostRetrieveView.as_view()),

    path('post/create/', PostCreateView.as_view()),        
    path('post/delete/<int:pk>/', PostDeleteView.as_view()),    
    path('post/update/<int:pk>/', PostUpdateView.as_view()),    
    
    
]