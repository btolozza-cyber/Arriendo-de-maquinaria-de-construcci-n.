from rest_framework.routers import DefaultRouter

from .views import (
    MaquinariaViewSet,
    CarroArriendoViewSet,
    ItemCarroViewSet,
    ContratoArriendoViewSet,
)

router = DefaultRouter()

router.register(
    r"maquinarias",
    MaquinariaViewSet,
    basename="maquinaria"
)

router.register(
    r"carros",
    CarroArriendoViewSet,
    basename="carro"
)

router.register(
    r"items-carro",
    ItemCarroViewSet,
    basename="item-carro"
)

router.register(
    r"contratos",
    ContratoArriendoViewSet,
    basename="contrato"
)

urlpatterns = router.urls