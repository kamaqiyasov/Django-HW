from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
class Measurement(models.Model):
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, blank=True, null=True, related_name='measurements')
    
    image = models.ImageField(blank=True, null=True)