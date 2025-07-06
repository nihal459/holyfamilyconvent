from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('view_announcements', views.view_announcements, name='view_announcements'),
    path('view_gallery', views.view_gallery, name='view_gallery'),
    path('view_careers', views.view_careers, name='view_careers'),
    path('view_contact', views.view_contact, name='view_contact'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('admission', views.admission, name='admission'),
    path('academics', views.academics, name='academics'),


    

    

]