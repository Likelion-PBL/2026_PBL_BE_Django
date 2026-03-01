from django.db import models


class Lion(models.Model):
    TRACK_CHOICES = [
        ('Django', 'Django'),
        ('SpringBoot', 'SpringBoot'),
        ('Frontend', 'Frontend'),
    ]

    name = models.CharField(max_length=100, verbose_name='이름')
    track = models.CharField(
        max_length=50,
        choices=TRACK_CHOICES,
        blank=True,
        verbose_name='트랙',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '아기사자'
        verbose_name_plural = '아기사자 목록'

    def __str__(self):
        return f"{self.name} ({self.track})"
