from django.urls import path
from post import views


urlpatterns = [
    path('', views.get_all),
    path('<int:post_id>', views.get_one),
    path('publish/', views.publish),
]
