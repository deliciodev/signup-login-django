from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('customers/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('customers/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('customers/', views.CustomerCreateListView.as_view(), name='customer_create_list'),
    path('customers/signup/', views.CustomerSignupView.as_view(), name='customer_signup'),
    path('customers/login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('customers/logout/', views.CustomerLogoutView.as_view(), name='customer_logout'),
    path('customers/<uuid:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view(), name='customer_retrieve_update_destroy'),
]