from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('create/student/', views.CreateStudentWithApartmentAPIView.as_view(), name='create_student'),
    path('students/<int:pk>/', views.StudentsListAPIView.as_view(), name='login'),
    path('employees/', views.EmployeeListAPIView.as_view())

]

