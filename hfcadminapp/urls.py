from django.urls import path
from . import views

urlpatterns = [ 
    path('adminlogin', views.adminlogin, name='adminlogin'),
    path('hfcadminhome', views.hfcadminhome, name='hfcadminhome'),
    path('hfcadminlogout', views.hfcadminlogout, name='hfcadminlogout'),
    path('news_announcements', views.news_announcements, name='news_announcements'),
    path('news_announcements_detail/<int:pk>', views.news_announcements_detail, name='news_announcements_detail'),    
    path('news_announcements_edit/<int:pk>/', views.news_announcements_edit, name='news_announcements_edit'),
    path('delete_news/<int:pk>/', views.delete_news, name='delete_news'),
    path('advertisement', views.advertisement, name='advertisement'),
    path('gallery', views.gallery, name='gallery'),
    path('delete_gallery/<int:pk>/', views.delete_gallery, name='delete_gallery'),
    path('careers', views.careers, name='careers'),
    path('delete_careers/<int:pk>/', views.delete_careers, name='delete_careers'),
    path('enquiries', views.enquiries, name='enquiries'),
    path('delete_messages/<int:pk>/', views.delete_messages, name='delete_messages'),
    path('ytvideo', views.ytvideo, name='ytvideo'),
    path('delete_ytvideo/<int:pk>/', views.delete_ytvideo, name='delete_ytvideo'),



]