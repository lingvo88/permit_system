from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
    path('', views.company_detail, name='detail'),
    path('edit/', views.company_edit, name='edit'),
    path('user/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('payment/add/', views.payment_method_add, name='payment_add'),
    path('payment/<int:payment_id>/delete/', views.payment_method_delete, name='payment_delete'),
]

