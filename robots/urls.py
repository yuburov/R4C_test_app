from django.urls import path
from robots import views

app_name = 'robots'

urlpatterns = [
    path('api/create_robot/', views.create_robot, name='create_robot'),
]