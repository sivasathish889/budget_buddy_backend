from rest_framework.serializers import ModelSerializer
from budget_buddy_app.models import *
from rest_framework import serializers
class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'



class CategorySerializer(ModelSerializer):
    # categorys = ExpenseSerialzier(many=True, read_only=True)
    class Meta:
        model = Catagory
        fields = '__all__'
        
        
class ExpenseSerialzier(ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Catagory.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Expense
        fields = '__all__'
        
class SocialSerializer(ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'
        
        
class TopExpenseSerializer(ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Expense
        fields = ['id', 'total_amount', 'category']



class DateOnlyField(serializers.ReadOnlyField):
    def to_representation(self, value):
        if hasattr(value, 'date'):
            return value.date()
        return value

class ExpenseCategorySummarySerializer(serializers.Serializer):
    category__id = serializers.IntegerField()
    category__name = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    latest_expense_id = serializers.IntegerField()
    latest_expense_date = DateOnlyField()