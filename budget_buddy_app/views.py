from rest_framework.response import Response
from django.db.models import Sum,Max
from rest_framework.decorators import api_view
from django.db.models.functions import TruncDay, TruncMonth
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
def register_verify(request, email):
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
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        offset = (page - 1) * limit
        
        # 1. Recent Expenses (Last 60 days)
        two_months_ago = today - datetime.timedelta(days=60)
        expense_query = Expense.objects.filter(user=user_id, date__gte=two_months_ago.astimezone(),
            date__lte=today.astimezone()).order_by('-date')
        
        total_expenses = expense_query.count()
        expense = expense_query[offset:offset+limit]
        expenseList = ExpenseSerialzier(expense, many=True).data
        has_more = (offset + limit) < total_expenses

        # 2. Monthly Total
        start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_total = Expense.objects.filter(user=user_id, date__gte=start_of_month.astimezone()).aggregate(Sum('amount'))['amount__sum'] or 0

        # 3. Weekly Total
        start_of_week = today - datetime.timedelta(days=7)
        weekly_total = Expense.objects.filter(user=user_id, date__gte=start_of_week.astimezone()).aggregate(Sum('amount'))['amount__sum'] or 0

        # 4. Category Stats (For Pie Chart - Current Month)
        category_stats = Expense.objects.filter(user=user_id, date__gte=start_of_month.astimezone()) \
            .values('category__name', 'category__id') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')
        
        # Calculate percentages
        category_data = []
        for stat in category_stats:
            percentage = (stat['total'] / monthly_total * 100) if monthly_total > 0 else 0
            category_data.append({
                "category": stat['category__name'],
                "id": stat['category__id'],
                "amount": stat['total'],
                "percentage": round(percentage, 1)
            })

        return Response({
            "message": "Fetched SuccessFully",
            "data": {
                "expenses": expenseList,
                "has_more": has_more,
                "monthly_total": monthly_total,
                "weekly_total": weekly_total,
                "category_stats": category_data
            },
            "success": True
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_filtered_stats(request):
    if request.current_user is None:
        return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    period = request.GET.get('period', 'monthly') # day, weekly, monthly
    
    today = datetime.datetime.now()
    if period == 'day':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == 'weekly':
        start_date = today - datetime.timedelta(days=7)
    else: # monthly
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    try:
        stats = Expense.objects.filter(user=user_id, date__gte=start_date.astimezone()) \
            .values('category__name', 'category__id') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')
        
        total_amount = sum(item['total'] for item in stats)
        
        data = []
        for item in stats:
            percentage = (item['total'] / total_amount * 100) if total_amount > 0 else 0
            data.append({
                "category": item['category__name'],
                "id": item['category__id'],
                "amount": item['total'],
                "percentage": round(percentage, 1)
            })
            
        return Response({"data": data, "total": total_amount, "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)
    

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

@api_view(["GET"])
def get_spending_graph(request):
    if request.current_user is None:
        return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=6)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        stats = Expense.objects.filter(user=user_id, date__gte=start_date.astimezone()) \
            .annotate(day=TruncDay('date')) \
            .values('day') \
            .annotate(total=Sum('amount')) \
            .order_by('day')
            
        stats_dict = {stat['day'].astimezone().strftime('%Y-%m-%d'): stat['total'] for stat in stats}
        
        days_names = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"]
        graph_data = []
        total_amount = 0
        
        for i in range(7):
            current_day = start_date + datetime.timedelta(days=i)
            day_str = current_day.strftime('%Y-%m-%d')
            amount = stats_dict.get(day_str, 0)
            js_day_index = (current_day.weekday() + 1) % 7
            
            total_amount += amount
            graph_data.append({
                "label": days_names[js_day_index],
                "value": amount
            })
            
        return Response({"data": graph_data, "total": total_amount, "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_monthly_summary(request):
    if request.current_user is None:
        return Response({"success": False}, status=status.HTTP_401_UNAUTHORIZED)
    user_id = request.current_user.get('id')
    try:
        # Group expenses by month and then by category
        monthly_stats = Expense.objects.filter(user=user_id) \
            .annotate(month=TruncMonth('date')) \
            .values('month', 'category__name', 'category__id') \
            .annotate(total=Sum('amount')) \
            .order_by('-month', '-total')

        # Format into a nested structure
        summary_dict = {}
        for stat in monthly_stats:
            month_str = stat['month'].astimezone().strftime('%B %Y')
            
            if month_str not in summary_dict:
                summary_dict[month_str] = {
                    "month": month_str,
                    "total": 0,
                    "categories": []
                }
            
            summary_dict[month_str]["total"] += stat['total']
            summary_dict[month_str]["categories"].append({
                "category": stat['category__name'],
                "id": stat['category__id'],
                "amount": stat['total']
            })

        # Convert to list and sort by month (it's already sorted by -month from DB, dict preserves order in Python 3.7+)
        data = list(summary_dict.values())
        
        return Response({"data": data, "success": True}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Something went wrong", "success": False}, status=status.HTTP_400_BAD_REQUEST)