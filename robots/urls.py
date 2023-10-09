from django.urls import path
from robots import views
from robots.views import GenerateReportView

app_name = 'robots'

urlpatterns = [
    path('api/create_robot/', views.create_robot, name='create_robot'),
    path('generate_report/', GenerateReportView.as_view(), name='generate_report'),

]