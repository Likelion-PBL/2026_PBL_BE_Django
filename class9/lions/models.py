from django.db import models

class Lion(models.Model):
    name = models.CharField(max_length=30)
    track = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    lion = models.ForeignKey(
        Lion,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.lion.name})"