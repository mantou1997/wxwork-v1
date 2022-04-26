from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import WxworkTag
from api.extrattr import UpdateAttrViewSet

router = DefaultRouter()
router.register(r'tag', WxworkTag, basename='/')
router.register(r'/user/update/', WxworkTag, basename='/')

urlpatterns = [
    path('', include(router.urls)),
]
