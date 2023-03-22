from django.urls import path, include
from . import views
from .views import CreateBookingView, OrderHistoryView

urlpatterns = [
    path('login/', views.LoginSignup.as_view(), name='login'),
    path('', views.Welcome.as_view(), name='welcome'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot'),
    path('order_history/', views.OrderHistoryView.as_view(), name='order_history'),
    path('booking/create/', CreateBookingView.as_view(), name='create_booking'),

]
