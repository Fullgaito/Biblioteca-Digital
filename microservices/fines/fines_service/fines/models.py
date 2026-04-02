from django.db import models

class Fine(models.Model):
    user_id = models.IntegerField()
    loan_id = models.CharField(max_length=50)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    days_late = models.IntegerField()

    status = models.CharField(max_length=20, default='pending')

    paid_at = models.DateTimeField(null=True, blank=True)
