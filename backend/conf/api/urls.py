from django.urls import path, include
from rest_framework.routers import DefaultRouter
from eggs.api.urls import egg_router  # Adjust the import path if necessary
from eggs.api.views import MyTokenObtainPairView, RegisterView, getRoutes  # Adjust the import path if necessary

from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
# Extend the router with the egg_router's registry
router.registry.extend(egg_router.registry)

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('routes/', getRoutes, name='get_routes'),
    path('', include(router.urls)),
]
