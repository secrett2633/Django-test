from rest_framework.routers import DefaultRouter

from app.api.v1.endpoints.test import TestSet

router = DefaultRouter(trailing_slash=False)
router.register("v1", TestSet, basename="test")
