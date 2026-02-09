from django.db import models

# 기본 PBL 코드
# class Lion(models.Model):
#     name = models.CharField(max_length=50)
#     track = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.name} ({self.track})"

# 보너스
class Lion(models.Model):
    TRACK_CHOICES = [
        ('Django', 'Django'),
        ('SpringBoot', 'SpringBoot'),
        ('Frontend', 'Frontend'),
    ]

    name = models.CharField(max_length=20)
    track = models.CharField(max_length=20, choices=TRACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.track})'
