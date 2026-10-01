from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import (
    User,
    Maquinaria,
    CarroArriendo,
    ItemCarro,
    ContratoArriendo,
    ItemContrato,
)

# Se registra los modelos para que puedan administrarse desde el panel administrativo
admin.site.register(User)
admin.site.register(Maquinaria)
admin.site.register(CarroArriendo)
admin.site.register(ItemCarro)
admin.site.register(ContratoArriendo)
admin.site.register(ItemContrato)