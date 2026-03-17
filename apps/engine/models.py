import uuid
from django.conf import settings
from django.db import models
from apps.problems.models import Problem


class Submission(models.Model):
    STATUS_CHOICES = [
        ('done', 'done'),
        ('wrong_answer', 'wrong answer'),
        ('error', 'error'),
    ]
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    code = models.TextField()
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=15,
        default='error'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.status}'
