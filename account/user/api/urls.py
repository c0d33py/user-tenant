from django.urls import path
from rest_framework_simplejwt.views import (TokenBlacklistView,
                                            TokenRefreshView, TokenVerifyView)

from .views import *

urlpatterns = [
    # API URLS for AJAX requests from the frontend (React) to the backend (Django)
    # for user authentication and registration
    path('user/', UserAPIView.as_view(), name='user'),  # user project API
    path('register/', UserRegisterAPIView.as_view(), name='register-api'),  # register user
    path('login/', UserLoginAPIView.as_view(), name='token_obtain_pair'),  # login
    path('profile/', UserProfileAPIView.as_view(), name='profile'),  # get user profile
    path('profile/picture/', UserProfilePictureUpdateAPIView.as_view(), name='profile-picture'),  # Profile picture update
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # verify token
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),  # for logout
    path('change-password/', UserPasswordChangeAPIView.as_view(), name='change-password'),  # Password change API
    path('email-verify/<uidb64>/<token>/', UserEmailVerifyAPIView.as_view(), name='email-verify'),  # Email Verification
    path('password-reset-token/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-token'),  # password reset token check API for frontend
    path('reset-password/', RequestPasswordResetEmail.as_view(), name='reset-password'),  # password reset API for frontend
    path('password-reset-confirm/<uidb64>/<token>/', UserPasswordResetAPIView.as_view(), name='password-reset-confirm'),  # password reset confirm API for frontend
    # User Interests API
    path('user-interest/', UserInterestAPIView.as_view(), name='user_interest'),  # user interest API
    path('user-services/', UserServicesAPIView.as_view(), name='user_services'),  # user service API
    # User Experience API
    path('user-experience/', UserExperienceAPIView.as_view(), name='user_experience'),  # user experience API
    path('user-experience/<int:pk>/', UserExperienceDetailAPIView.as_view(), name='user_experience_detail'),  # user experience detail API

    # User Education API
    path('user-education/', UserEducationAPIView.as_view(), name='user_education'),  # user education API
    path('user-education/<int:pk>/', UserEducationDetailAPIView.as_view(), name='user_education_detail'),  # user education detail API

    # USER CRUD API
    path('user-list/', UserListView.as_view(), name='user-list-api'),
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user-detail-api'),
    path('user-create/', UserCreateView.as_view(), name='user-create-api'),
    path('user-update/<int:pk>/', UserUpdateView.as_view(), name='user-update-api'),
    path('user-delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete-api'),


    # path('profile/', ProfileView.as_view(), name='profile'),
    # path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    # path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),
    # path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    # path('profile/<int:pk>/change-password/', ProfileChangePasswordView.as_view(), name='profile-change-password'),
]
