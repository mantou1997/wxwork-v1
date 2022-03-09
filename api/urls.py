from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import WxworkTag

router = DefaultRouter()
router.register(r'tag', WxworkTag, basename='/')

urlpatterns = [
    path('', include(router.urls)),
]
