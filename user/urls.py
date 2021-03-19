from django.urls import path
from user import views


urlpatterns = [
    path('reg/', views.reg),
    path('login/', views.login),
    path('test/', views.test),
]
