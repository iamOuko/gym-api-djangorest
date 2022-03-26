from rest_framework import routers
from gym import views


router = routers.DefaultRouter()
router.register('customusers', views.CustomUserViewset, basename='customusers')
router.register('profiles', views.UserProfileViewset, basename='profiles')
router.register('healthrecords', views.HealthRecordViewset, basename='healthrecords')
router.register('goals', views.UserGoalViewset, basename='goals')