import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Result(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PASSED = 'PASSED', 'Passed'
        WRONG_ANSWER = 'WRONG_ANSWER', 'Wrong Answer'
        TIME_LIMIT_EXCEEDED = 'TIME_LIMIT_EXCEEDED', 'Time Limit Exceeded'
        RUNTIME_ERROR = 'RUNTIME_ERROR', 'Runtime Error'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(
        'submissions.Submission',
        on_delete=models.CASCADE,
        related_name='results',
    )
    test_case = models.ForeignKey(
        'test_cases.TestCase',
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
    execution_time = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )

    class Meta:
        ordering = 'test_case__id'

    def __str__(self):
        return f'Result {self.id} - {self.status}'
