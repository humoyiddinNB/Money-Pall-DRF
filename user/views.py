from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser, EmailOTP
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer, RegisterSerializer, OTPVerifySerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
import random
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import login
from drf_yasg import openapi


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Foydalanuvchilar ro'yxati",
        responses={200: CustomUserSerializer(many=True)}
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Bitta foydalanuvchi haqida ma'lumot",
        responses={200: CustomUserSerializer()}
    )
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterView(APIView):

    @swagger_auto_schema(
        operation_summary="Registratsiya qilish",
        request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'msg': 'Muvaffaqiyatli ro‘yxatdan o‘tish',
                'token': token.key,
                'status': status.HTTP_201_CREATED
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @swagger_auto_schema(
        operation_summary="Email orqali OTP yuborish",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="OTP yuborildi"),
            404: openapi.Response(description="Email topilmadi"),
            400: openapi.Response(description="Email kiritilmagan")
        }
    )
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({
                "error": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not CustomUser.objects.filter(email=email).exists():
            return Response({
                "error": "Email not found."
            }, status=status.HTTP_404_NOT_FOUND)

        code = str(random.randint(100000, 999999))
        EmailOTP.objects.create(email=email, code=code)

        send_mail(
            subject="MoneyPall ga kirish uchun shundan foydalaning",
            message=f"Hi, your OTP is: {code}. It will expire in 5 minutes.",
            from_email="noreply@moneypall.uz",
            recipient_list=[email]
        )

        return Response({
            "message": "OTP sent to your email."
        }, status=status.HTTP_200_OK)


class OTPVerifyAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="OTP tekshirish",
        request_body=OTPVerifySerializer,
        responses={200: openapi.Response(description="Muvoffaqiyatli", examples={
            "application/json": {
                "detail": "Hush kelibsiz bro!",
                "token": "abc123token",
                "status": 200
            }
        })}
    )
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            otp = EmailOTP.objects.filter(email=email, code=code).first()
            if not otp:
                return Response({"detail": "OTP xato yoki yaroqsiz.", 'status': status.HTTP_400_BAD_REQUEST})

            if otp.is_expired:
                return Response({"detail": "OTP vaqti tugagan.", 'status': status.HTTP_400_BAD_REQUEST})

            if otp.is_confirmed:
                return Response({"detail": "OTP oldin foydalanilgan.", 'status': status.HTTP_400_BAD_REQUEST})

            otp.is_confirmed = True
            otp.save()

            user = CustomUser.objects.filter(email=email).first()
            if not user:
                return Response({"detail": "Foydalanuvchi topilmadi.", 'status': status.HTTP_404_NOT_FOUND})

            login(request, user)


            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "detail": "Hush kelibsiz bro!",
                "token": token.key,
                'status': status.HTTP_200_OK
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Foydalanuvchini tizimdan chiqarish (Log out)",
        responses={
            200: openapi.Response(description="Muvaffaqiyatli chiqdi"),
            401: openapi.Response(description="Avtorizatsiya talab qilinadi")
        }
    )
    def post(self, request):
        token = Token.objects.filter(user=request.user).first()
        if token:
            token.delete()
        return Response({
            "data": "Kozimga Korinmang"
        }, status=status.HTTP_200_OK)


class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Profilni ko‘rish",
        responses={200: CustomUserSerializer()}
    )
    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response({
            'data': serializer.data,
            'status': status.HTTP_200_OK
        })

    @swagger_auto_schema(
        operation_summary="Profilni yangilash",
        request_body=CustomUserSerializer,
        responses={
            200: openapi.Response(description="Profil muvaffaqiyatli yangilandi", schema=CustomUserSerializer()),
            400: "Xato ma'lumot"
        }
    )
    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Profil yangilandi",
                'status': status.HTTP_200_OK
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Akkauntni o‘chirish",
        responses={
            204: openapi.Response(description="Akkaunt o‘chirildi"),
            401: "Token mavjud emas yoki noto‘g‘ri"
        }
    )
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            "detail": "Akkaunt o‘chirildi.",
            'status': status.HTTP_204_NO_CONTENT
        })