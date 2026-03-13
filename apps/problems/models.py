import uuid

from django.db import models

DIFFICULTY_CHOICES = [('easy', 'easy'),
                      ('medium', 'medium'),
                      ('hard', 'hard'),
                      ]


class Problem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=200, choices=DIFFICULTY_CHOICES, default='easy')
    category = models.CharField(max_length=200)
