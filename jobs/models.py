from django.conf import settings
from django.db import models


class Job(models.Model):

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    title = models.CharField(max_length=150)

    description = models.TextField()

    location = models.CharField(max_length=100)

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=[
            ('APPLIED', 'Applied'),
            ('SELECTED', 'Selected'),
            ('REJECTED', 'Rejected'),
        ],
        default='APPLIED'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'job'],
                name='unique_employee_job_application'
            )
        ]

    def __str__(self):
        return f"{self.employee.email} - {self.job.title}"