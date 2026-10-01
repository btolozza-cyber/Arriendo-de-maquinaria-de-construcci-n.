from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, CarroArriendo


@receiver(post_save, sender=User)
def crear_carro_empresa(sender, instance, created, **kwargs):
    # Se crea automáticamente un carro de arriendo cuando un usuario se registra con rol de EMPRESA
    
    if instance.role == User.Role.EMPRESA:
        CarroArriendo.objects.get_or_create(
            usuario=instance
        )