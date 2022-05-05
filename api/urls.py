from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import extattr


router = DefaultRouter()  # 创建路由器(路由器只能结束视图集一起使用)
router.register(r'wx', extattr.UpdateExtattrViewSet,basename='common')  # 注册路由


urlpatterns = [
    path('', include(router.urls)),
]



