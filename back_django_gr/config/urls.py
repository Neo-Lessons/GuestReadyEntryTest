#from django.contrib import admin
from django.urls import path, include
#from modules import guestready_front

urlpatterns = [
    path('', include('modules.front_django.urls', namespace='front')),
    # NEO: 03.07.22 00:58 (~003) [APPEND API]
    # <NEW>
    path('api/v1/', include('modules.api_v1.urls', namespace='api')),
    # </NEW> </CHANGE>
]
