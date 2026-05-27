import uuid
from django.core.exceptions import ValidationError
from django.db import models


class TestCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='test_cases',
    )
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=False)

    def clean(self):
        errors = {}

        if not self.input_data or not self.input_data.strip():
            errors['input_data'] = 'Input data cannot be empty'

        if not self.expected_output or not self.expected_output.strip():
            errors['expected_output'] = 'Expected output cannot be empty'

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'Test for {self.problem.title}'


# Prevent pytest from collecting this Django model as a test class.
TestCase.__test__ = False
