from urllib import response
from gym.serializers import CustomUserSerializer, UpdateUserProfileSerializer,CreateUpdateHealthRecordSerializer, UserProfileSerializer,HealthRecordSerializer, UserGoalSerializer, UpdateUserGoalSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from gym.models import CustomUser, UserProfile, HealthRecord, UserGoal
from .calculator import bmi
from rest_framework.decorators import action
from gym.login import LoginController

from django.contrib.auth import authenticate
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token


class CustomUserViewset(viewsets.ViewSet):
 
    def list(self, request):
        # get all objects from db
        queryset = CustomUser.objects.all()

        # pass through serializer
        serialized_data = CustomUserSerializer(queryset, many=True)

        # return data / response
        if not serialized_data.data:
            return Response(
                {'detail': [], 'code':404},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'detail': serialized_data.data, 'code':200},
            status=status.HTTP_200_OK
        )
        
    def create(self, request):
        # get data from request payload
        # pass through serializer
        serialized_data = CustomUserSerializer(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                {'detail': serialized_data.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )

        # store data in database
        serialized_data.save()

        # return response
        return Response(
            {'detail': 'User created succesfully', 'code': 200},
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        try:
            queryset = CustomUser.objects.get(pk=pk)
            serialized_data = CustomUserSerializer(queryset)
            return Response(
                    {'details':serialized_data.data, 'code':200},
                    status=status.HTTP_200_OK
                )

        except CustomUser.DoesNotExist:
            return Response(
                {'details':'User Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        serialized_data = CustomUserSerializer(data=request.data)
        if not serialized_data.is_valid():
                return Response(
                    {'details':serialized_data.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        custom_user = CustomUser.objects.filter(pk=pk)
            
        if custom_user:
                custom_user.update(**serialized_data.data)
                return Response(
                    {'details':'User succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
        return Response(
                {'details':'User to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )



    def delete(self, request, pk=None):
        CustomUser.objects.filter(pk=pk).delete()
        return Response(
            {'details':'Succesfully deleted user.', 'code':200},
            status=status.HTTP_200_OK
        )
    @action(methods=['POST'], detail=False, permission_classes=[])
    def login(self, request):
        """login a user"""
        login_user = LoginController()
        return login_user.login(request)
        
    


class UserProfileViewset(viewsets.ViewSet):
    
    def list(self, request):
        
        queryset = UserProfile.objects.all()
        serialized_data = UserProfileSerializer(queryset, many=True)
        if not serialized_data.data:
            return Response(
                {'detail': [], 'code':404},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'detail': serialized_data.data, 'code':200},
            status=status.HTTP_200_OK
        )
        
    def create(self, request):
        serialized_data = UserProfileSerializer(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                {'detail': serialized_data.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )

        custom_user = serialized_data.validated_data.get('custom_user')

        # does the user exist
        try:
            
            custom_user = CustomUser.objects.get(id=custom_user.id)

            # does the user have a profile already
            if UserProfile.objects.filter(custom_user=custom_user).exists():
                return Response(
                    {'detail': 'The user already has a profile', 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except CustomUser.DoesNotExist:
            return Response(
                {'detail': 'The user provided does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serialized_data.save()

        return Response(
            {'detail': 'UserProfile created succesfully', 'code': 200},
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        try:
            queryset = UserProfile.objects.get(pk=pk)
            serialized_data = UserProfileSerializer(queryset)
            return Response(
                    {'details':serialized_data.data, 'code':200},
                    status=status.HTTP_200_OK
                )

        except UserProfile.DoesNotExist:
            return Response(
                {'details':'UserProfile Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        
        serialized_data = UpdateUserProfileSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(
                {'details':serialized_data.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
                
        user_profile = UserProfile.objects.filter(pk=pk)
        
        if user_profile:
                user_profile.update(**serialized_data.validated_data)
                return Response(
                    {'details':'User Profile succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
        return Response(
                {'details':'User Profile to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )



    def delete(self, request, pk=None):
        UserProfile.objects.filter(pk=pk).delete()
        return Response(
            {'details':'Succesfully deleted User Profile.', 'code':200},
            status=status.HTTP_200_OK
        )


class HealthRecordViewset(viewsets.ViewSet):
    def list(self, request):

        queryset = HealthRecord.objects.all()
        serialized_data = HealthRecordSerializer(queryset, many=True)
        if not serialized_data.data:
            return Response(
                {'detail': [], 'code':404},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'detail': serialized_data.data, 'code':200},
            status=status.HTTP_200_OK
        )


    def create(self, request):
        # serialize init data
        serialized_data = CreateUpdateHealthRecordSerializer(data=request.data)

        # Check if serialized data is valid
        if not serialized_data.is_valid():
            return Response(
                {'detail': serialized_data.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_profile_id = serialized_data.validated_data.get('user_profile_id')

        # does the user_profile exist
        try:
            user_profile = UserProfile.objects.get(id=user_profile_id)

            # does the user_profile have a health record already
            if HealthRecord.objects.filter(user_profile=user_profile).exists():
                return Response(
                    {'detail': 'The user_profile already has a health record', 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except UserProfile.DoesNotExist:
            return Response(
                {'detail': 'The user_profile provided does not exist', 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )

        # calculate bmi
        # extract weight
        weight = serialized_data.validated_data.get('weight')

        # extract height
        height = serialized_data.validated_data.get('height')

        # call bmi funtion 
        # store bmi value
        user_bmi = bmi(weight, height)

        # create data object to be added to db
        health_records = {
            "underlying_conditions": serialized_data.validated_data.get('underlying_conditions'),
            "weight": weight,
            "height": height, 
            "bmi": user_bmi,  
            "user_profile" : user_profile
        }

        health_record = HealthRecord(**health_records)
        health_record.save()
        
        return Response(
            {'detail': 'Record created succesfully', 'code': 200},
            status=status.HTTP_201_CREATED
        )
    
    def retrieve(self, request, pk=None):
        try:
            queryset = HealthRecord.objects.get(pk=pk)
            serialized_data = HealthRecordSerializer(queryset)
            return Response(
                    {'details':serialized_data.data, 'code':200},
                    status=status.HTTP_200_OK
                )

        except HealthRecord.DoesNotExist:
            return Response(
                {'details':'Health record Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        
        serialized_data = CreateUpdateHealthRecordSerializer(data=request.data)
        if not serialized_data.is_valid():
            return Response(
                {'details':serialized_data.errors, 'code': 400},
                status=status.HTTP_400_BAD_REQUEST
            )
                
        healthrecord = HealthRecord.objects.filter(pk=pk)
        
        if healthrecord:
                healthrecord.update(**serialized_data.validated_data)
                return Response(
                    {'details':'Health record succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
        return Response(
                {'details':'Health record to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )



    def delete(self, request, pk=None):
        HealthRecord.objects.filter(pk=pk).delete()
        return Response(
            {'details':'Succesfully deleted health record.', 'code':200},
            status=status.HTTP_200_OK
        )



class UserGoalViewset(viewsets.ViewSet):
    def list(self, request):

        queryset = UserGoal.objects.all()
        serialized_data = UserGoalSerializer(queryset, many=True)
        if not serialized_data.data:
            return Response(
                {'detail': [], 'code':404},
                status=status.HTTP_200_OK
            )
        
        return Response(
            {'detail': serialized_data.data, 'code':200},
            status=status.HTTP_200_OK
        )

    
    def create(self, request):
        serialized_data = UserGoalSerializer(data=request.data)

        if not serialized_data.is_valid():
            return Response(
                {'detail': serialized_data.errors, 'code':400},
                status=status.HTTP_400_BAD_REQUEST
            )

        serialized_data.save()

        return Response(
            {'detail': 'Goal created succesfully', 'code': 200},
            status=status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk=None):
        try:
            queryset = UserGoal.objects.get(pk=pk)
            serialized_data = UserGoalSerializer(queryset)
            return Response(
                    {'details':serialized_data.data, 'code':200},
                    status=status.HTTP_200_OK
                )

        except UserGoal.DoesNotExist:
            return Response(
                {'details':'Goal Does Not Exist', 'code': 400},
                status=status.HTTP_200_OK
            )

    def update(self, request, pk=None):
        serialized_data = UpdateUserGoalSerializer(data=request.data)
        if not serialized_data.is_valid():
                return Response(
                    {'details':serialized_data.errors, 'code': 400},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        user_goal = UserGoal.objects.filter(pk=pk)
            
        if user_goal:
                user_goal.update(**serialized_data.data)
                return Response(
                    {'details':'Goal succesfully updated', 'code':200},
                    status=status.HTTP_200_OK
                )
        return Response(
                {'details':'Goal to be updated does not exist', 'code':400},
                status=status.HTTP_200_OK
            )



    def delete(self, request, pk=None):
        UserGoal.objects.filter(pk=pk).delete()
        return Response(
            {'details':'Succesfully deleted goal.', 'code':200},
            status=status.HTTP_200_OK
        )