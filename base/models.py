from django.db import models

# Create your models here.
class EventDates(models.Model):
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    name = models.CharField(default="",max_length=100)

    def __str__(self) -> str:
        return self.name + ' starts at : '+self.event_start.isoformat() + ' ends at : '+self.event_end.isoformat()