from django.urls import path
from . import views
urlpatterns = [
    path('',views.login, name='login'),
    path('index',views.index, name='index'),
    path('login',views.login, name='login'),
    path('userform',views.userform, name='userform'),
    path('registerattendance',views.registerattendance, name='registerattendance'),
    path('admin',views.admin, name='admin'),
    path('adminviewattendance',views.adminviewattendance, name='adminviewattendance'),
    path('searchbydate',views.searchbydate, name='searchbydate'),
    path('addmeetdate',views.addmeetdate, name='addmeetdate'),
]

