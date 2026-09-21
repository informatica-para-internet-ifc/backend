from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from core.views import (
    AnoViewSet,
    ArquivoViewSet,
    AtividadeViewSet,
    BlocoViewSet,
    BuscaView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    DisciplinaViewSet,
    UserRegistrationView,
    UserViewSet,
)

from uploader.router import router as uploader_router
from uploader.views import serve_stored_file

router = DefaultRouter()

router.register(r'usuarios', UserViewSet, basename='usuarios')
router.register(r'anos', AnoViewSet, basename='anos')
router.register(r'disciplinas', DisciplinaViewSet, basename='disciplinas')
router.register(r'atividades', AtividadeViewSet, basename='atividades')
router.register(r'blocos', BlocoViewSet, basename='blocos')
router.register(r'arquivos', ArquivoViewSet, basename='arquivos')

urlpatterns = [
    path('admin/', admin.site.urls),
    # OpenAPI 3
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/doc/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
    # Autenticação JWT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    # Registro de usuários
    path('api/registro/', UserRegistrationView.as_view(), name='user_registration'),
    # Busca
    path('api/busca/', BuscaView.as_view(), name='busca'),
    # API
    path('api/', include(router.urls)),
    path('api/media/', include(uploader_router.urls)),
    # Arquivos enviados, guardados no banco de dados
    path('media/<path:path>', serve_stored_file, name='media'),
]
