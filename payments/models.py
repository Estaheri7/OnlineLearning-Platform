from django.db import models

from users.models import CustomUser
from courses.models import Course

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ]

    user = models.ForeignKey(CustomUser, related_name='user_payments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course_payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_time = models.DateTimeField(auto_now_add=True)
