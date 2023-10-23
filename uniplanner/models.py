from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta
import datetime
class User(AbstractUser):
    pass

class event(models.Model):
    username = models.CharField(max_length=30)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField()

    def serialize(self):
        return {
            "username":self.username,
            "event_name":self.event_name,
            "event_year": self.event_date.year,
            "event_month": self.event_date.strftime('%b'),
            "event_day": self.event_date.day,
            "event_time": self.event_time,
        }
    

class module(models.Model):
    name = models.CharField(max_length=60)

class usermodule(models.Model):
    module_id = models.ForeignKey(module, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    def serialize(self):
        return {
            "module_id": self.module_id,
            "username": self.username
        }

class toask(models.Model):
    module_id = models.ForeignKey(module, on_delete=models.CASCADE)
    toask = models.TextField()
    answered_date = models.DateField(null=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "module_id": self.module_id,
            "toask": self.toask,
            "answered_date":self.answered_date
        }
    
class deadline(models.Model):
    module_id = models.ForeignKey(module, on_delete=models.CASCADE)
    task = models.CharField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=30, default="undone")
    priority = models.CharField(max_length=10)
    def serialize(self):
        return {
            "id": self.id,
            "module_id": self.module_id.id,
            "task":  self.task,
            "date": self.date,
            "time": self.time,
            "status": self.status,
            "remaining_days": (self.date - date.today()).days,
            "remaining_time": (datetime.datetime.combine(self.date,self.time) - datetime.datetime.now()).total_seconds(),
            "priority": self.priority
        }
