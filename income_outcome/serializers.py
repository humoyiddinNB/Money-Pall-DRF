from rest_framework import serializers
from .models import IncomeCategory, ExpenseCategory, Expense

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'name', 'image']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'name', 'image']


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())

    class Meta:
        model = Expense
        fields = ['id', 'amount', 'category', 'currency', 'description', 'date']