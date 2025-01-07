from django.urls import path, include
from django.contrib import admin

from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls.static import static
from django.conf import settings

from app.api.v1.v1_router import router as v1_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(v1_router.urls), name="v1"),
]

urlpatterns += [
    path("api/v1/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += [
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
