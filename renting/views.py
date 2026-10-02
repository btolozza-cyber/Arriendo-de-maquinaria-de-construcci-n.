from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    CarroArriendo,
    ItemCarro,
    Maquinaria,
    ContratoArriendo,
    ItemContrato,
)

from .permissions import (
    IsEjecutivo,
    IsEmpresa,
    IsEjecutivoOrEmpresaReadOnly,
)

from .serializers import (
    CustomTokenObtainPairSerializer,
    MaquinariaSerializer,
    CarroArriendoSerializer,
    ItemCarroSerializer,
    ItemContratoSerializer,
    ContratoArriendoSerializer,
)

from django.shortcuts import render
from django.db import transaction

class CustomTokenObtainPairView(TokenObtainPairView):
    # Se ajusta la vista para utilizar el serializer personalizado (Con los roles)

    serializer_class = CustomTokenObtainPairSerializer

class MaquinariaViewSet(viewsets.ModelViewSet):
    # Permite realizar operaciones CRUD sobre las maquinarias

    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
    permission_classes = [IsEjecutivoOrEmpresaReadOnly]
    filterset_fields = ["categoria", "nombre"]

class CarroArriendoViewSet(viewsets.ModelViewSet):
    serializer_class = CarroArriendoSerializer
    permission_classes = [IsEmpresa]

    def get_queryset(self):
        # Cada empresa solo puede acceder a su propio carro.
        return CarroArriendo.objects.filter(
            usuario=self.request.user
        )

    def perform_create(self, serializer):
        # El usuario autenticado queda asociado automáticamente al carro.
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):

        carro = self.get_object()
        items = carro.items.select_related("maquinaria").all()

        if not items.exists():
            return Response(
                {"error": "El carro está vacío."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Todas las operaciones posteriores forman una única transacción.
        with transaction.atomic():

            # Validamos disponibilidad de cada maquinaria.
            for item in items:

                maquinaria = item.maquinaria

                # Buscamos contratos que tengan un período que se
                # superponga con el período solicitado.
                items_ocupados = ItemContrato.objects.filter(
                    maquinaria=maquinaria,
                    fecha_inicio__lt=item.fecha_fin,
                    fecha_fin__gt=item.fecha_inicio,
                    contrato__estado__in=[
                        ContratoArriendo.Estado.PAGADO,
                        ContratoArriendo.Estado.ENTREGADO,
                    ]
                )

                cantidad_ocupada = sum(
                    ocupado.cantidad
                    for ocupado in items_ocupados
                )

                cantidad_disponible = (
                    maquinaria.stock_total - cantidad_ocupada
                )

                if item.cantidad > cantidad_disponible:

                    raise serializers.ValidationError(
                        {
                            "error": (
                                f"No hay suficiente stock disponible "
                                f"para {maquinaria.nombre} en las "
                                f"fechas seleccionadas."
                            )
                        }
                    )

            # Si todas las máquinas tienen disponibilidad,
            # recién aquí creamos el contrato.
            contrato = ContratoArriendo.objects.create(
                usuario=request.user
            )

            # Copiamos los elementos del carro al contrato.
            for item in items:

                ItemContrato.objects.create(
                    contrato=contrato,
                    maquinaria=item.maquinaria,
                    fecha_inicio=item.fecha_inicio,
                    fecha_fin=item.fecha_fin,
                    cantidad=item.cantidad,
                    tarifa_diaria=item.maquinaria.tarifa_diaria,
                    garantia=item.maquinaria.garantia,
                )

            # El carro queda vacío después de confirmar.
            items.delete()

        serializer = ContratoArriendoSerializer(contrato)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ContratoArriendoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContratoArriendoSerializer
    permission_classes = [IsEmpresa]

    def get_queryset(self):
        return ContratoArriendo.objects.filter(
            usuario=self.request.user
        )

class ItemCarroViewSet(viewsets.ModelViewSet):
    # Permite gestionar los items del carro de una empresa 

    serializer_class = ItemCarroSerializer
    permission_classes = [IsEmpresa]

    def get_queryset(self):
        return ItemCarro.objects.filter(
            carro__usuario=self.request.user
        )

    def perform_create(self, serializer):
        carro = CarroArriendo.objects.get(
            usuario=self.request.user
        )

        serializer.save(carro=carro)

from django.http import HttpResponse

from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def login_page(request):
    return render(request, "login.html")

def maquinaria_page(request):
    return render(request, "maquinaria.html")

def carro_page(request):
    return render(request, "carro.html")

def contratos_page(request):
    return render(request, "contratos.html")