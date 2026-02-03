from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView

from measurement.models import Measurement, Sensor
from measurement.serializers import MeasurementSerializer, SensorDetailSerializer


class SensorListView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class  = SensorDetailSerializer

class SensorUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class  = SensorDetailSerializer

class MeasurementCreateView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer