import uuid
from django.conf import settings
from django.db import models


class Submission(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        DONE = 'DONE', 'Done'
        WRONG_ANSWER = 'WRONG_ANSWER', 'Wrong answer'
        ERROR = 'ERROR', 'Error'

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


class Result(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PASSED = 'PASSED', 'Passed'
        WRONG_ANSWER = 'WRONG_ANSWER', 'Wrong Answer'
        TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'
        RUNTIME_ERROR = 'RUNTIME_ERROR', 'Runtime Error'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name='results',
    )
    test_case = models.ForeignKey(
        'problems.TestCase',
        on_delete=models.CASCADE,
        related_name='results',
    )
    status = models.CharField(
        choices=Status.choices,
        max_length=25,
        default=Status.PENDING,
    )
    actual_output = models.TextField(
        null=True,
        blank=True,
    )
    execution_time = models.FloatField(default=0.0)

    class Meta:
        ordering = ['test_case__id']

    def __str__(self):
        return f"Result {self.id} - {self.status}"
