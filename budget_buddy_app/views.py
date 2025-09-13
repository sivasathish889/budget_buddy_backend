from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from rest_framework import status
from .utils.bcrypt import hash_password,check_password
from .utils.jwt import encode_jwt
import datetime
from django.core.mail import send_mail
import math

import random
@api_view(["GET"])
def home(request):
    return Response({"age" : "hello world"})

    
@api_view(["POST"])   
def register(request):
    try:
        name = request.data["name"]
        email = request.data["email"]
        phone = request.data["phone"]
        DOB = request.data["DOB"]
        password = request.data['password']
        hashed_password = hash_password(password)
        format_date = datetime.datetime.strptime(DOB, '%d/%m/%Y').date()
        if name == "" or email == "" or phone == "" or DOB == "":
            return Response({"message":"All fields are required", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(email=email).exists():
            return Response({"message":"Email already exists", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        user = UserSerializer(data={"name":name,"email":email,"phone":phone, "DOB":format_date,'password' : hashed_password})
        if not user.is_valid():
            return Response({"message": dict(user.errors), "success": False}, status=status.HTTP_200_OK)
        user.save()
        return Response({"message": "User Created Successfully", "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_user(_,pk):
    try:
        if not Users.objects.filter(id=pk).exists():
            return Response({"message":"User Not Found", "success" : False},status=400)
        user = Users.objects.get(id=pk)
        user = UserSerializer(user)
        return Response(user.data,status=200)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=400)
    


@api_view(["GET"])
def login(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    try:
        if not Users.objects.filter(email=email).exists():
            return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
        user = Users.objects.get(email=email)
        if not check_password(password,user.password):
            return Response({"message":"Invalid Password", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        user = UserSerializer(user).data
        jwt_token = encode_jwt(user)
        return Response({"message":"Login Successfully", "Token": jwt_token, "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def social_login(request):
    print(request)
    return Response({"message":"Login Successfully", "success" : True},status=status.HTTP_200_OK)  

@api_view(["GET"])
def forget_password(request, email):
    if not Users.objects.filter(email=email).exists():
        return Response({"message":"Email Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
    otp = math.floor(random.randint(1000,9999))
    try:
        send_mail(
        subject='Forget Password',
        message = f"Your OTP is {otp}",
        from_email='rdxsathish96@gmail.com',
        recipient_list=[email],
        fail_silently=False,
        )
        return Response({"message":"OTP Sent Successfully", "OTP": str(otp), "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message" : "error"})

@api_view(["POST"])
def reset_password(request):
    password = request.data["newPassword"]
    email = request.data["email"]
    try:
        if not Users.objects.filter(email=email).exists():
            return Response({"message":"Email Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
        user = Users.objects.get(email=email)
        hashed_password = hash_password(password)
        user.password = hashed_password
        user.save()
        return Response({"message":"Password Reset Successfully", "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def add_expense(request):
    category = request.data['category']
    amount = request.data['amount']
    memo = request.data['memo']
    user_id = request.current_user.get('id')
    try:
        if(category=="" or amount=="" or memo==""):
            return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        expense = ExpenseSerialzier(data={"amount":amount, "description" : memo, "category" : int(category), "user" : int(user_id) })
        if not expense.is_valid():
            print(expense.errors)
            return Response({"message" : dict(expense.errors), "success" : False}, status=status.HTTP_400_BAD_REQUEST)
        expense.save()
        return Response({"message" : "Added SuccessFully", "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(["GET"])
def get_category(request):
    try:
        category = Catagory.objects.all()
        categoryList = CategorySerializer(category, many=True).data
        return Response({"message"  : "Fetched SuccessFully", "data" : (categoryList), "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_recentUse_byId(request):
    if request.current_user is None:
        return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        expense = Expense.objects.filter(user=user_id).order_by('-date')
        expenseList = ExpenseSerialzier(expense, many=True).data
        return Response({"message"  : "Fetched SuccessFully", "data" : (expenseList), "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def get_all_expense(request):
    if request.current_user is None:
        return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        expense = Expense.objects.filter(user=user_id)
        expenseList = ExpenseSerialzier(expense, many=True).data
        return Response({"message"  : "Fetched SuccessFully", "data" : (expenseList), "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)