from django.urls import path
from . import views

app_name = 'permits'

urlpatterns = [
    path('', views.permit_list, name='list'),
    path('new/', views.permit_create, name='create'),
    path('<int:permit_id>/', views.permit_detail, name='detail'),
    path('<int:permit_id>/edit/', views.permit_edit, name='edit'),
    path('<int:permit_id>/copy/', views.permit_copy, name='copy'),
    path('<int:permit_id>/delete/', views.permit_delete, name='delete'),
    path('document/<int:document_id>/download/', views.permit_document_download, name='document_download'),
]

