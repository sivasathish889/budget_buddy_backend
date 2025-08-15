from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users
from .serializer import *
from rest_framework.serializers import ValidationError
from rest_framework import status
from .helpers.bcrypt import hash_password,check_password
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
        if name == "" or email == "" or phone == "" or DOB == "":
            return Response({"message":"All fields are required", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(email=email).exists():
            return Response({"message":"Email already exists", "success" : False},status=status.HTTP_400_BAD_REQUEST)
        hashing_password = hash_password(request.data["password"])
        user = UserSerializer(data={"name":name,"email":email,"phone":phone,"DOB":
                                    DOB, "password":hashing_password})
        if user.is_valid():
            user.save()
            return Response({"message":"User Created Successfully", "success":True},status=status.HTTP_200_OK)
        else:
            raise ValidationError("Fields Not Valid")
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
        user = UserSerializer(user)
        return Response({"message":"Login Successfully", "success" : True},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message":"Something went wrong", "success" : False},status=status.HTTP_400_BAD_REQUEST)
    
