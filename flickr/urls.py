from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'photos', PhotoViewset)
router.register(r'groups', PhotoGroupViewset)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include('rest_auth.urls'))
]
