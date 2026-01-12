from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('customer/', views.customer_dashboard, name='customer_dashboard'),
    path('employee/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/permit/<int:permit_id>/', views.employee_permit_detail, name='employee_permit_detail'),
    path('employee/permit/<int:permit_id>/email/', views.send_email, name='send_email'),
    path('permit/<int:permit_id>/comment/', views.add_comment, name='add_comment'),
    path('employee/companies/', views.company_list, name='company_list'),
    path('employee/company/<int:company_id>/', views.company_detail_employee, name='company_detail_employee'),
    path('attachment/<int:attachment_id>/download/', views.download_email_attachment, name='download_email_attachment'),
]