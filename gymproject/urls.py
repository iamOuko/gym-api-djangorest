from django.contrib import admin
from django.urls import path, include
from .router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include((router.urls, 'customusers'))),
    path('', include((router.urls, 'profiles'))),
    path('', include((router.urls, 'healthrecords'))),
    path('', include((router.urls, 'goals'))),
    
]