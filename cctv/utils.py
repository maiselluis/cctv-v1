
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from django.contrib.auth.models import User
#para el action user
from .models import UserActionLog
from functools import wraps

def send_email(subject, html_message, recipient_list):
    sender_email = settings.EMAIL_HOST_USER
    sender_password = settings.EMAIL_HOST_PASSWORD
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT

    try:
        # Configurar el mensaje con formato HTML
        msg = MIMEMultipart("alternative")  # Permite texto y HTML
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipient_list)
        msg["Subject"] = subject

        # Adjuntar el contenido HTML
        html_part = MIMEText(html_message, "html")  # Esto define que es HTML
        msg.attach(html_part)

        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        # Enviar el correo
        server.sendmail(sender_email, recipient_list, msg.as_string())

        # Cerrar conexión
        server.quit()

        return "✅ Email successfully sent in HTML format"

    except smtplib.SMTPAuthenticationError:
        return "❌ Authentication error: Please verify credentials"
    except Exception as e:
        return f"❌ Error sending email: {e}"

def get_notification_emails_by_location(location_id):
    """
    Retorna una lista de emails de usuarios que deben recibir notificaciones para una ubicación específica.
    """
    return User.objects.filter(notifications__location_id=location_id).values_list("email", flat=True)

def enviar_notificacion_reporte(reporte):
    asunto = f"CRC@CCTV Surveillance System"
    
    # Formato HTML para el mensaje
    mensaje_html = f"""
    <html>
     <body>        
        <h2> <strong>New report type: { reporte.report_type}</strong> </h2>
        <p><strong>🏷️ Tittle: { reporte.report_title}</h2>
        <p><strong>📌 Report No:</strong> {reporte.report_nro}</p>
        <p><strong>📅 Date:</strong> {reporte.date}</p>
        <p><strong>🕛 Time:</strong> {reporte.time.strftime("%I:%M %p")}</p>
        <p><strong>🌍 Branch:</strong> {reporte.location}</p>
        <p><strong>📍 Origination:</strong> {reporte.origination}</p>
        <p><strong>🏢 Location:</strong> {reporte.area}</p>   
        <p><strong>👨‍💼 Duty Manager:</strong> {reporte.duty_manager}</p>     
        <p><strong>👮‍♂️ Cctv Officer:</strong> {reporte.cctv_id}</p>
        <p><strong>📝 Details:</strong> {reporte.detail}</p>
        <p><strong>✅ Action Taken:</strong> {reporte.action_token}</p>
        <br>
        <p><a href="{ 'http://200.125.163.182/report/detail/' + str(reporte.report) }"  style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">  View Report </a></p>
    </body>
    </html>
    """
    destinatarios=list(get_notification_emails_by_location(reporte.location.id))
    if not destinatarios:
            return None 
    
    resultado = send_email(asunto, mensaje_html, destinatarios)
#   <p><a href="{ 'http://192.168.102.247/report/detail/' + str(reporte.report) if reporte.location.id == 1 else 'http://200.125.163.182/report/detail/' + str(reporte.report) }"  style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">  View Report </a></p>

  #  if reporte.location.id==1:
  #      destinatarios = ["mestrada@clubroyalcaribbean.net","bsiman@clubroyalcaribbean.net"]  
   
   # if reporte.location.id==2:     
    #    destinatarios = ["mestrada@clubroyalcaribbean.net","mchetram@clubroyalcaribbean.net"]
    #if reporte.location.id==5: 
     #   destinatarios = ["mestrada@clubroyalcaribbean.net","rbaliram@nimagroups.com"]

      
    #resultado = send_email(asunto, mensaje_html, destinatarios)
 
    #return resultado
def enviar_notificacion_blacklist(blacklist):
    asunto = f"CRC@CCTV Surveillance System (Notification of the end of the Blacklist period)."
    
    # Formato HTML para el mensaje
    mensaje_html = f"""
    <html>
   <body>        
        <h2> <strong>The customer has expired  their assigned blacklist period</strong> </h2>
       <p><strong> 📅  Blacklisted Date:</strong> {blacklist.date}</p>          
       <p><strong> 👤  Customer Name:</strong>  { blacklist.name}  { blacklist.surname}</p> 
       <p><strong> 🌍  Branch:</strong>  { blacklist.location.location}</p> 
       <p><strong> 🛑  Reason why he(she) was blacklisted:</strong> {blacklist.reason.reason}</p>       
       <p><strong> 📌  Blacklisted by:</strong> {blacklist.blacklistby.name} {blacklist.blacklistby.surname}</p>       
        <p><a href="{ 'http://200.125.163.182/blacklist/update/' + str(blacklist.id) }"  style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-size: 16px;">  Update Blacklisted Customer </a></p>
    </body>
    </html>
    """
   
    destinatarios=list(get_notification_emails_by_location(blacklist.location.id))   
    if not destinatarios:      
        return None 
 
    resultado = send_email(asunto, mensaje_html, destinatarios)


def enviar_notificacion_create_user(user):
        asunto = f"CRC@CCTV Surveillance System (New User Created)"        
        # Formato HTML para el mensaje
        mensaje_html = f"""
        <html>
          <body>        
            <h2> <strong>New user created in the system</strong> </h2>
        <p><strong> 👤  User Name:</strong>  { user.username}</p>          
        <p><strong> 📧  Email:</strong>  { user.email}</p>            
          </body>
        </html>
        """
        destinatarios=['mestrada@clubroyalcaribbean.net']    
        send_email(asunto, mensaje_html, destinatarios)

#para el action  de los usuarios
def log_user_action_decorator(action, extra_info=""):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                UserActionLog.objects.create(
                    user=request.user,
                    action=action,
                    url=request.path,
                    extra_info=extra_info
                )
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator