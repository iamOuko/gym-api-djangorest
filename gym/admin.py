from tokenize import Token
from django.contrib import admin
from .models import UserProfile, CustomUser, HealthRecord, UserGoal, TokenModel

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'custom_user')


admin.site.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')

admin.site.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'weight', 'height', 'BMI', 'underlying_conditions')

admin.site.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ('new_weight', 'size')

admin.site.register(TokenModel)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('key')