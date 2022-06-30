#from django.contrib import admin
from django.urls import path, include
#from modules import guestready_front

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('reports/', HttpResponse("Hello."))
    #path('', include('guestready.urls', namespace='reports')),
    # path('', include('modules.guestready_front.urls', namespace='reports'))
path('', include('modules.front_django.urls', namespace='front')),
]
