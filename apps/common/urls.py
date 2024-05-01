from django.urls import path
from . import views


urlpatterns = [
    path('floor-list/', views.FloorListAPIView.as_view()),
]

