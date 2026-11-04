from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    completed = models.BooleanField(default=False)

    reminder_2_days_sent = models.BooleanField(default=False)
    reminder_1_day_sent = models.BooleanField(default=False)
    reminder_today_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title