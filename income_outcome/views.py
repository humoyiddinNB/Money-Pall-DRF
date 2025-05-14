from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from .models import Income, Expense, IncomeCategory, ExpenseCategory
from .serializers import IncomeCategorySerializer, ExpenseCategorySerializer, ExpenseSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Dashboard statistikasi",
        operation_description="Foydalanuvchining daromad, xarajat va balans statistikasi: kunlik, haftalik, oylik va yillik bo‘yicha.",
        responses={
            200: openapi.Response(
                description="Statistik ma'lumotlar",
                examples={
                    "application/json": {
                        "total_income": 12000,
                        "total_expense": 8000,
                        "balance": 4000,
                        "daily_income": 200,
                        "daily_expense": 100,
                        "weekly_income": 1500,
                        "weekly_expense": 800,
                        "monthly_income": 6000,
                        "monthly_expense": 4000,
                        "yearly_income": 12000,
                        "yearly_expense": 8000
                    }
                }
            ),
            401: openapi.Response(description="Avtorizatsiya talab qilinadi")
        }
    )
    def get(self, request):
        user = request.user

        incomes = Income.objects.filter(user=user).order_by('-date')
        expenses = Expense.objects.filter(user=user).order_by('-date')

        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)

        total_income = sum(i.amount for i in incomes)
        total_expense = sum(e.amount for e in expenses)
        balance = total_income - total_expense

        data = {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "daily_income": sum(i.amount for i in incomes.filter(date=today)),
            "daily_expense": sum(e.amount for e in expenses.filter(date=today)),
            "weekly_income": sum(i.amount for i in incomes.filter(date__gte=week_ago)),
            "weekly_expense": sum(e.amount for e in expenses.filter(date__gte=week_ago)),
            "monthly_income": sum(i.amount for i in incomes.filter(date__gte=month_ago)),
            "monthly_expense": sum(e.amount for e in expenses.filter(date__gte=month_ago)),
            "yearly_income": sum(i.amount for i in incomes.filter(date__gte=year_ago)),
            "yearly_expense": sum(e.amount for e in expenses.filter(date__gte=year_ago)),
        }

        return Response(data)


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser

class AddIncomeCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_summary="Yangi income kategoriyasi qo‘shish",
        request_body=IncomeCategorySerializer,
        responses={
            201: openapi.Response(description="Income kategoriyasi qo‘shildi"),
            400: openapi.Response(description="Xatolik mavjud")
        }
    )
    def post(self, request):
        serializer = IncomeCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Income kategoriyasi muvaffaqiyatli qo'shildi.",
                'status': status.HTTP_201_CREATED
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AddIncomeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Yangi income qo‘shish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["amount", "category", "currency"],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, example=250.00),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, example="USD"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, example="Freelance to‘lovi"),
                'date': openapi.Schema(type=openapi.FORMAT_DATE, example="2025-05-13"),
            }
        ),
        responses={
            201: openapi.Response(
                description="Income muvaffaqiyatli qo‘shildi",
                examples={
                    "application/json": {
                        "message": "Income muvaffaqiyatli qo‘shildi.",
                        "income_id": 5
                    }
                }
            ),
            400: openapi.Response(description="Noto‘g‘ri ma'lumot"),
            404: openapi.Response(description="Kategoriya topilmadi")
        }
    )
    def post(self, request):
        amount = request.data.get('amount')
        category_id = request.data.get('category')
        currency = request.data.get('currency')
        description = request.data.get('description')
        date = request.data.get('date') or timezone.now().date()

        if not all([amount, category_id, currency]):
            return Response({"error": "Barcha maydonlar to'ldirilishi kerak."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = IncomeCategory.objects.get(id=category_id)
        except IncomeCategory.DoesNotExist:
            return Response({"error": "Kategoriya topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        income = Income.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            currency=currency,
            description=description,
            date=date
        )

        return Response({"message": "Income muvaffaqiyatli qo‘shildi.", "income_id": income.id}, status=status.HTTP_201_CREATED)


class AddExpenseCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Yangi expense kategoriyasi qo‘shish",
        request_body=ExpenseCategorySerializer,
        responses={
            201: openapi.Response(description="Kategoriya qo‘shildi"),
            400: openapi.Response(description="Xatolik: noto‘g‘ri ma'lumot")
        }
    )
    def post(self, request):
        serializer = ExpenseCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Expense Category successfully created.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Failed to create Expense Category.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class AddExpenseView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Yangi expense qo‘shish",
        request_body=ExpenseSerializer,
        responses={
            201: openapi.Response(description="Expense qo‘shildi"),
            400: openapi.Response(description="Xatolik: validatsiya xatolari")
        }
    )
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Expense successfully added.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Failed to add Expense.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)