from django.urls import path, include
from .views import UserViewSet, MyTokenObtainPairView, UserFromTokenView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", MyTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/user-info/", UserFromTokenView.as_view(), name="token_info"),
]
