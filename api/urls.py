from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import WxworkTag
#from api.extrattr import UpdateAttrViewSet
from . import extrattr

router = DefaultRouter()  # 创建路由器(路由器只能结束视图集一起使用)
router.register(r'wx', extrattr.MyExcelView,basename='common')  # 注册路由


urlpatterns = [
    path('', include(router.urls)),
]

'''
router = DefaultRouter()
router.register(r'tag', WxworkTag, basename='/')
router.register(r'/user/update/', WxworkTag, basename='/')

urlpatterns = [
    path('', include(router.urls)),
]
'''

