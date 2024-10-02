from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.fooddata, name='home'),
    path('home/', views.fooddata, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('view/', views.view_documents, name='view_documents'),
    path('data_summary/', views.data_summary, name='data_summary'),  # Updated path for summary
    path('test_form/', views.test_form, name='test_form'),
    ] 
