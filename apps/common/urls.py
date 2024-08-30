from django.urls import path
from . import views


create_floor = views.FloorViewSets.as_view({'post': 'create'})
delete_floor = views.FloorViewSets.as_view({'delete': 'destroy'})
list_floor = views.FloorViewSets.as_view({'get': 'list'})
detail_floor = views.FloorViewSets.as_view({'get': 'retrieve'})
update_floor = views.FloorViewSets.as_view({'patch': 'partial_update'})


create_payment = views.StudentPaymentViewSets.as_view({'post': 'create'})
delete_payment = views.StudentPaymentViewSets.as_view({'delete': 'destroy'})
list_payment = views.StudentPaymentViewSets.as_view({'get': 'list'})
detail_payment = views.StudentPaymentViewSets.as_view({'get': 'retrieve'})
update_payment = views.StudentPaymentViewSets.as_view({'patch': 'partial_update'})


urlpatterns = [
    path('floor-list/', list_floor),
    path('floor-create/', create_floor),
    path("floor/update/<int:pk>/", update_floor),
    path("floor/destroy/<int:pk>/", delete_floor),
    path("room-list/<int:pk>/", views.RoomsListAPIView.as_view()),
    path("room/destroy/<int:pk>/", views.RoomDestroyAPIView.as_view()),

    path('attendance/<int:pk>/', views.AttendanceUpdateAPIView.as_view(), name='attendance_detail'),
    path('attendance/date/', views.AttendanceFloorListAPIView.as_view(), name='attendances'),

    path('group/create/', views.GroupCreateAPIView.as_view(), name='login'),
    path('group/list/', views.GroupCreateAPIView.as_view(), name='login'),

    path('application-student/create/', views.ApplicationCreateAPIView.as_view(), name='application_student_create'),
    path('student/applications/', views.StudentApplicationListAPIView.as_view(), name='application_student_list'),

    path('student-payment/create/', create_payment),
    path('student-payment/update/<int:pk>', update_payment),
    path('student-payment/destroy/<int:pk>/', delete_payment),
    path('student-payment/list/', list_payment),

]

