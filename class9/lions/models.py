from django.db import models


class Lion(models.Model):
    TRACK_CHOICES = [
        ('Django', 'Django'),
        ('SpringBoot', 'SpringBoot'),
        ('Frontend', 'Frontend'),
    ]

    name = models.CharField(max_length=30)
    track = models.CharField(max_length=30, choices=TRACK_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# ──────────────────────────────────────────────
# 1:N  Lion ─< Task  (기존)
# ──────────────────────────────────────────────
class Task(models.Model):
    """
    아기사자의 성장 과제 (1:N)
    - Lion 1명은 여러 Task를 가질 수 있다.
    - Lion 삭제 시 Task도 CASCADE 삭제된다.
    """
    lion = models.ForeignKey(
        Lion,
        on_delete=models.CASCADE,
        related_name='tasks',      # lion.tasks.all() 역방향 접근
    )
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.title} ({self.lion.name})"


# ──────────────────────────────────────────────
# 1:1  Lion ─ LionProfile  (신규)
# ──────────────────────────────────────────────
class LionProfile(models.Model):
    """
    아기사자 프로필 (1:1)
    - Lion 1명은 정확히 1개의 프로필을 가진다.
    - OneToOneField: ForeignKey + unique=True 와 동일한 효과
    - 단방향: profile.lion 으로만 접근 (역방향 기본값: lion.lionprofile)
    - Lion 삭제 시 Profile도 CASCADE 삭제된다.
    """
    lion = models.OneToOneField(
        Lion,
        on_delete=models.CASCADE,
        related_name='profile',    # lion.profile 로 역방향 접근
    )
    github_url = models.URLField(blank=True, verbose_name='GitHub URL')
    bio = models.TextField(blank=True, verbose_name='자기소개')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lion.name}의 프로필"


# ──────────────────────────────────────────────
# N:M  Lion ─── Tag  (신규)
# ──────────────────────────────────────────────
class Tag(models.Model):
    """
    관심 기술 태그 (N:M)
    - Lion 1명은 여러 Tag를 가질 수 있고,
      Tag 1개는 여러 Lion에 사용될 수 있다.
    - ManyToManyField: Django가 중간 테이블(lions_lion_tags)을 자동 생성한다.
    - 양방향 접근:
        lion.tags.all()       — Lion → Tag 방향
        tag.lions.all()       — Tag → Lion 역방향 (related_name='lions')
    """
    name = models.CharField(max_length=50, unique=True, verbose_name='태그명')
    lions = models.ManyToManyField(
        Lion,
        related_name='tags',       # lion.tags.all() 역방향 접근
        blank=True,
    )

    def __str__(self):
        return self.name
