from rest_framework import serializers
from gym.models import CustomUser, UserProfile, HealthRecord, UserGoal


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'first_name', 'last_name', 'picture', 'date_of_birth', 'gender', 'custom_user']

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'picture', 'date_of_birth', 'gender']

class HealthRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecord
        fields = ['id', 'weight', 'height', 'bmi', 'underlying_conditions']

class CreateUpdateHealthRecordSerializer(serializers.Serializer):
    weight = serializers.DecimalField(max_digits=10, decimal_places=2)
    height = serializers.DecimalField(max_digits=10, decimal_places=2)
    underlying_conditions = serializers.CharField()
    trainee_id = serializers.IntegerField()

class UserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['id', 'new_weight', 'size', 'custom_user']

class UpdateUserGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGoal
        fields = ['new_weight', 'size']