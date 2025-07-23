from django.db import models
from django.contrib.auth.models import User
import json



class Website(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name
    
    def get_latest_check(self):
        return self.status_checks.order_by('-timestamp').first()
    
    def get_sparkline_data(self):
        checks = self.status_checks.order_by('timestamp').all()[:24]
        return [check.response_time if check.response_time is not None else 0 for check in checks]

    def get_sparkline_json(self):
        dummy_data = self.get_sparkline_data()
        return json.dumps(dummy_data)




class StatusCheck(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='status_checks')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_up = models.BooleanField()
    status_code = models.PositiveIntegerField(null=True, blank=True)
    response_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        status = "Up" if self.is_up else "Down"
        return f"{self.website.name} - {status} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    

