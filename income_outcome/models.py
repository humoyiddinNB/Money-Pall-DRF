from django.db import models
import datetime

class IncomeCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_pics/', default='category_pics/def_categ.png')

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_pics/', default='category_pics/def_categ.png')

    def __str__(self):
        return self.name


class Income(models.Model):
    CURRENCY_TYPES = [
        ('D', 'DOLLAR'),
        ('S', 'SUM'),
        ('C', 'CREDIT_CARD')
    ]
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(IncomeCategory, on_delete=models.CASCADE)
    currency = models.CharField(max_length=1, choices=CURRENCY_TYPES, default='S')
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Income: {self.amount} {self.currency}"


class Expense(models.Model):
    CURRENCY_TYPES = [
        ('D', 'DOLLAR'),
        ('S', 'SUM'),
        ('C', 'CREDIT_CARD')
    ]
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    currency = models.CharField(max_length=1, choices=CURRENCY_TYPES, default='S')
    description = models.TextField(null=True, blank=True)
    date = models.DateField(default=datetime.date.today, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expense: {self.amount} {self.currency}"