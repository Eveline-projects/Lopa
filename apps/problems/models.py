import uuid

from django.db import models

DIFFICULTY_CHOICES = [
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
]


class Problem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        related_name='testcases',
    )
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)

    def __str__(self):
        return f"Test for {self.problem.title}"
