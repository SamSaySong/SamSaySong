from django.urls import path, include
from rest_framework import routers
from . import views
from django.conf.urls import url


router = routers.DefaultRouter()
router.register(r'claim', views.ClaimViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('detail', views.OCR_VINA, name='detail')
]
