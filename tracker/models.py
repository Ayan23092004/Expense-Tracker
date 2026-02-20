from django.db import models
from django.contrib.auth.models import User  #


class Expense(models.Model):
    # Defining specific categories for consistent data analysis
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Bills', 'Bills'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.category} - ${self.amount}"