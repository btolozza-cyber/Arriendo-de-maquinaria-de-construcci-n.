from django.contrib.auth.models import AbstractUser
from django.db import models

#Usuario del sistema, que abarca tanto a la empresa que solicita la maquinaria, como el ejecutivo de arriendos. 
class User(AbstractUser):
    """Usuario del sistema."""

#Roles del usuario
    class Role(models.TextChoices):
        EMPRESA = "EMPRESA", "Empresa Constructora"
        EJECUTIVO = "EJECUTIVO", "Ejecutivo de Arriendos"

    role = models.CharField(
        max_length=20,
        choices=Role.choices
    )
    
#Maquinaria 
class Maquinaria(models.Model):
    #Representa los equipos disponibles para el arriendo, el EJECUTIVO es quien administra estos registros

    class Categoria(models.TextChoices):
        EXCAVADORA = "EXCAVADORA", "Excavadora"
        GENERADOR = "GENERADOR", "Generador"
        ANDAMIO = "ANDAMIO", "Andamio"
        HORMIGONERA = "HORMIGONERA", "Hormigonera"

    nombre = models.CharField(max_length=100)

    categoria = models.CharField(
        max_length=30,
        choices=Categoria.choices
    )

    tarifa_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    garantia = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock_total = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

#Carro de arriendo 
class CarroArriendo(models.Model):
    #Representa el carro (completo) de arriendo de la constructora, única por usuario (Independiente cierre sesión o el acceso desde otro dispositivo )

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="carro"
    )

    def __str__(self):
        return f"Carro de {self.usuario.username}"

#Items del carro
class ItemCarro(models.Model):
    #Se representa toda la maquínaria agregada al carro de arriendo 
    #Un carro puede tener diferentes items, por lo que se aplica ForeignKey

    carro = models.ForeignKey(
        CarroArriendo,
        on_delete=models.CASCADE,
        related_name="items"
    )

    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.PROTECT,
        related_name="items_carro"
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.maquinaria.nombre} x {self.cantidad}"

#Contrato de arriendo 
class ContratoArriendo(models.Model):
    #Representa el contrato de arriendo confirmado por la empresa, se conserva el historial del arriendo y su estado
    #El stock solo es validado y reservado cuando el contrato pase al estado PAGADO

    class Estado(models.TextChoices):
        PAGADO = "PAGADO", "Pagado"
        ENTREGADO = "ENTREGADO", "Entregado"
        COMPLETADO = "COMPLETADO", "Completado"
        CANCELADO = "CANCELADO", "Cancelado"

    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="contratos"
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PAGADO
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Contrato #{self.id} - {self.estado}"

#Items del contrato
class ItemContrato(models.Model):
    #Representa las máquinas que se contienen en el contrato 
    #Se guarda la tarifa diaria y la garantía utilizadas al momento de contratar

    contrato = models.ForeignKey(
        ContratoArriendo,
        on_delete=models.CASCADE,
        related_name="items"
    )

    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.PROTECT,
        related_name="items_contrato"
    )

    fecha_inicio = models.DateField()

    fecha_fin = models.DateField()

    cantidad = models.PositiveIntegerField(default=1)

    tarifa_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    garantia = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.maquinaria.nombre} x {self.cantidad}"
    