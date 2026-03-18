import uuid
from django.conf import settings
from django.db import models


class Submission(models.Model):
    class Status(models.TextChoices):
        DONE = 'done', 'Done'
        WRONG_ANSWER = 'wrong_answer', 'Wrong answer'
        PENDING = 'pending', 'Pending'
        ERROR = 'error', 'Error'

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
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=Status.choices,
        max_length=15,
        default=Status.PENDING,
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.status}'
