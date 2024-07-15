from django.urls import path
from . import views


urlpatterns = [
    path('floor-list/', views.FloorParentListAPIView.as_view()),
    path('floor-create/', views.FloorParentListAPIView.as_view()),
    path('room-list/<int:pk>/', views.FloorChildListAPIView.as_view()),
    path("floor/update/<int:pk>/", views.FloorUpdateAPIView.as_view()),

    path('attendance/<int:pk>/', views.AttendanceUpdateAPIView.as_view(), name='attendance_detail'),
    path('attendance/date/', views.AttendanceFloorListAPIView.as_view(), name='attendances'),

    path('group/create/', views.GroupCreateAPIView.as_view(), name='login'),
    path('group/list/', views.GroupCreateAPIView.as_view(), name='login'),

]

