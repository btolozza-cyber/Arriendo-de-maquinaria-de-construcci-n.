from django.contrib.auth.models import AbstractUser
from django.db import models


#Representa al usuario del sistema, que puede ser una empresa o un ejecutivo
class User(AbstractUser):

    #Define los roles disponibles dentro del sistema
    class Role(models.TextChoices):
        EMPRESA = "EMPRESA", "Empresa Constructora"
        EJECUTIVO = "EJECUTIVO", "Ejecutivo de Arriendos"

    #Indica el rol que tiene cada usuario
    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )


#Representa una maquinaria disponible para ser arrendada
class Maquinaria(models.Model):

    #Define las categorías disponibles para las maquinarias
    class Categoria(models.TextChoices):
        EXCAVADORA = "EXCAVADORA", "Excavadora"
        GENERADOR = "GENERADOR", "Generador"
        ANDAMIO = "ANDAMIO", "Andamio"
        HORMIGONERA = "HORMIGONERA", "Hormigonera"

    #Nombre de la maquinaria
    nombre = models.CharField(
        max_length=100
    )

    #Categoría a la que pertenece la maquinaria
    categoria = models.CharField(
        max_length=30,
        choices=Categoria.choices
    )

    #Precio diario de arriendo de la maquinaria
    tarifa_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    #Monto de garantía solicitado por la maquinaria
    garantia = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    #Cantidad total de unidades disponibles
    stock_total = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre


#Representa el carro de arriendo de la empresa
class CarroArriendo(models.Model):

    #Usuario propietario del carro
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="carro"
    )

    def __str__(self):
        return f"Carro de {self.usuario.username}"


#Representa una maquinaria agregada al carro de arriendo
class ItemCarro(models.Model):

    #Carro al que pertenece el item
    carro = models.ForeignKey(
        CarroArriendo,
        on_delete=models.CASCADE,
        related_name="items"
    )

    #Maquinaria seleccionada para el arriendo
    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.PROTECT,
        related_name="items_carro"
    )

    #Fecha en que comienza el arriendo
    fecha_inicio = models.DateField()

    #Fecha en que termina el arriendo
    fecha_fin = models.DateField()

    #Cantidad de unidades solicitadas
    cantidad = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return f"{self.maquinaria.nombre} x {self.cantidad}"


#Representa un contrato de arriendo confirmado
class ContratoArriendo(models.Model):

    #Define los estados posibles de un contrato
    class Estado(models.TextChoices):
        PAGADO = "PAGADO", "Pagado"
        ENTREGADO = "ENTREGADO", "Entregado"
        COMPLETADO = "COMPLETADO", "Completado"
        CANCELADO = "CANCELADO", "Cancelado"

    #Usuario que realizó el contrato
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="contratos"
    )

    #Estado actual del contrato
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PAGADO
    )

    #Fecha y hora en que se creó el contrato
    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Contrato #{self.id} - {self.estado}"


#Representa una maquinaria incluida dentro de un contrato
class ItemContrato(models.Model):

    #Contrato al que pertenece el item
    contrato = models.ForeignKey(
        ContratoArriendo,
        on_delete=models.CASCADE,
        related_name="items"
    )

    #Maquinaria incluida en el contrato
    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.PROTECT,
        related_name="items_contrato"
    )

    #Fecha de inicio del arriendo
    fecha_inicio = models.DateField()

    #Fecha de término del arriendo
    fecha_fin = models.DateField()

    #Cantidad de unidades arrendadas
    cantidad = models.PositiveIntegerField(
        default=1
    )

    #Tarifa diaria utilizada al crear el contrato
    tarifa_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    #Garantía utilizada al crear el contrato
    garantia = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.maquinaria.nombre} x {self.cantidad}"