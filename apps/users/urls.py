from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('create/student/', views.CreateStudentWithApartmentAPIView.as_view(), name='create_student'),
    path('student/list/', views.StudentsListAPIView.as_view(), name='login'),
    path('employee/list/', views.EmployeeListAPIView.as_view()),
    path('students/<int:pk>/', views.StudentsListAPIView.as_view(), name='login'),

]

