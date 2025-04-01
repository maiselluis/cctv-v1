from .utils import enviar_notificacion_reporte
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.backends.signals import connection_created
from .models import Report

@receiver(post_save, sender=Report)
def notificar_nuevo_reporte(sender, instance, created, **kwargs):
    if created: 
        enviar_notificacion_reporte(instance)
@receiver(connection_created)
def configure_sqlite(sender, connection, **kwargs):
    if connection.vendor == 'sqlite':
        cursor = connection.cursor()
        cursor.execute("PRAGMA page_size = 65536;")  # 64 KB por página
        cursor.execute("PRAGMA cache_size = -524288;")  # ~32 GB de caché (-N significa en KB)
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA temp_store = MEMORY;")
        cursor.execute("PRAGMA mmap_size = 34359738368;")  # 32 GB de uso de memoria mapeada
        cursor.execute("PRAGMA memory_limit = 34359738368;")  # Límite total de memoria a 32 GB