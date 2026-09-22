from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    path('course/<int:course_id>/exam/', views.exam, name='exam'),
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]