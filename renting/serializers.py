from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    CarroArriendo,
    ItemCarro,
    Maquinaria,
    ContratoArriendo,
    ItemContrato,
)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Se personaliza el JWT para incluir información del usuario, principalmente, identificar su rol
    # Dentro del sistema 

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Se agrega el rol del usuario 
        token["role"] = user.role

        # El username para identificarlo.
        token["username"] = user.username

        return token

class MaquinariaSerializer(serializers.ModelSerializer):
    # Convierte los objetos de maquinaria a JSON, además de validar los datos recibidos en peticiones API

    class Meta:
        model = Maquinaria
        fields = [
            "id",
            "nombre",
            "categoria",
            "tarifa_diaria",
            "garantia",
            "stock_total",
        ]

class CarroArriendoSerializer(serializers.ModelSerializer):
   # Valida los datos recibidos y convierte los objetos del carro a JSON

    class Meta:
        model = CarroArriendo
        fields = [
            "id",
            "usuario",
        ]

class ItemCarroSerializer(serializers.ModelSerializer):
    # Convierte los items del carro entre objetos Django y JSON.
    # También valida fechas, cantidad y calcula el costo del arriendo.

    dias_arriendo = serializers.SerializerMethodField()
    costo_arriendo = serializers.SerializerMethodField()

    class Meta:
        model = ItemCarro
        fields = [
            "id",
            "carro",
            "maquinaria",
            "fecha_inicio",
            "fecha_fin",
            "cantidad",
            "dias_arriendo",
            "costo_arriendo",
        ]
        read_only_fields = [
            "carro",
            "dias_arriendo",
            "costo_arriendo",
        ]

    def validate(self, data):
        # La fecha de inicio debe ser anterior a la fecha de fin.
        if data["fecha_inicio"] >= data["fecha_fin"]:
            raise serializers.ValidationError(
                "La fecha de inicio debe ser anterior a la fecha de fin."
            )

        # La cantidad debe ser mayor que cero.
        if data["cantidad"] <= 0:
            raise serializers.ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        # La cantidad solicitada no puede superar
        # el stock total de la maquinaria.
        if data["cantidad"] > data["maquinaria"].stock_total:
            raise serializers.ValidationError(
                "La cantidad solicitada supera el stock disponible."
            )

        return data

    def get_dias_arriendo(self, obj):
        # Calcula los días de arriendo.
        return (obj.fecha_fin - obj.fecha_inicio).days

    def get_costo_arriendo(self, obj):
        # Calcula:
        # tarifa diaria × días + garantía.
        dias = (obj.fecha_fin - obj.fecha_inicio).days

        return (
            obj.maquinaria.tarifa_diaria * dias
            + obj.maquinaria.garantia
        )

class ItemContratoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemContrato
        fields = [
            "id",
            "maquinaria",
            "fecha_inicio",
            "fecha_fin",
            "cantidad",
            "tarifa_diaria",
            "garantia",
        ]

class ContratoArriendoSerializer(serializers.ModelSerializer):
    # Convierte los contratos de arriendo entre objetos Django y JSON.

    items = ItemContratoSerializer(many=True, read_only=True)

    class Meta:
        model = ContratoArriendo
        fields = [
            "id",
            "usuario",
            "estado",
            "fecha_creacion",
            "items",
        ]
        read_only_fields = [
            "usuario",
            "estado",
            "fecha_creacion",
            "items",
        ]