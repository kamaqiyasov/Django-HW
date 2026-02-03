from django.urls import path

from measurement.views import MeasurementCreateView, SensorListView, SensorUpdateView

urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<int:pk>/', SensorUpdateView.as_view()),
    path('measurements/', MeasurementCreateView.as_view()),
]
