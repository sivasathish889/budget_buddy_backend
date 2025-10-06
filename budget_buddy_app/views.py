from rest_framework.response import Response
from django.db.models import Sum,Max
from rest_framework.decorators import api_view
from .models import *
from .serializer import *
from rest_framework import status
from .utils.bcrypt import hash_password,check_password
from .utils.jwt import encode_jwt
import datetime
from django.core.mail import send_mail
import math
from django.conf import settings
import random
import datetime
@api_view(["GET"])
def home(request):
    return Response({"age" : "hello world"})

@api_view(["GET"])
def register_verify(request):
    email = request.GET.get('email')
    try:
        if Users.objects.filter(email=email).exists():
            return Response({"message":"Email already exists", "success" : False}, status=status.HTTP_400_BAD_REQUEST)
        otp = math.floor(random.randint(1000,9999))
        send_mail(
        subject='Regsiter Otp verify',
        message = f"Your OTP is {otp}",
        from_email='rdxsathish96@gmail.com',
        recipient_list=[email],
        fail_silently=False,
        )
        return Response({"message":"Email is available", "success" : True,"otp" :str(otp)}, status=status.HTTP_200_OK)
    except Exception as e:
        print("error",e)
        return Response({"message":"Something went wrong", "success" : False}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])   
def register(request):
    try:
        name = request.data["name"]
        email = request.data["email"]
        phone = request.data["phone"]
        DOB = request.data["DOB"]
        password = request.data['password']
        hashed_password = hash_password(password)
        format_date = datetime.datetime.strptime(DOB, '%m/%d/%Y').date()
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
def get_user(request):
    if request.current_user is None:
        return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        if not Users.objects.filter(id=user_id).exists():
            return Response({"message":"User Not Found", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        user = Users.objects.get(id=user_id)
        user = UserSerializer(user)
        return Response({"message":"User Fetched Successfully", "data": user.data, "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    


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
        expense = ExpenseSerialzier(data={"amount": amount, "description": memo, "category_id": int(category), "user": int(user_id)})
        if not expense.is_valid():
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
        return Response({ "success" : False},status=status.HTTP_200_OK)
    user_id = request.current_user.get('id')
    try:
        today = datetime.datetime.now()
        two_months_ago = today - datetime.timedelta(days=60)
        expense = Expense.objects.filter(user=user_id, date__gte=two_months_ago.astimezone(),
            date__lte=today.astimezone()).order_by('-date')
        expenseList = ExpenseSerialzier(expense, many=True).data
        return Response({"message"  : "Fetched SuccessFully", "data" : (expenseList), "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT"])
def update_profile(request):
    if request.current_user is None:
        return Response({"message": "User Not Found", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        user = Users.objects.get(id=user_id)
        name = request.data.get('name', user.name)
        phone = request.data.get('phone', user.phone)
        email = request.data.get('email', user.email)
        goal = request.data.get('goal', user.goal)
        if(goal > 100):
            user.goal = goal
        user.name = name
        user.phone = phone
        user.email = email
        user.save()
        return Response({"message": "Profile Updated Successfully", "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["PUT"])
def change_password(request):
    if request.current_user is None:
        return Response({"message": "User Not Found", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        user = Users.objects.get(id=user_id)
        currentPassword = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        if not check_password(currentPassword, user.password):
            return Response({"message": "Invalid Old Password", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        hashed_password = hash_password(new_password)
        user.password = hashed_password
        user.save()
        return Response({"message": "Password Changed Successfully", "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def send_otp(request):
    email = request.GET.get('email')
    if not Users.objects.filter(email=email).exists():
        print("hrer")
        return Response({"message": "Email Not Found", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
    otp = math.floor(random.randint(1000, 9999))
    try:
        send_mail(
            subject='OTP Verification',
            message=f"Your OTP is {otp}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "OTP Sent Successfully", "success": True, "otp": str(otp)}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
def verifyPassword(request,password):
    if request.current_user is None:
        return Response({"message": "User Not Found", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        if not Users.objects.filter(id = user_id).exists():
            return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
        user = Users.objects.get(id = user_id)
        if not check_password(password,user.password):
            return Response({"message":"Invalid Password", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Password Verified Successfully", "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["DELETE"])
def delete_account(request):
    if request.current_user is None:
        return Response({"message": "User Not Found", "success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        if not Users.objects.filter(id = user_id).exists():
            return Response({"message":"User Not Found", "success" : False},status=status.HTTP_401_UNAUTHORIZED)
        user = Users.objects.get(id = user_id)
        user.delete()
        return Response({"message":"Account Deleted Successfully", "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_expense(request, id):
    try:
        expense = Expense.objects.get(id = id)
        expense.delete()
        return Response({"message":"Expense Deleted Successfully", "success" : True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False}, status=status.HTTP_400_BAD_REQUEST)