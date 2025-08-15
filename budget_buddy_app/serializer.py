from rest_framework.serializers import ModelSerializer

from budget_buddy_app.models import Users

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'