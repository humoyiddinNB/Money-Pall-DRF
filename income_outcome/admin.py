from django.contrib import admin

from income_outcome.models import Income, Expense, IncomeCategory, ExpenseCategory

admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
