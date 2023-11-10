from rest_framework.routers import DefaultRouter
from eggs.api.urls import egg_router
from django.urls import path, include

router = DefaultRouter()
#posts
router.registry.extend(egg_router.registry)

urlpatterns = [
    path('', include(router.urls))
]