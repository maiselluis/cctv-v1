from .utils import enviar_notificacion_reporte,enviar_notificacion_blacklist,enviar_notificacion_create_user
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.backends.signals import connection_created
from .models import Report,BlackList,UserLocation
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .views import get_end_date
#para obtener localizacion del usuario conectado
from django.http import JsonResponse
from .views import get_client_ip,get_location_from_ip

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


@receiver(user_logged_in,sender=User)
def check_blacklist_on_login(sender, user, request, **kwargs):
        today = timezone.now().date()
        entry = BlackList.objects.filter(notified=False).exclude(Q(duration=6) | Q(duration=7))  
        for entry in entry:
              end_date = get_end_date(entry.date, entry.duration.id)  
              if end_date and end_date <= today:          
                enviar_notificacion_blacklist(entry)               
                entry.notified = True
                entry.save()

@receiver(post_save,sender=User)
def notify_user_created(sender, instance, created, **kwargs):
    if created:
       enviar_notificacion_create_user(instance)
#esto esat funcionando vbienperop la api no es libre
@receiver(user_logged_in,sender=User)
def user_location_view(sender, user, request, **kwargs):
    ip = get_client_ip(request)   
    location = get_location_from_ip(ip)  

    user_location = UserLocation( 
                                 ip=location.get('ip') ,
                                 user=user.username,
                                 latitude=location.get('latitude'),
                                 longitude=location.get('longitude'),
                                 city=location.get('city'),
                                 region=location.get('region'),
                                 country=location.get('country'), 
                                )
    user_location.save()
  