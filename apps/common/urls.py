from django.urls import path
from . import views


urlpatterns = [
    path('floor-list/', views.FloorParentListAPIView.as_view()),
    path('room-list/<int:pk>/', views.FloorChildListAPIView.as_view()),

]

