from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('customers/token/refresh/', views.JWTTokenRefreshView.as_view(), name='customer_token_refresh'),

    path('customers/', views.CustomerCreateListView.as_view(), name='customer_create_list'),
    path('customers/signup/', views.CustomerSignupView.as_view(), name='customer_signup'),
    path('customers/login/', views.CustomerLoginView.as_view(), name='customer_login'),
    path('customers/logout/', views.CustomerLogoutView.as_view(), name='customer_logout'),
    path('customers/<uuid:pk>/', views.CustomerRetrieveUpdateDestroyView.as_view(), name='customer_retrieve_update_destroy'),
    path('customers/profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
]