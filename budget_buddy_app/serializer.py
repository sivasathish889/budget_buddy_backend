from rest_framework.serializers import ModelSerializer
from budget_buddy_app.models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ExpenseSerialzier(ModelSerializer):
    class Meta:
         model = Expense
         fields = '__all__'

class CategorySerializer(ModelSerializer):
    categorys = ExpenseSerialzier(many=True, read_only=True)
    class Meta:
        model = Catagory
        fields = '__all__'