from rest_framework import viewsets, status
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

from .permissions import IsEjecutivo, IsEmpresa

from .serializers import (
    CustomTokenObtainPairSerializer,
    MaquinariaSerializer,
    CarroArriendoSerializer,
    ItemCarroSerializer,
    ItemContratoSerializer,
    ContratoArriendoSerializer,
)

from django.shortcuts import render

class CustomTokenObtainPairView(TokenObtainPairView):
    # Se ajusta la vista para utilizar el serializer personalizado (Con los roles)

    serializer_class = CustomTokenObtainPairSerializer

class MaquinariaViewSet(viewsets.ModelViewSet):
    # Permite realizar operaciones CRUD sobre las maquinarias

    queryset = Maquinaria.objects.all()
    serializer_class = MaquinariaSerializer
    permission_classes = [IsEjecutivo]
    filterset_fields = ["categoria", "nombre"]

class CarroArriendoViewSet(viewsets.ModelViewSet):
    #
    
    serializer_class = CarroArriendoSerializer
    permission_classes = [IsEmpresa]

    def get_queryset(self):
        # Filtra el carro para que la empresa solamente
        # pueda acceder a su propio carro.
        return CarroArriendo.objects.filter(
            usuario=self.request.user
        )

    def perform_create(self, serializer):
        # El usuario se obtiene directamente del token JWT.
        # No permitimos que el cliente elija otro usuario.
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        # Obtiene únicamente el carro perteneciente
        # al usuario autenticado.
        carro = self.get_object()

        # Obtiene todos los items del carro.
        items = carro.items.all()

        # No se puede confirmar un carro vacío.
        if not items.exists():
            return Response(
                {"error": "El carro está vacío."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crea el contrato asociado al usuario autenticado.
        contrato = ContratoArriendo.objects.create(
            usuario=request.user
        )

        # Copia cada item del carro al contrato.
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

        # Vacía el carro después de confirmar el contrato.
        items.delete()

        # Devuelve el contrato creado.
        serializer = ContratoArriendoSerializer(contrato)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ContratoArriendoViewSet(viewsets.ModelViewSet):
    """
    Permite gestionar los contratos de arriendo.

    Cada empresa solamente puede acceder a sus propios contratos.
    """

    serializer_class = ContratoArriendoSerializer
    permission_classes = [IsEmpresa]

    def get_queryset(self):
        # La empresa solamente puede consultar
        # los contratos asociados a su propio usuario.
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