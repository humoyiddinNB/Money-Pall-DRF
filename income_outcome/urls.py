from django.urls import path
from .views import DashboardAPIView, AddIncomeAPIView, AddIncomeCategoryAPIView, AddExpenseView, AddExpenseCategoryView

urlpatterns = [
    path('dashboard', DashboardAPIView.as_view(), name='dashboard'),
    path('add_income_category', AddIncomeCategoryAPIView.as_view(), name='add_income_category'),
    path('add_income', AddIncomeAPIView.as_view(), name='add_income'),
    path('add_expense', AddExpenseView.as_view(), name='add_expense'),
    path('add_expense_category', AddExpenseCategoryView.as_view(), name='add_expense_category')
]