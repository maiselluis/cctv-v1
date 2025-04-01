from reportlab.lib.pagesizes import letter,landscape,portrait,A4

from reportlab.platypus import Table, TableStyle, Paragraph,Spacer,SimpleDocTemplate, Frame,PageBreak, PageTemplate
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Image
from reportlab.pdfgen import canvas
from django.http import JsonResponse,FileResponse, Http404,HttpResponse
from django.db.models import Count, F
from django.utils.dateparse import parse_date
from .models import *
import os
from django.conf import settings
from reportlab.lib.units import mm
from django.db.models import Sum
from reportlab.lib.colors import red,black
from django.db.models import Q

def generate_report(request,report):
         
      # Configuración del PDF
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'inline; filename="cliente_reporte.pdf"'
       # Crear un documento
      doc = SimpleDocTemplate(response, pagesize=letter)

      # Obtener estilos de muestra
      styles = getSampleStyleSheet()

      custom_style  = ParagraphStyle(
      name="CustomStyle",
      parent=styles["Normal"],
      fontName="Helvetica",  # Font name (e.g., Helvetica, Times-Roman, etc.)
      fontSize=12,           # Font size
      leading=14,            # Line spacing
     # spaceBefore=5,        # Space before paragraph
      #spaceAfter=5,         # Space after paragraph
           )
      normal_style = styles['Normal']
      header=styles['Heading3']    
 
      # Crear elementos del reporte
      elements = []
      loacation=''
      branch=''
    

     
     
      dat=Report.objects.filter(report=report).values('detail','action_token','area_id','location_id')
    
      for data in dat:
          
          area=Area.objects.filter(id=data['area_id']).values('area').first()
          if area:
              loacation=area['area']
          loc=Location.objects.filter(id=data['location_id']).values('location').first()
         
          if loc:
              branch=loc['location']
          

          detail=data['detail']
          parrafos = detail.split('\n\n')
          elements.append(Spacer(0, 230)) 
          paragraph_text = ("Detail:")
          elements.append(Paragraph(paragraph_text, header))
          for parrafo in parrafos:          
            parrafo = parrafo.replace('\n', '<br/>')           
            elements.append(Paragraph(parrafo, custom_style))           
            elements.append(Spacer(1, 12))
     
          acction_taken=data['action_token']
          parrafos = acction_taken.split('\n\n')
          paragraph_text = ("Action Taken:")
         
          elements.append(Paragraph(paragraph_text, header))
          for parrafo in parrafos:          
            parrafo = parrafo.replace('\n', '<br/>')           
            elements.append(Paragraph(parrafo, custom_style))           
            elements.append(Spacer(1, 12))

             

      def draw_text_short(canvas, doc):
        
       
          # Dimensiones de la página
         width, height = letter
        
               #estilos
         styles = getSampleStyleSheet()
         normal_style = styles['Normal']
         
        
         elements = []
       
         image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
         full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
         image = ImageReader(full_path)
        
         canvas.drawImage(image, 100, height-100, width=60, height=70)

         # Título
         canvas.setFont("Times-Roman", 18)
         canvas.drawString((width/2)-30, height - 50, "Club Royal Caribbean")
         canvas.drawString((width/2)-30, height - 70, "CCTV Report")
         canvas.drawString((width/2)-30, height - 90, branch)
   
         
         
         datos=Report.objects.filter(report=report).values('date','time','location_id','usd_rate','euro_rate','gbp_rate','winning',
                                                         'box','dealer_id','customer_id','duty_manager_id','inspector_id','pittboss_id','other_id','detail','action_token',
                                                         'money_recovered','money_not_recovered','money_paid','money_not_paid','dubbed_to','origination_id','report_title_id','money_recovered','report_type','value_us','report_nro')
      
         for data in datos:
                  
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(50, height - 130, "Date")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(50, height - 150, str(data["date"]))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(120, height - 130, "Time")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(120, height - 150, str(data['time']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(180, height - 130, "Location")
            canvas.setFont("Times-Roman", 12)
          
            canvas.drawString(180, height - 150, loacation)
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(280, height - 130, "USD Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(280, height - 150, str(data['usd_rate']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(350, height - 130, "EURO Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(350, height - 150, str(data['euro_rate']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(430, height - 130, "GBP Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(430, height - 150,str(data['gbp_rate']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(500, height - 130, "Winning#")
            canvas.setFont("Times-Roman", 14)
            if data['winning']:
                canvas.drawString(500, height - 150, str(data['winning']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(565, height - 130, "Box#")
            canvas.setFont("Times-Roman", 12)
            if data['box']:
                canvas.drawString(565, height - 150, str(data['box']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(50, height - 170, "Staff Involved")
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(50, height - 190, "Name")
            canvas.setFont("Times-Roman", 12)
           
            duty=Staff.objects.filter(id=data['duty_manager_id']).values('name','surname','position').first()
            if duty:
                canvas.drawString(50, height - 210, str(duty['name']) +' '+ str(duty['surname']))
                pos=Position.objects.filter(id=duty['position']).values('name').first()
                canvas.drawString(250, height - 210,  str(pos['name']))
                canvas.drawString(400, height - 210,str(data['duty_manager_id']))
           
           
            pitboss=Staff.objects.filter(id=data['pittboss_id']).values('name','surname','position').first()
            if pitboss:
                canvas.drawString(50, height - 230, str(pitboss['name']) +' '+ str(pitboss['surname']))
                pos=Position.objects.filter(id=pitboss['position']).values('name').first()
                canvas.drawString(250, height - 230, str(pos['name']))
                canvas.drawString(400, height - 230, str(data['pittboss_id']))
         
            inspector=Staff.objects.filter(id=data['inspector_id']).values('name','surname','position').first()
            if inspector:
                canvas.drawString(50, height - 250, str(inspector['name']) +' '+ str(inspector['surname']))
                pos=Position.objects.filter(id=inspector['position']).values('name').first()
                canvas.drawString(250, height - 250,str(pos['name']))
                canvas.drawString(400, height - 250, str(data['inspector_id']))
            dealer=Staff.objects.filter(id=data['dealer_id']).values('name','surname','position').first()
            if dealer:
                canvas.drawString(50, height - 270,str(dealer['name']) +' '+ str(dealer['surname']))
                pos=Position.objects.filter(id=dealer['position']).values('name').first()
                canvas.drawString(250, height - 270, str(pos['name']))
                canvas.drawString(400, height - 270, str(data['dealer_id']))
                     
            other=Staff.objects.filter(id=data['other_id']).values('name','surname','position').first()  
          
            if other:
           
                canvas.drawString(50, height - 290,str(other['name']) +' '+ str(other['surname']))
                pos=Position.objects.filter(id=other['position']).values('name').first()
                canvas.drawString(250, height - 290, str(pos['name']))
                canvas.drawString(400, height - 290, str(data['other_id']))     
           
            
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(250, height - 190, "Position")
            canvas.setFont("Times-Bold", 12)
                   
            canvas.drawString(400, height - 190, "Id")
            canvas.setFont("Times-Roman", 12) 
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(450, height - 170, "Customer")
            canvas.setFont("Times-Roman", 12)
            customer=Customer.objects.filter(id=data['customer_id']).values('customer','photo').first()
            if customer:
                canvas.drawString(450, height - 190,str(customer['customer']))
            else:
                  canvas.drawString(450, height - 190,str("No Customer"))   
            # Imagen del cliente
            try:    
                                
               image_path = "media/"+customer['photo']  # Resolve the path to the static file
               
               full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
               image = ImageReader(full_path)

                # Draw the image on the PDF
               canvas.drawImage( image, 450, height - 310, width=100, height=100)            
              
            except Exception as e:
               canvas.setFont("Times-Italic", 10)
               image_path = "media/images/noimage.jpg"  # Resolve the path to the static file
               
               full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
               image = ImageReader(full_path)
               canvas.drawImage( image, 450, height - 310, width=100, height=100)      
            
             
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(50, height - 600, "Money Paid")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(50, height - 620, str( data['money_paid']))
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(150, height - 600, "Money Not Paid")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(150, height - 620, str(data['money_not_paid']))
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(270, height - 600, "Money Recovered")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(270, height - 620, str(data['money_recovered']))
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(400, height - 600, "Money Not Recovered")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(400, height - 620, str(data['money_not_recovered']))
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(530, height - 600, "Value (US)")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(530, height - 620, str(data['value_us']))

            canvas.setFont("Times-Bold", 12)
            canvas.drawString(50, height - 650, "Origination")
            origination=ReportOrigination.objects.filter(id=data['origination_id']).values('origination').first()
            if origination:
                canvas.setFont("Times-Roman", 12)
                canvas.drawString(50, height - 670, origination['origination'])
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(200, height - 650, "Footage")
            canvas.setFont("Times-Roman", 12)
            if data['dubbed_to'] :
                canvas.drawString(200, height - 670, "✓")
            else:
                canvas.drawString(200, height - 670, "✗")     
                  
            
            canvas.setFont("Times-Bold", 12)
            canvas.drawString(280, height - 650, "Type")
            typer=ReportType.objects.filter(id=data['report_type']).values('report_type').first()
            if typer:
                canvas.setFont("Times-Roman", 12)
                canvas.drawString(280, height - 670, typer['report_type'])
           
           
            canvas.setFont("Times-Roman", 11)
            title=ReportTitle.objects.filter(id=data['report_title_id']).values('title').first()
            
           # canvas.setFont("Times-Bold", 14)
          #  canvas.drawString(200, height - 310, "Title:")
            if title :
                canvas.setFont("Times-Bold", 16)
                canvas.drawString(180, height - 310, title['title'])
                canvas.setFont("Times-Bold", 11)
            canvas.drawString(530, height - 650, "Report #")
            canvas.setFont("Times-Roman", 11)
            canvas.drawString(550, height - 670,  str(data["report_nro"]))




      # Pie de página

            canvas.setFont("Times-Bold", 10)
            canvas.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")
            
            page_number_text = f"Page {canvas.getPageNumber()}"
          # Set the position of the page number
            canvas.drawRightString(200 * mm, 8 * mm, page_number_text)
      doc.build(elements, onFirstPage=draw_text_short)
      # Finalizar el PDF
    #  doc.showPage()
     # doc.save()
      return response

def generate_daily_shift (request,id):
     # Configuración del PDF
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'inline; filename="cliente_reporte.pdf"'
       # Crear un documento
      doc = SimpleDocTemplate(response, pagesize=letter)

      # Obtener estilos de muestra
      styles = getSampleStyleSheet()
      normal_style = styles['Normal']
      header=styles['Heading3']
    
     
 
      # Crear elementos del reporte
      elements = []
      loacation=''
      branch=''
      #token_position=430
      # detail_position=350
     
        
     
      dat=DailyShift.objects.filter(id=id).values('detail','location_id')
    
      for data in dat:          
         
          loc=Location.objects.filter(id=data['location_id']).values('location').first()
          if loc:
            
              branch=loc['location']
          
          #Details
          elements.append(Spacer(0, 250)) 
          paragraph_text = ("Detail:")
          elements.append(Paragraph(paragraph_text, header))
          elements.append(Spacer(0, 1))  
          elements.append(Paragraph(data['detail'], normal_style))
          elements.append(Spacer(10, 10))    
          
       
            
       

      def draw_text_short(canvas, doc):
        
       
          # Dimensiones de la página
         width, height = letter
        # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
        # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #  image = ImageReader(full_path)
        
       #  canvas.drawImage(image, 0, 0, width=width, height=height)
       #  transparencia = Color(1, 1, 1, alpha=0.5)  # Blanco semitransparente
       #  canvas.setFillColor(transparencia)
        # canvas.rect(0, 0, width, height, fill=True, stroke=False)
         image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
         full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
         image = ImageReader(full_path)
        
         canvas.drawImage(image, 100, height-100, width=60, height=70)
        
               #estilos
         styles = getSampleStyleSheet()
         normal_style = styles['Normal']
         
        
         elements = []

        # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        # image = ImageReader(full_path)
        
        # canvas.drawImage(image, 0, 0, width=width, height=height)

         # Título
         canvas.setFont("Times-Bold", 18)
         canvas.drawString(width/2-80, height - 50, "Club Royal Caribbean")
         canvas.drawString((width/2)-80, height - 70, "CCTV Daily Shift  Report")
         canvas.drawString((width/2)-50, height - 90, branch)
      
   
         
         
         datos=DailyShift.objects.filter(id=id).values('date','usd_rate','euro_rate','gbp_rate','casino_open','casino_close','shift_id',
                                                         'officer1_id','officer2_id','supervisor_id')
      
         for data in datos:
                  
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(50, height - 130, "Date")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(50, height - 150, str(data["date"]))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(120, height - 130, "Casino Open")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(120, height - 150, str(data['casino_open']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(210, height - 130, "Casino Close")
            canvas.setFont("Times-Roman", 12)
          
            canvas.drawString(210, height - 150, str(data['casino_close']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(320, height - 130, "USD Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(320, height - 150, str(data['usd_rate']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(400, height - 130, "EURO Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(400, height - 150, str(data['euro_rate']))
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(480, height - 130, "GBP Rate")
            canvas.setFont("Times-Roman", 12)
            canvas.drawString(480, height - 150,str(data['gbp_rate']))
          
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(50, height - 210, "Name")
            canvas.setFont("Times-Roman", 12)
            supervisor=Staff.objects.filter(id=data['supervisor_id']).values('name','surname','position').first()
            if supervisor:
                pos=Position.objects.filter(id=supervisor['position']).values('name').first()
                canvas.drawString(250, height - 240, str(pos['name']))
                canvas.drawString(400, height - 240, str(data['supervisor_id']))
                canvas.drawString(50, height - 240,str(supervisor['name']) +' '+ str(supervisor['surname']))
            officer1=Staff.objects.filter(id=data['officer1_id']).values('name','surname','position').first()
            if officer1:
                pos=Position.objects.filter(id=officer1['position']).values('name').first()
                canvas.drawString(250, height - 260, str(pos['name']))
                canvas.drawString(400, height - 260, str(data['officer1_id']))
             
                canvas.drawString(50, height - 260, str(officer1['name']) +' '+ str(officer1['surname']))
            officer2=Staff.objects.filter(id=data['officer2_id']).values('name','surname','position').first()
            if officer2:
                pos=Position.objects.filter(id=officer2['position']).values('name').first()
                canvas.drawString(250, height - 280, str(pos['name']))
                canvas.drawString(400, height - 280, str(data['officer2_id']))
                canvas.drawString(50, height - 280, str(officer2['name']) +' '+ str(officer2['surname']))
          
           
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(250, height - 210, "Position")
            canvas.drawString(400, height - 210, "Id")
           # Pie de página

            canvas.setFont("Times-Roman", 10)
            canvas.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
      doc.build(elements, onFirstPage=draw_text_short)
      # Finalizar el PDF
    #  doc.showPage()
     # doc.save()
      return response

def generate_cash_desk_transaction(request):
   
    location_idform=request.GET.get('location')
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    
    def get_cash_desk_summary(start_date, end_date, account_type_id,location):    # Realizar la consulta
        if location:
            results = (Cash_Desk_Transaction.objects.filter( date__range=(start_date, end_date),   account_type_id=account_type_id,location_id=location ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter( date__range=(start_date, end_date),   account_type_id=account_type_id ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))

        return results
    
    account_name=''
    count=0     

    # Valida y procesa las fechas
    if not date_begin:
        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')
       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:
       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')
    
    else:
        date_end = parse_date(date_end)

  
    # Filter data using the query
    if location_idform:
        transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end),location_id=location_idform ).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')
    else:
         transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end)).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')

  
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
  #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
  #  image = ImageReader(full_path)
        
 #   p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString(width/2-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-100, height - 70, "CCTV Cash Desk Transaction Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+80 , y_start, "Customer")
    p.drawString(x_start+200 , y_start, "Location")
    p.drawString(x_start+250 , y_start, "Token")
    p.drawString(x_start+290 , y_start, "TT$")
    p.drawString(x_start+330 , y_start, "USD")
    p.drawString(x_start+360 , y_start, "EURO")
    p.drawString(x_start+400 , y_start, "CAD")
    p.drawString(x_start+440 , y_start, "GBP")
    p.drawString(x_start+480 , y_start, "Employee")
    p.drawString(x_start+550 , y_start, "Authorized By")
    p.drawString(x_start+620 , y_start, "Branch")

 
   
    for record in transactions:
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        token=Token.objects.filter(id=record['token_id']).values('token').first()
        employeee_data=Staff.objects.filter(id=record['employee_id']).values('name','surname').first()
        authorized_data=Staff.objects.filter(id=record['autorized_by_id']).values('name','surname').first()
        account=AccountType.objects.filter(id=record['account_type_id']).values('account_type').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        
            
        if account!=account_name:         
           
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           p.drawString(x_start , y_start, account['account_type'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height

           result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform) 
          
           
        else:
           count+=1   
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        if custom:
            p.setFont("Times-Roman", 8)   
            p.drawString(x_start+80 , y_start, custom['customer'])
            p.setFont("Times-Roman", 9)   
        if area_cashier:
            p.drawString(x_start+200 , y_start, area_cashier['area_cashier'])
        if token:
            p.drawString(x_start+250 , y_start, token['token'])
        p.drawString(x_start+290 , y_start, str(record['tt_dolar']))
        p.drawString(x_start+330 , y_start, str(record['usd_dolar']))
        p.drawString(x_start+360 , y_start, str(record['euro_dolar']))
        p.drawString(x_start+400 , y_start, str(record['cad_dolar']))
        p.drawString(x_start+440 , y_start, str(record['gbp_dolar']))
        if employeee_data:
            p.drawString(x_start+480 , y_start, str(employeee_data['name']+' ' +employeee_data['surname']  ))
        if authorized_data:
           p.drawString(x_start+550 , y_start, str(authorized_data['name']+' ' +authorized_data['surname']  ) )      

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
        result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform) 
      
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 250, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Bold", 10)
                p.drawString(x_start+250 , y_start, "Sum:")
            
              

                p.drawString(x_start+290 , y_start, str(entry['tt_total']))
                p.drawString(x_start+330 , y_start, str(entry['usd_total']))
                p.drawString(x_start+360 , y_start, str(entry['euro_total']))
                p.drawString(x_start+400 , y_start, str(entry['cad_total']))
                p.drawString(x_start+440 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 10)


        account_name=account
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          p.setFont("Times-Roman", 10)
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)
       

       


    page_number_text = f"Page {p.getPageNumber()}"
    p.setFont("Times-Roman", 10)
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")        
    p.save()
    return response

def generate_poker_payouts(request):
  
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
  
    def get_poker_payout_summary(start_date, end_date, combination_id,location):    
           if location:
            results = (Poker_Payout.objects.filter(date__range=(start_date, end_date), combination_id=combination_id,location_id=location).values("combination_id").annotate(t_bet=Sum("bet"),t_payout=Sum("payout"),count=Count("combination_id")).order_by("combination_id"))
       
           else:
            results = (Poker_Payout.objects.filter(date__range=(start_date, end_date), combination_id=combination_id).values("combination_id").annotate(t_bet=Sum("bet"),t_payout=Sum("payout"),count=Count("combination_id")).order_by("combination_id"))      
          
           return results
   

    combination_name=''

    count=0
      

    # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
   
   
    if location_idform:
        poker_payout = Poker_Payout.objects.filter(date__range=(date_begin,date_end),location_id=location_idform ).values( 'id', 'date', 'time', 'bet','payout', 'customer_id', 'location_id', 'combination_id', 'table_id', 'dealer_id','inspector_id', 'pitboss_id').order_by('combination_id','date','time')
    else:
        poker_payout = Poker_Payout.objects.filter(date__range=(date_begin,date_end) ).values( 'id', 'date', 'time', 'bet','payout', 'customer_id', 'location_id', 'combination_id', 'table_id', 'dealer_id','inspector_id', 'pitboss_id').order_by('combination_id','date','time')

        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString(width/2-80, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-80, height - 70, "CCTV Poker Payouts Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+90  , y_start, "Table")
    p.drawString(x_start+130 , y_start, "Bet")
    p.drawString(x_start+180 , y_start, "Payout")
    p.drawString(x_start+240 , y_start, "Customer")
    p.drawString(x_start+340 , y_start, "Dealer")
    p.drawString(x_start+430 , y_start, "Inspector")   
    p.drawString(x_start+530 , y_start, "Pitbos")
    p.drawString(x_start+620 , y_start, "Branch")

 
    p.setFont("Times-Roman", 9) 
    for record in poker_payout:
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()
        dealer=Staff.objects.filter(id=record['dealer_id']).values('name', 'surname').first()
        inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()
        pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        combination=PokerCombination.objects.filter(id=record['combination_id']).values('poker_combination').first()
        table=PokerTable.objects.filter(id=record['table_id']).values('poker_table').first()
        
            
        if combination!=combination_name:          
         
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start, underline_y, x_start + 75, underline_y)
           p.drawString(x_start , y_start, combination['poker_combination'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height  
           result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform)            
           
        else:
           count+=1      
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        p.drawString(x_start+90 , y_start, str(table['poker_table']))
        p.drawString(x_start+130 , y_start, str('TT$'+ str( record['bet'])))
        p.drawString(x_start+180 , y_start, str('TT$'+ str( record['payout'])))

        if custom:
            p.setFont("Times-Roman", 8)   
            p.drawString(x_start+240 , y_start, custom['customer'])
            p.setFont("Times-Roman", 9)   
        if dealer:
            p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
        if inspector:
            p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
        if pitboss:
            p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
       
        result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform) 
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height
                p.setFont("Times-Bold", 9)
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 90, underline_y, x_start + 235, underline_y)
                p.drawString(x_start+90 , y_start, "Sum:")
                p.drawString(x_start+130 , y_start, str('TT$'+str(entry['t_bet'])))
                p.drawString(x_start+180 , y_start, str('TT$'+ str( entry['t_payout'])))
                p.setFont("Times-Roman", 10)
               

        combination_name=combination
        p.setFont("Times-Roman", 10)
        p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
        page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
        p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(240 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          y_start=height - 50
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #   image = ImageReader(full_path)
      #    p.drawImage(image, 0, 0, width=width, height=height)

       
    p.save()
    return response

def generate_daily_exception(request):
   
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')
    location_idform=request.GET.get('location')
    exclude=request.GET.get('exclude')
    employee_name=''     

    # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)  
    
    if location_idform:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end),location_id=location_idform ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
        if exclude=='true':
            excluded_departments = [11] 
            daily_exeption=daily_exeption.exclude(employee__department_id__in=excluded_departments)  
    else:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end) ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
        if exclude=='true':
            excluded_departments = [11] 
            daily_exeption=daily_exeption.exclude(employee__department_id__in=excluded_departments)  
   
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = portrait(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)

   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
 #   image = ImageReader(full_path)
  #  p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString(width/2-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Daily Exceptions Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Exception Type")     
   # p.drawString(x_start+200 , y_start, "Over Time")    
   # p.drawString(x_start+370 , y_start, "Shift Change")
    p.drawString(x_start+260 , y_start, "Branch")
    p.drawString(x_start+340 , y_start, "Notes")
   
    p.drawString(x_start+160 , y_start, "Time In")    
    p.drawString(x_start+210 , y_start, "Time Out")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 460, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 460, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
    #p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")


 
    p.setFont("Times-Roman", 12) 
    for record in daily_exeption:
        exception_type=ExceptionType.objects.filter(id=record['exception_type_id']).values('exeption_type').first()    
        
        employee=Staff.objects.filter(id=record['employee_id']).values('name', 'surname').first()       
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
            
        if employee!=employee_name:          
                
           y_start-=row_height+5
           p.setFont("Times-Bold", 12)
           p.drawString(x_start , y_start+5,str( employee['name'] +' ' +employee['surname'] )+' - ( ' +str( record['employee_id'] )+' )')
          # Línea discontinua debajo del texto
           underline_y_below_dashed = y_start   # Ajusta la posición debajo del texto
           dash_length = 5  # Longitud de cada segmento
           gap_length = 3  # Longitud del espacio entre segmentos

        # Dibujar línea discontinua
           x_start_dashed = x_start 
           x_end_dashed = x_start + 150
           current_x = x_start_dashed

           while current_x < x_end_dashed:
            # Dibuja un segmento de línea
            p.line(current_x, underline_y_below_dashed, min(current_x + dash_length, x_end_dashed), underline_y_below_dashed)
            # Salta un espacio
            current_x += dash_length + gap_length
                #   p.drawString(x_start , y_start, str( record['employee_id'] ))              
           y_start-=row_height
           p.setFont("Times-Roman", 11)     
                
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(exception_type['exeption_type']))
        if record['daily_from']:
            p.drawString(x_start+160 , y_start, str(record['daily_from'].strftime('%H:%M')))
        if record['daily_to']:
            p.drawString(x_start+210 , y_start, str(record['daily_to'].strftime('%H:%M')))
       # if record['total_hours']:
          #  p.drawString(x_start+280 , y_start, str(record['total_hours']))
       # if record['new_shift']:
        #    p.drawString(x_start+410 , y_start, str(record['new_shift'].strftime('%H:%M')))
       # if record['old_shift']:
         #   p.drawString(x_start+350 , y_start, str(record['old_shift'].strftime('%H:%M')))
        if record['detail']:
            p.drawString(x_start+340 , y_start, str(record['detail']))
       
        if location:
             p.drawString(x_start+260 , y_start, str(location['location']))

        employee_name=employee
       
        y_start -= row_height+5
        if y_start < 60:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
         
          p.drawRightString(200 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
       #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
      #    image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 11)

    page_number_text = f"Page {p.getPageNumber()}"
         
    p.drawRightString(200 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
    p.save()
    return response

def generate_counterfeit(request):
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    location_idform=request.GET.get('location')
     
    # Valida y procesa las fechas
    if not date_begin:
        date_begin=datetime.datetime.now().date()       
    else:
        date_begin = parse_date(date_begin)

    if not date_end:
        date_end=datetime.datetime.now().date()
    else:
        date_end = parse_date(date_end)
     
    
    def counterfeit_summary(date_begin, date_end,location):
        if location:
            results = (Counterfait.objects.filter(date__range=[date_begin, date_end],location_id=location ).aggregate(tt_dolar=Sum('tt_dolar'),tt_us_dolar=Sum('usd_dolar'), tt_gbp=Sum('gbp_dolar'), tt_euro_dolar=Sum('euro_dolar'),))
        else:
           results = (Counterfait.objects.filter(date__range=[date_begin, date_end] ).aggregate(tt_dolar=Sum('tt_dolar'),tt_us_dolar=Sum('usd_dolar'), tt_gbp=Sum('gbp_dolar'), tt_euro_dolar=Sum('euro_dolar'),))

        return results
    
    if location_idform:
        counterfeit = Counterfait.objects.filter(date__range=(date_begin,date_end),location_id=location_idform ).values( 'id', 'date', 'usd_dolar', 'tt_dolar','euro_dolar','gbp_dolar', 'serial_number', 'report_nro', 'notes', 'location_id','area_cashier','employee_id','customer_id').order_by('id')
    else:
        counterfeit = Counterfait.objects.filter(date__range=(date_begin,date_end) ).values( 'id', 'date', 'usd_dolar', 'tt_dolar','euro_dolar','gbp_dolar', 'serial_number', 'report_nro', 'notes', 'location_id','area_cashier','employee_id','customer_id').order_by('id')

   # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString(width/2-90, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Counterfeit Banknotes Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-90, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Location")     
    p.drawString(x_start+90 , y_start, "TT$")    
    p.drawString(x_start+140 , y_start, "USD")
    p.drawString(x_start+180 , y_start, "EURO")
    p.drawString(x_start+230 , y_start, "GBP")
    p.drawString(x_start+260 , y_start, "Serial No")
    p.drawString(x_start+310 , y_start, "Cashier")
    p.drawString(x_start+400 , y_start, "Customer")
    p.drawString(x_start+510 , y_start, "Branch")  
    p.drawString(x_start+570 , y_start, "Notes")  
    p.setFont("Times-Roman", 10) 
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start +650, underline_y_below)

    # Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 650, underline_y_above)
    y_start-=row_height
    y_start -= row_height
    for record in counterfeit:
       
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier']).values('area_cashier').first()
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()
        employee=Staff.objects.filter(id=record['employee_id']).values('name', 'surname').first()
       
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(area_cashier['area_cashier']))
        p.drawString(x_start+90 , y_start, str('TT$'+ str(record['tt_dolar'])))
        p.drawString(x_start+140 , y_start, str('$'+str(record['usd_dolar'])))
        p.drawString(x_start+180 , y_start, str('$'+ str(record['euro_dolar'])))
        p.drawString(x_start+230 , y_start, str('$'+ str( record['gbp_dolar'])))
        p.drawString(x_start+260 , y_start, str(record['serial_number']))      
       
        if location:
             p.drawString(x_start+510 , y_start, str(location['location']))
        p.drawString(x_start+570 , y_start, str(record['notes']))
        if custom:
             p.drawString(x_start+400 , y_start, str(custom['customer']))
        if employee:
            p.drawString(x_start+310 , y_start,str( employee['name'] +' ' +employee['surname'] ))

        if date_begin and date_end:
            result = counterfeit_summary(date_begin, date_end,location_idform) 
            y_start -= row_height+5

            if y_start < 50:
                page_number_text = f"Page {p.getPageNumber()}"
                p.drawRightString(260 * mm, 8 * mm, page_number_text)
                p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
                p.showPage()      
                y_start=height - 50
                p = canvas.Canvas(response, page_size)
               # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
              #  image = ImageReader(full_path)
              #  p.drawImage(image, 0, 0, width=width, height=height)
                p.setFont("Times-Roman", 10)
        
    y_start-=row_height+5
    p.setFont("Times-Bold", 10)
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 50, underline_y, x_start + 300, underline_y)
    y_start-=row_height
    p.drawString(x_start+50 , y_start, "Sum:")
    result = counterfeit_summary(date_begin, date_end,location_idform)
    p.drawString(x_start+90 , y_start, str( '$'+ str(result['tt_dolar'])))
    p.drawString(x_start+140 , y_start, str('$'+ str( result['tt_us_dolar'])))
    p.drawString(x_start+180 , y_start, str('$'+ str( result['tt_euro_dolar'])))
    p.drawString(x_start+230 , y_start, str('$'+ str( result['tt_gbp'])))              
    p.setFont("Times-Roman", 10)        

    
    page_number_text = f"Page {p.getPageNumber()}"
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
    
    p.save()
    return response

def generate_cd_error(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    location_idform=request.GET.get('location')
     
    # Valida y procesa las fechas
    if not date_begin:
        date_begin=datetime.datetime.now().date()       
    else:
        date_begin = parse_date(date_begin)

    if not date_end:
        date_end=datetime.datetime.now().date()
    else:
        date_end = parse_date(date_end) 
    
    def get_error_type_summary(start_date, end_date, error_type_id,location):    # Realizar la consulta
       if location:
        results = (Cash_Desk_Error.objects.filter(date__range=(start_date, end_date), error_type_id=error_type_id,location_id=location ).values("error_type_id") .annotate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),count=Count("error_type_id")).order_by("error_type_id"))
       else:
        results = (Cash_Desk_Error.objects.filter(date__range=(start_date, end_date), error_type_id=error_type_id ).values("error_type_id") .annotate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),count=Count("error_type_id")).order_by("error_type_id"))

       return results
    
    def total_error_type_summary(start_date,end_date,location):
        if location:
            results=( Cash_Desk_Error.objects.filter(date__range=(start_date, end_date),location_id=location).aggregate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),))
        else:
            results=( Cash_Desk_Error.objects.filter(date__range=(start_date, end_date)).aggregate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),))    
        return results
    
   

    error_type_name=''
    count=0
      

    # Filter data using the query
    if location_idform:
        error_type = Cash_Desk_Error.objects.filter(date__range=(date_begin,date_end),location_id=location_idform ).values( 'date', 'time', 'tt','usd', 'euro', 'area_cashier_id', 'error_type_id', 'location_id','cashier_id', 'duty_manager_id', 'supervisor_id').order_by('error_type_id')
    else:
        error_type = Cash_Desk_Error.objects.filter(date__range=(date_begin,date_end) ).values( 'date', 'time', 'tt','usd', 'euro', 'area_cashier_id', 'error_type_id', 'location_id','cashier_id', 'duty_manager_id', 'supervisor_id').order_by('error_type_id')
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)   
 
   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
  #  p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString(width/2-80, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-80, height - 70, "CCTV Cash Desk Error Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+100 , y_start, "Location")
    p.drawString(x_start+150 , y_start, "TT$")
    p.drawString(x_start+200 , y_start, "USD")
    p.drawString(x_start+250 , y_start, "Euro")
    p.drawString(x_start+290 , y_start, "Cashier")
    p.drawString(x_start+370 , y_start, "Duty Manager")
    p.drawString(x_start+470 , y_start, "Supervisor/Senior")    
    p.drawString(x_start+620 , y_start, "Branch") 
    p.setFont("Times-Roman", 10) 

    for record in error_type:
        error_type=CDErrorType.objects.filter(id=record['error_type_id']).values('error_type').first()
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        cashier=Staff.objects.filter(id=record['cashier_id']).values('name','surname').first()
        supervisor=Staff.objects.filter(id=record['supervisor_id']).values('name','surname').first()
        duty_manager=Staff.objects.filter(id=record['duty_manager_id']).values('name','surname').first()    
        location=Location.objects.filter(id=record['location_id']).values('location').first()        
            
        if error_type!=error_type_name:             
           count+=1         
           y_start-=row_height
           p.setFont("Times-Bold", 10)
           p.drawString(x_start , y_start, error_type['error_type'])
           p.setFont("Times-Roman", 10)             
           y_start-=row_height           
           
        else:
           count+=1   
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        if cashier:
            p.drawString(x_start+290 , y_start, str(cashier['name']+' ' +cashier['surname']  ))
          
        if area_cashier:
            p.drawString(x_start+100 , y_start, area_cashier['area_cashier'])
        
        p.drawString(x_start+150 , y_start, str(record['tt']))
        p.drawString(x_start+200 , y_start, str(record['usd']))
        p.drawString(x_start+250 , y_start, str(record['euro']))
    
      
        if duty_manager:
           p.drawString(x_start+370 , y_start, str(duty_manager['name']+' ' +duty_manager['surname']  ) ) 
        if supervisor:
            p.drawString(x_start+470 , y_start, str(supervisor['name']+' ' +supervisor['surname']  ))     

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location'])) 


        result = get_error_type_summary(date_begin, date_end, record['error_type_id'],location_idform)       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height
                p.setFont("Times-Bold", 10)
                p.drawString(x_start+100 , y_start, "Sum:")
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 100, underline_y, x_start + 280, underline_y)
                p.setFont("Times-Bold", 10) 

                p.drawString(x_start+150 , y_start, str(entry['tt_total']))
                p.drawString(x_start+200 , y_start, str(entry['usd_total']))
                p.drawString(x_start+250 , y_start, str(entry['euro_total']))
               
                p.setFont("Times-Roman", 10)


        error_type_name=error_type
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
         
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by Crc@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)

    result=total_error_type_summary(date_begin, date_end,location_idform) 
    y_start-=row_height
    p.setFont("Times-Bold", 10)
    p.drawString(x_start+80 , y_start, "Grand Total:")
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 80, underline_y, x_start + 280, underline_y)
    p.setFont("Times-Bold", 10) 
    p.drawString(x_start+150 , y_start, str(result['tt_total']))
    p.drawString(x_start+200 , y_start, str(result['usd_total']))
    p.drawString(x_start+250 , y_start, str(result['euro_total']))
    p.setFont("Times-Roman", 10)  

    page_number_text = f"Page {p.getPageNumber()}"
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
       
    p.save()
    return response

def generate_customer_blacklist(request,id):
              
      # Configuración del PDF
      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'inline; filename="cliente_reporte.pdf"'
  
      doc = SimpleDocTemplate(response, pagesize=letter)
 
      styles = getSampleStyleSheet()
      normal_style = styles['Normal']
      header=styles['Heading3']   
      elements = []
      loacation=''
      branch=''
        
      dat=BlackList.objects.filter(id=id).values('details','location')
    
      for data in dat:
      
          elements.append(Spacer(0, 250)) 
          paragraph_text = ("Detail:")
          elements.append(Paragraph(paragraph_text, header))
          elements.append(Spacer(0, 1))  
          elements.append(Paragraph(data['details'], normal_style))
          elements.append(Spacer(10, 10))  
          locat=Location.objects.filter(id=data['location']).values('location').first()
          if locat:
              branch=locat['location']        
            
       

      def draw_text_short(canvas, doc):     
       
         width, height = letter     
     
       #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
        # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #  image = ImageReader(full_path)
        
      #   canvas.drawImage(image, 0, 0, width=width, height=height)
         image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
         full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
         image = ImageReader(full_path)
        
         canvas.drawImage(image, 100, height-100, width=60, height=70)

         # Título
         canvas.setFont("Times-Roman", 18)
         canvas.drawString((width/2)-30, height - 50, "Club Royal Caribbean")
         canvas.drawString((width/2)-50, height - 70, "CCTV Blacklist Report")
         canvas.drawString((width/2)-30, height - 90, branch)
       
         
         datos=BlackList.objects.filter(id=id).values('id','name','surname','blacklistby','date','details','picture','sex','reason','race','duration','location')
      
         for data in datos:
                  
            canvas.setFont("Times-Bold", 14)
            canvas.drawString(80, height - 130, "Date:")            
            canvas.drawString(80, height - 160, "Name:")
            canvas.drawString(80, height - 190, "Surname:")
            canvas.drawString(80, height - 210, "Reason:")
            canvas.drawString(80, height - 240, "Race:")
            
            canvas.drawString(80, height - 270, "Blacklisted by:")
            canvas.drawString(80, height - 300, "Sex:")
            canvas.drawString(80, height - 330, "Duration:")        
            canvas.setFont("Times-Roman", 14)
            canvas.drawString(180, height - 130, str(data['date']))          
             
            canvas.drawString(180, height - 160, str(data['name']))
            canvas.drawString(180, height - 190, str(data['surname']))

            reason=Reason.objects.filter(id=data['reason']).values('reason').first()
            if reason:
                canvas.setFillColor(red)
                canvas.drawString(180, height - 210, str(reason['reason']) ) 
            
            race=Race.objects.filter(id=data['race']).values('race').first()
            if race:
                canvas.setFillColor(black)
                canvas.drawString(180, height - 240, str(race['race']) ) 

           
            blacklistby=Staff.objects.filter(id=data['blacklistby']).values('name','surname').first()
            if blacklistby:
                canvas.drawString(180, height - 270,str(blacklistby['name']) +' '+ str(blacklistby['surname']))
        
            sex=Sex.objects.filter(id=data['sex']).values('sex').first()
            if sex:
                canvas.drawString(180, height - 300, str(sex['sex']) )

            
            duration=Duration.objects.filter(id=data['duration']).values('duration').first()
            if duration:
                canvas.drawString(180, height - 330, str(duration['duration']) )
            
 
            try:      
                                
              image_path = "media/"+data['picture']  # Resolve the path to the static file
               
              full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
              image = ImageReader(full_path)          
              canvas.drawImage( image, 400, height - 250, width=100, height=100)         
              
            except Exception as e:
               canvas.setFont("Times-Italic", 10)
               image_path = "media/images/noimage.jpg"  # Resolve the path to the static file
               
               full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
               image = ImageReader(full_path)
               canvas.drawImage( image, 400, height - 250, width=100, height=100)
     
             
            canvas.setFont("Times-Bold", 10)
            canvas.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")
            
            page_number_text = f"Page {canvas.getPageNumber()}"
         
            canvas.drawRightString(200 * mm, 8 * mm, page_number_text)
      doc.build(elements, onFirstPage=draw_text_short)

      return response


def generate_daily_exception_by_employee(request):

     
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')
    location_idform=request.GET.get('location')
    employee_id=request.GET.get('employee')
 
    employee_name=''     

    # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)  
    if not  employee_id:
        employee_id=0
    
    if location_idform:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end),location_id=location_idform,employee_id=employee_id ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
    else:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end),employee_id=employee_id ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
   
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = portrait(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)

   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
 #   image = ImageReader(full_path)
  #  p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-120, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-180, height - 70, "CCTV Daily Exceptions Report by Employee")   
    p.setFont("Times-Bold", 11)
    p.drawString((width/2)-120, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Exception Type")     
  #  p.drawString(x_start+200 , y_start, "Over Time")    
 #   p.drawString(x_start+370 , y_start, "Shift Change")

   
    p.drawString(x_start+150 , y_start, "Time In")    
    p.drawString(x_start+200 , y_start, "Time Out")
    p.drawString(x_start+250 , y_start, "Branch")
    p.drawString(x_start+320 , y_start, "Notes")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 460, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 460, underline_y_above)
    y_start-=row_height
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")


 
    p.setFont("Times-Roman", 12) 
    for record in daily_exeption:
        exception_type=ExceptionType.objects.filter(id=record['exception_type_id']).values('exeption_type').first()    
        
        employee=Staff.objects.filter(id=record['employee_id']).values('name', 'surname').first()       
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
            
        if employee!=employee_name:          
                
           y_start-=row_height
           p.setFont("Times-Bold", 12)
           p.drawString(x_start , y_start,str( employee['name'] +' ' +employee['surname'] )+' - ( '+ str( record['employee_id'] )+')')
        #   p.drawString(x_start , y_start, str( record['employee_id'] ))    
     # Línea discontinua debajo del texto
           underline_y_below_dashed = y_start - 3  # Ajusta la posición debajo del texto
           dash_length = 5  # Longitud de cada segmento
           gap_length = 3  # Longitud del espacio entre segmentos

        # Dibujar línea discontinua
           x_start_dashed = x_start 
           x_end_dashed = x_start + 150
           current_x = x_start_dashed

           while current_x < x_end_dashed:
            # Dibuja un segmento de línea
            p.line(current_x, underline_y_below_dashed, min(current_x + dash_length, x_end_dashed), underline_y_below_dashed)
            # Salta un espacio
            current_x += dash_length + gap_length
                #   p.drawString(x_start , y_start, str( record['employee_id'] ))              
           y_start-=row_height +5
           p.setFont("Times-Roman", 12)     
                
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(exception_type['exeption_type']))
        if record['daily_from']:
            p.drawString(x_start+150 , y_start, str(record['daily_from'].strftime('%H:%M')))
        if record['daily_to']:
            p.drawString(x_start+200 , y_start, str(record['daily_to'].strftime('%H:%M')))
      #  if record['total_hours']:
        #    p.drawString(x_start+280 , y_start, str(record['total_hours']))
      #  if record['new_shift']:
       #     p.drawString(x_start+410 , y_start, str(record['new_shift'].strftime('%H:%M')))
      #  if record['old_shift']:
      #      p.drawString(x_start+350 , y_start, str(record['old_shift'].strftime('%H:%M')))
        if record['detail']:
            p.drawString(x_start+320 , y_start, str(record['detail']))
       
        if location:
             p.drawString(x_start+250 , y_start, str(location['location']))

        employee_name=employee
       
        y_start -= row_height+5
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
         
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
       #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
      #    image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 11)

    page_number_text = f"Page {p.getPageNumber()}"
         
    p.drawRightString(200 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")    
    p.save()
    return response

def generate_report_by_date(request):
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'

    # Create a PDF canvas
    page_size = portrait(letter)
    width, height = page_size
    p = canvas.Canvas(response, page_size)

    # Styles
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle(
        name="CustomStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=14,
    )
    header = styles['Heading3']

    # Parse dates
    date_begin = request.GET.get('date_begin', datetime.datetime.now().strftime('%Y-%m-%d'))
    date_end = request.GET.get('date_end', datetime.datetime.now().strftime('%Y-%m-%d'))
    location_idform = request.GET.get('location')
    date_begin = parse_date(date_begin)
    date_end = parse_date(date_end)

    # Retrieve reports
    if location_idform:
        datos = Report.objects.filter(
        date__range=[date_begin, date_end], location_id=location_idform
    ).values('date', 'time', 'location_id', 'usd_rate', 'euro_rate', 'gbp_rate', 'winning',
             'box', 'dealer_id', 'customer_id', 'duty_manager_id', 'inspector_id', 'pittboss_id',
             'other_id', 'detail', 'action_token', 'money_recovered', 'money_not_recovered',
             'money_paid', 'money_not_paid', 'dubbed_to', 'origination_id', 'report_title_id',
             'report', 'money_recovered', 'report_type', 'value_us', 'report_nro', 'area_id')
    else:
        datos = Report.objects.filter(
        date__range=[date_begin, date_end]).values('date', 'time', 'location_id', 'usd_rate', 'euro_rate', 'gbp_rate', 'winning',
             'box', 'dealer_id', 'customer_id', 'duty_manager_id', 'inspector_id', 'pittboss_id',
             'other_id', 'detail', 'action_token', 'money_recovered', 'money_not_recovered',
             'money_paid', 'money_not_paid', 'dubbed_to', 'origination_id', 'report_title_id',
             'report', 'money_recovered', 'report_type', 'value_us', 'report_nro', 'area_id')
   


    for data in datos:
        area=Area.objects.filter(id=data['area_id']).values('area').first()
        if area:
              loacation=area['area']
           
        loc=Location.objects.filter(id=data['location_id']).values('location').first()
         
        if loc:
              branch=loc['location']
             
        # Draw header
        branch = Location.objects.filter(id=data['location_id']).values('location').first().get('location', '')
        p.setFont("Times-Roman", 18)
        p.drawString((width / 2) - 30, height - 50, "Club Royal Caribbean")
        p.drawString((width / 2) - 30, height - 70, "CCTV Report")
        p.drawString((width / 2) - 30, height - 90, branch)
        #Image
        image_path = "/static/background-crc.jpg"  # Resolve the path to the static file               
        full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        image = ImageReader(full_path)        
        p.drawImage(image, 100, height-100, width=60, height=70)

        # Draw details
        p.setFont("Times-Bold", 14)
        p.drawString(50, height - 130, "Date")
        p.setFont("Times-Roman", 12)
        p.drawString(50, height - 150, str(data["date"]))
        p.setFont("Times-Bold", 12)
        p.drawString(120, height - 130, "Time")
        p.setFont("Times-Roman", 12)
        p.drawString(120, height - 150, str(data['time']))
        p.setFont("Times-Bold", 14)
        p.drawString(180, height - 130, "Location")
        p.setFont("Times-Roman", 12)
                
        p.drawString(180, height - 150, loacation)
        p.setFont("Times-Bold", 14)
        p.drawString(280, height - 130, "USD Rate")
        p.setFont("Times-Roman", 12)
        p.drawString(280, height - 150, str(data['usd_rate']))
        p.setFont("Times-Bold", 14)
        p.drawString(350, height - 130, "EURO Rate")
        p.setFont("Times-Roman", 12)
        p.drawString(350, height - 150, str(data['euro_rate']))
        p.setFont("Times-Bold", 14)
        p.drawString(430, height - 130, "GBP Rate")
        p.setFont("Times-Roman", 12)
        p.drawString(430, height - 150,str(data['gbp_rate']))
        p.setFont("Times-Bold", 14)
        p.drawString(500, height - 130, "Winning#")
        p.setFont("Times-Roman", 14)
        
        if data['winning']:
                p.drawString(500, height - 150, str(data['winning']))
               
        p.setFont("Times-Bold", 12)
        p.drawString(565, height - 130, "Box#")
        p.setFont("Times-Roman", 12)
        if data['box']:
               p.drawString(565, height - 150, str(data['box']))
               p.setFont("Times-Bold", 14)
        p.drawString(50, height - 170, "Staff Involved")
        p.setFont("Times-Bold", 14)
        p.drawString(50, height - 190, "Name")
        p.setFont("Times-Roman", 12)
                
        duty=Staff.objects.filter(id=data['duty_manager_id']).values('name','surname','position').first()
        if duty:
             p.drawString(50, height - 210, str(duty['name']) +' '+ str(duty['surname']))
             pos=Position.objects.filter(id=duty['position']).values('name').first()
             p.drawString(250, height - 210,  str(pos['name']))
             p.drawString(400, height - 210,str(data['duty_manager_id']))
                
                
        pitboss=Staff.objects.filter(id=data['pittboss_id']).values('name','surname','position').first()
        if pitboss:
                p.drawString(50, height - 230, str(pitboss['name']) +' '+ str(pitboss['surname']))
                pos=Position.objects.filter(id=pitboss['position']).values('name').first()
                p.drawString(250, height - 230, str(pos['name']))
                p.drawString(400, height - 230, str(data['pittboss_id']))
        inspector=Staff.objects.filter(id=data['inspector_id']).values('name','surname','position').first()
        if inspector:
                p.drawString(50, height - 250, str(inspector['name']) +' '+ str(inspector['surname']))
                pos=Position.objects.filter(id=inspector['position']).values('name').first()
                p.drawString(250, height - 250,str(pos['name']))
                p.drawString(400, height - 250, str(data['inspector_id']))
        dealer=Staff.objects.filter(id=data['dealer_id']).values('name','surname','position').first()
        if dealer:
                p.drawString(50, height - 270,str(dealer['name']) +' '+ str(dealer['surname']))
                pos=Position.objects.filter(id=dealer['position']).values('name').first()
                p.drawString(250, height - 270, str(pos['name']))
                p.drawString(400, height - 270, str(data['dealer_id']))
                            
        other=Staff.objects.filter(id=data['other_id']).values('name','surname','position').first()  
                
        if other:
              p.drawString(50, height - 290,str(other['name']) +' '+ str(other['surname']))
              pos=Position.objects.filter(id=other['position']).values('name').first()
              p.drawString(250, height - 290, str(pos['name']))
              p.drawString(400, height - 290, str(data['other_id']))     
                
                    
        p.setFont("Times-Bold", 14)
        p.drawString(250, height - 190, "Position")
        p.setFont("Times-Bold", 12)
                        
        p.drawString(400, height - 190, "Id")
        p.setFont("Times-Roman", 12) 
        p.setFont("Times-Bold", 14)
        p.drawString(450, height - 170, "Customer")
        p.setFont("Times-Roman", 12)
        customer=Customer.objects.filter(id=data['customer_id']).values('customer','photo').first()
        if customer:
                p.drawString(450, height - 190,str(customer['customer']))
        else:
                p.drawString(450, height - 190,str("No Customer"))   
    
        try:    
                                        
                image_path = "media/"+customer['photo']  # Resolve the path to the static file
                
                full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
                image = ImageReader(full_path)

                        # Draw the image on the PDF
                p.drawImage( image, 450, height - 310, width=100, height=100)            
                    
        except Exception as e:
                p.setFont("Times-Italic", 10)
                image_path = "media/images/noimage.jpg"  # Resolve the path to the static file
                    
                full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
                image = ImageReader(full_path)
                p.drawImage( image, 450, height - 310, width=100, height=100)      
                    
                    
        p.setFont("Times-Bold", 12)
        p.drawString(50, height - 600, "Money Paid")
        p.setFont("Times-Roman", 12)
        p.drawString(50, height - 620, str( data['money_paid']))
        p.setFont("Times-Bold", 12)
        p.drawString(150, height - 600, "Money Not Paid")
        p.setFont("Times-Roman", 12)
        p.drawString(150, height - 620, str(data['money_not_paid']))
        p.setFont("Times-Bold", 12)
        p.drawString(270, height - 600, "Money Recovered")
        p.setFont("Times-Roman", 12)
        p.drawString(270, height - 620, str(data['money_recovered']))
        p.setFont("Times-Bold", 12)
        p.drawString(400, height - 600, "Money Not Recovered")
        p.setFont("Times-Roman", 12)
        p.drawString(400, height - 620, str(data['money_not_recovered']))
        p.setFont("Times-Bold", 12)
        p.drawString(530, height - 600, "Value (US)")
        p.setFont("Times-Roman", 12)
        p.drawString(530, height - 620, str(data['value_us']))

        p.setFont("Times-Bold", 12)
        p.drawString(50, height - 650, "Origination")
        origination=ReportOrigination.objects.filter(id=data['origination_id']).values('origination').first()
        if origination:
                        p.setFont("Times-Roman", 12)
                        p.drawString(50, height - 670, origination['origination'])
        p.setFont("Times-Bold", 12)
        p.drawString(200, height - 650, "Footage")
        p.setFont("Times-Roman", 12)
        if data['dubbed_to'] :
                 p.drawString(200, height - 670, "✓")
        else:
                p.drawString(200, height - 670, "✗")     
                        
                    
        p.setFont("Times-Bold", 12)
        p.drawString(280, height - 650, "Type")
        typer=ReportType.objects.filter(id=data['report_type']).values('report_type').first()
        if typer:
            p.setFont("Times-Roman", 12)
            p.drawString(280, height - 670, typer['report_type'])           
                
            p.setFont("Times-Roman", 11)
            title=ReportTitle.objects.filter(id=data['report_title_id']).values('title').first()
                    
               
        if title :
                   p.setFont("Times-Bold", 16)
                   p.drawString(180, height - 310, title['title'])
                   p.setFont("Times-Bold", 11)
        p.drawString(530, height - 650, "Report #")
        p.setFont("Times-Roman", 11)
        p.drawString(550, height - 670,  str(data["report_nro"]))

         # Add report details (e.g., "Detail" and "Action Taken")
        detail = data['detail']
        action_token = data['action_token']

        # Define custom style
        customStyle = {
            "header_font": "Times-Bold",
            "header_size": 14,
            "body_font": "Times-Roman",
            "body_size": 12,
            "line_spacing": 14,  # Line spacing for paragraphs
            "margin_left": 50,
            "margin_right": 550,  # PDF width minus margin
            "margin_bottom": 50,
        }

        # Function to draw text within boundaries
        def draw_wrapped_text(p, text, x, y, width, style):
            lines = []
            current_line = ""
            for word in text.split():
                if p.stringWidth(current_line + " " + word, style["body_font"], style["body_size"]) <= width:
                    current_line += " " + word if current_line else word
                else:
                    lines.append(current_line)
                    current_line = word
            if current_line:
                lines.append(current_line)

            for line in lines:
                p.drawString(x, y, line)
                y -= style["line_spacing"]
            return y

            # Draw "Detail" section
        p.setFont(customStyle["header_font"], customStyle["header_size"])
        p.drawString(customStyle["margin_left"], height - 350, "Detail:")

        y_cursor = height - 370
        p.setFont(customStyle["body_font"], customStyle["body_size"])
        for paragraph in detail.split('\n\n'):
        # Dividir el párrafo en líneas
         lines = paragraph.split('\n')

        # Dibujar línea por línea, respetando los saltos de línea originales
        for line in lines:
            y_cursor = draw_wrapped_text(
                p, line, customStyle["margin_left"], y_cursor,
                customStyle["margin_right"] - customStyle["margin_left"], customStyle
            )
        y_cursor -= customStyle["line_spacing"]  # Space between paragraphs

           # Draw "Action Taken" section
        p.setFont(customStyle["header_font"], customStyle["header_size"])
        p.drawString(customStyle["margin_left"], y_cursor - 20, "Action Taken:")

        y_cursor -= 40
        p.setFont(customStyle["body_font"], customStyle["body_size"])
        for paragraph in action_token.split('\n\n'):
              y_cursor = draw_wrapped_text(
                  p, paragraph, customStyle["margin_left"], y_cursor,
                    customStyle["margin_right"] - customStyle["margin_left"], customStyle
                )
        y_cursor -= customStyle["line_spacing"]  # Space between paragraphs
                
               # Add footer and move to the next page
        p.setFont("Times-Italic", 10)
        p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
        p.showPage()  # Move to the next page for the next report

                # Save the PDF
    p.save()
    return response

def generate_cash_desk_transaction_customer_expense(request):
    customer_id=request.GET.get('customer')   
    location_idform=request.GET.get('location')
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    custom = Customer.objects.filter(id=customer_id).values('customer').first() 


    
   
    
    def get_cash_desk_summary(start_date, end_date, account_type_id,location,customer):    # Realizar la consulta
        if location:
            results = (Cash_Desk_Transaction.objects.filter( account_type_id=account_type_id,date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(account_type_id=account_type_id, date__range=(start_date, end_date),customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))

        return results
    

    def get_cash_desk_summary_total(start_date, end_date,location,customer):    # Realizar la consulta
        if location:
            results = (Cash_Desk_Transaction.objects.filter( Q(account_type_id=37) | Q(account_type_id=7),date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(Q(account_type_id=37) | Q(account_type_id=7), date__range=(start_date, end_date),customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))

        return results
    account_name=''
    count=0     

    # Valida y procesa las fechas
    if not date_begin:
        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')
       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:
       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')
    
    else:
        date_end = parse_date(date_end)
   
    # Filter data using the query
    if location_idform:
        transactions = Cash_Desk_Transaction.objects.filter( Q(account_type_id=37) | Q(account_type_id=7),date__range=(date_begin,date_end),location_id=location_idform,customer_id=customer_id ).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')
    else:
         transactions = Cash_Desk_Transaction.objects.filter( Q(account_type_id=37) | Q(account_type_id=7),date__range=(date_begin,date_end),customer_id=customer_id).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')

  
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
  #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
  #  image = ImageReader(full_path)
        
 #   p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)    
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Customer Expense Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-80, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 16)

    p.drawString((width/2)-40, height-110, custom['customer'])
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Time")    
    p.drawString(x_start+120 , y_start, "Location")
    p.drawString(x_start+180 , y_start, "Token")
    p.drawString(x_start+240 , y_start, "TT$")
    p.drawString(x_start+300 , y_start, "USD")
    p.drawString(x_start+360 , y_start, "EURO")
    p.drawString(x_start+400 , y_start, "CAD")
    p.drawString(x_start+440 , y_start, "GBP")
    p.drawString(x_start+480 , y_start, "Employee")
    p.drawString(x_start+550 , y_start, "Authorized By")
    p.drawString(x_start+620 , y_start, "Branch")

 
   
    for record in transactions:
       
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        token=Token.objects.filter(id=record['token_id']).values('token').first()
        employeee_data=Staff.objects.filter(id=record['employee_id']).values('name','surname').first()
        authorized_data=Staff.objects.filter(id=record['autorized_by_id']).values('name','surname').first()
        account=AccountType.objects.filter(id=record['account_type_id']).values('account_type').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        
            
        if account!=account_name:         
           
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           p.drawString(x_start , y_start, account['account_type'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height

           result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform,customer_id)           
           
        else:
           count+=1   
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(record['time'].strftime('%H:%M')))
     
          
        if area_cashier:
            p.drawString(x_start+120 , y_start, area_cashier['area_cashier'])
        if token:
            p.drawString(x_start+180 , y_start, token['token'])
        p.drawString(x_start+240 , y_start, str(record['tt_dolar']))
        p.drawString(x_start+300 , y_start, str(record['usd_dolar']))
        p.drawString(x_start+360 , y_start, str(record['euro_dolar']))
        p.drawString(x_start+400 , y_start, str(record['cad_dolar']))
        p.drawString(x_start+440 , y_start, str(record['gbp_dolar']))
        if employeee_data:
            p.drawString(x_start+480 , y_start, str(employeee_data['name']+' ' +employeee_data['surname']  ))
        if authorized_data:
           p.drawString(x_start+550 , y_start, str(authorized_data['name']+' ' +authorized_data['surname']  ) )      

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
        result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform,customer_id) 
      
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 180, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Roman", 9)
                p.drawString(x_start+180 , y_start, "Sum:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)


        account_name=account
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          p.setFont("Times-Roman", 10)
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)
       

       

    result_total = get_cash_desk_summary_total(date_begin, date_end,location_idform,customer_id) 
    for entry in result_total:
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 160, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Bold", 9)
                p.drawString(x_start+160 , y_start, "Grand Total:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)

    page_number_text = f"Page {p.getPageNumber()}"
    p.setFont("Times-Roman", 10)
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")     
    p.save()
    return response

def generate_cash_desk_transaction_customer_cumplimentary(request):
    customer_id=request.GET.get('customer')   
    location_idform=request.GET.get('location')
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    custom=Customer.objects.filter(id=customer_id).values('customer').first()
    
    def get_cash_desk_summary(start_date, end_date, account_type_id,location,customer):  
        if location:
            results = (Cash_Desk_Transaction.objects.filter( account_type_id=account_type_id,date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(account_type_id=account_type_id, date__range=(start_date, end_date),customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))

        return results
    

    def get_cash_desk_summary_total(start_date, end_date,location,customer):    
        if location:
            results = (Cash_Desk_Transaction.objects.filter(Q(account_type=16) | Q(account_type=17) | Q(account_type=21) | Q(account_type=34) | Q(account_type=52) | Q(account_type=53),date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(Q(account_type=16) | Q(account_type=17) | Q(account_type=21) | Q(account_type=34) | Q(account_type=52) | Q(account_type=53), date__range=(start_date, end_date),customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))

        return results
    account_name=''
    count=0     

 
    if not date_begin:
        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')
       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:
       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')
    
    else:
        date_end = parse_date(date_end)

  
  
    if location_idform:
        transactions = Cash_Desk_Transaction.objects.filter(Q(account_type=16) | Q(account_type=17) | Q(account_type=21) | Q(account_type=34) | Q(account_type=52) | Q(account_type=53),date__range=(date_begin,date_end),location_id=location_idform,customer_id=customer_id ).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')
    else:
         transactions = Cash_Desk_Transaction.objects.filter(Q(account_type=16) | Q(account_type=17) | Q(account_type=21) | Q(account_type=34) | Q(account_type=52) | Q(account_type=53),date__range=(date_begin,date_end),customer_id=customer_id).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')

  
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
  #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
  #  image = ImageReader(full_path)
        
 #   p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Customer Complimentary Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-80, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 16)

    p.drawString((width/2)-60, height-110, custom['customer'])
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Time")    
    p.drawString(x_start+120 , y_start, "Location")
    p.drawString(x_start+180 , y_start, "Token")
    p.drawString(x_start+240 , y_start, "TT$")
    p.drawString(x_start+300 , y_start, "USD")
    p.drawString(x_start+360 , y_start, "EURO")
    p.drawString(x_start+400 , y_start, "CAD")
    p.drawString(x_start+440 , y_start, "GBP")
    p.drawString(x_start+480 , y_start, "Employee")
    p.drawString(x_start+550 , y_start, "Authorized By")
    p.drawString(x_start+620 , y_start, "Branch")

 
   
    for record in transactions:
       
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        token=Token.objects.filter(id=record['token_id']).values('token').first()
        employeee_data=Staff.objects.filter(id=record['employee_id']).values('name','surname').first()
        authorized_data=Staff.objects.filter(id=record['autorized_by_id']).values('name','surname').first()
        account=AccountType.objects.filter(id=record['account_type_id']).values('account_type').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        
            
        if account!=account_name:         
           
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           p.drawString(x_start , y_start, account['account_type'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height

           result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform,customer_id)           
           
        else:
           count+=1   
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(record['time'].strftime('%H:%M')))
     
          
        if area_cashier:
            p.drawString(x_start+120 , y_start, area_cashier['area_cashier'])
        if token:
            p.drawString(x_start+180 , y_start, token['token'])
        p.drawString(x_start+240 , y_start, str(record['tt_dolar']))
        p.drawString(x_start+300 , y_start, str(record['usd_dolar']))
        p.drawString(x_start+360 , y_start, str(record['euro_dolar']))
        p.drawString(x_start+400 , y_start, str(record['cad_dolar']))
        p.drawString(x_start+440 , y_start, str(record['gbp_dolar']))
        if employeee_data:
            p.drawString(x_start+480 , y_start, str(employeee_data['name']+' ' +employeee_data['surname']  ))
        if authorized_data:
           p.drawString(x_start+550 , y_start, str(authorized_data['name']+' ' +authorized_data['surname']  ) )      

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
        result = get_cash_desk_summary(date_begin, date_end, record['account_type_id'],location_idform,customer_id) 
      
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 180, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Roman", 9)
                p.drawString(x_start+180 , y_start, "Sum:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)


        account_name=account
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          p.setFont("Times-Roman", 10)
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)
       

       

    result_total = get_cash_desk_summary_total(date_begin, date_end,location_idform,customer_id) 
    for entry in result_total:
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 160, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Bold", 9)
                p.drawString(x_start+160 , y_start, "Grand Total:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)

    page_number_text = f"Page {p.getPageNumber()}"
    p.setFont("Times-Roman", 10)
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")     
    p.save()
    return response


def generate_cash_desk_transaction_by_customer(request):
    customer_id=request.GET.get('customer')     
    location_idform=request.GET.get('location')
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    if not customer_id:
        customer_id=0
   
    
    def get_cash_desk_summary(start_date, end_date, account_type_id,location,customer):  
        if location:
            results = (Cash_Desk_Transaction.objects.filter( account_type_id=account_type_id,date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(account_type_id=account_type_id, date__range=(start_date, end_date),customer_id=customer ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))

        return results
    

    def get_cash_desk_summary_total(start_date, end_date,location,customer):    
        if location:
            results = (Cash_Desk_Transaction.objects.filter(date__range=(start_date, end_date),location_id=location,customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter( date__range=(start_date, end_date),customer_id=customer ).values("customer_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("customer_id")).order_by("customer_id"))

        return results
    account_name=''
    count=0     

 
    if not date_begin:
        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')
       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:
       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')
    
    else:
        date_end = parse_date(date_end)

    
    
    custom=Customer.objects.filter(id=customer_id).values('customer').first()
  
    if location_idform:
        transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end),location_id=location_idform,customer_id=customer_id ).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')
    else:
         transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end),customer_id=customer_id).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')

  
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
  #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
  #  image = ImageReader(full_path)
        
 #   p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Customer Transactions Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-80, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 16)
    if customer_id:
        p.drawString((width/2)-60, height-110, custom['customer'])
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Time")    
    p.drawString(x_start+120 , y_start, "Location")
    p.drawString(x_start+180 , y_start, "Token")
    p.drawString(x_start+240 , y_start, "TT$")
    p.drawString(x_start+300 , y_start, "USD")
    p.drawString(x_start+360 , y_start, "EURO")
    p.drawString(x_start+400 , y_start, "CAD")
    p.drawString(x_start+440 , y_start, "GBP")
    p.drawString(x_start+480 , y_start, "Employee")
    p.drawString(x_start+550 , y_start, "Authorized By")
    p.drawString(x_start+620 , y_start, "Branch")

 
   
    for record in transactions:
       
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        token=Token.objects.filter(id=record['token_id']).values('token').first()
        employeee_data=Staff.objects.filter(id=record['employee_id']).values('name','surname').first()
        authorized_data=Staff.objects.filter(id=record['autorized_by_id']).values('name','surname').first()
        account=AccountType.objects.filter(id=record['account_type_id']).values('account_type').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        
            
        if account!=account_name:         
           
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           p.drawString(x_start , y_start, account['account_type'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height

           result = get_cash_desk_summary(date_begin, date_end,record['account_type_id'],location_idform,customer_id)           
           
        else:
           count+=1   
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(record['time'].strftime('%H:%M')))
     
          
        if area_cashier:
            p.drawString(x_start+120 , y_start, area_cashier['area_cashier'])
        if token:
            p.drawString(x_start+180 , y_start, token['token'])
        p.drawString(x_start+240 , y_start, str(record['tt_dolar']))
        p.drawString(x_start+300 , y_start, str(record['usd_dolar']))
        p.drawString(x_start+360 , y_start, str(record['euro_dolar']))
        p.drawString(x_start+400 , y_start, str(record['cad_dolar']))
        p.drawString(x_start+440 , y_start, str(record['gbp_dolar']))
        if employeee_data:
            p.drawString(x_start+480 , y_start, str(employeee_data['name']+' ' +employeee_data['surname']  ))
        if authorized_data:
           p.drawString(x_start+550 , y_start, str(authorized_data['name']+' ' +authorized_data['surname']  ) )      

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
        result = get_cash_desk_summary(date_begin, date_end,record['account_type_id'], location_idform,customer_id) 
      
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 180, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Roman", 9)
                p.drawString(x_start+180 , y_start, "Sum:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)


        account_name=account
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          p.setFont("Times-Roman", 10)
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)
       

       

    result_total = get_cash_desk_summary_total(date_begin, date_end,location_idform,customer_id) 
    for entry in result_total:
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 160, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Bold", 9)
                p.drawString(x_start+160 , y_start, "Grand Total:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)

    page_number_text = f"Page {p.getPageNumber()}"
    p.setFont("Times-Roman", 10)
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")     
    p.save()
    return response


def generate_cash_desk_transaction_by_account_type(request):
    account_type=request.GET.get('account_type')     
    location_idform=request.GET.get('location')
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 


    
    def get_cash_desk_summary(start_date, end_date, account_type_id,location):  
        if location:
            results = (Cash_Desk_Transaction.objects.filter( account_type_id=account_type,date__range=(start_date, end_date),location_id=location ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))
        else:
            results = (Cash_Desk_Transaction.objects.filter(account_type_id=account_type, date__range=(start_date, end_date) ).values("account_type_id").annotate(tt_total=Sum("tt_dolar"),usd_total=Sum("usd_dolar"),euro_total=Sum("euro_dolar"),gbp_total=Sum("gbp_dolar"),cad_total=Sum("cad_dolar"),count=Count("account_type_id")).order_by("account_type_id"))

        return results
    

  
    account_name=''
    count=0     

 
    if not date_begin:
        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')
       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:
       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')
    
    else:
        date_end = parse_date(date_end)
    
    
    if not account_type:
        account_type=1


  
  
    if location_idform:
        transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end),location_id=location_idform,account_type_id=account_type ).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')
    else:
         transactions = Cash_Desk_Transaction.objects.filter(date__range=(date_begin,date_end),account_type_id=account_type).values( 'transactions', 'date', 'time', 'tt_dolar',
                                                                                                    'usd_dolar', 'euro_dolar', 'gbp_dolar', 'cad_dolar', 'account_type_id', 'area_cashier_id',
                                                                                                      'customer_id', 'location_id', 'autorized_by_id', 'employee_id', 'token_id').order_by('account_type_id')

  
    account_name=AccountType.objects.filter(id=account_type).values('account_type').first()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
  #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
  #  image = ImageReader(full_path)
        
 #   p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)   
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-120, height - 70, "CCTV Account Type Transactions Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-80, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 16)

    p.drawString((width/2)-60, height-110, account_name['account_type'])
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+10 , y_start, "Time")    
    p.drawString(x_start+110 , y_start, "Location")
    p.drawString(x_start+170 , y_start, "Token")
    p.drawString(x_start+220 , y_start, "TT$")
    p.drawString(x_start+270 , y_start, "USD")
    p.drawString(x_start+310 , y_start, "EURO")
    p.drawString(x_start+360 , y_start, "CAD")
    p.drawString(x_start+400 , y_start, "GBP")
    p.drawString(x_start+440 , y_start, "Employee")
    p.drawString(x_start+520 , y_start, "Authorized By")
    p.drawString(x_start+620 , y_start, "Branch")

 
   
    for record in transactions:
       
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        token=Token.objects.filter(id=record['token_id']).values('token').first()
        employeee_data=Staff.objects.filter(id=record['employee_id']).values('name','surname').first()
        authorized_data=Staff.objects.filter(id=record['autorized_by_id']).values('name','surname').first()
        account=AccountType.objects.filter(id=record['account_type_id']).values('account_type').first()
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        
            
        if account!=account_name:         
           
           count+=1
         
           y_start-=row_height
           p.setFont("Times-Bold", 9)
           p.drawString(x_start , y_start, account['account_type'])
           p.setFont("Times-Roman", 9)             
           y_start-=row_height

           result = get_cash_desk_summary(date_begin, date_end,record['account_type_id'],location_idform)           
           
        else:
           count+=1   
        p.setFont("Times-Roman", 10)
        y_start-=row_height   
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+10 , y_start, str(record['time'].strftime('%H:%M')))
     
          
        if area_cashier:
            p.drawString(x_start+110 , y_start, area_cashier['area_cashier'])
        if token:
            p.drawString(x_start+170 , y_start, token['token'])
        p.drawString(x_start+220 , y_start, str(record['tt_dolar']))
        p.drawString(x_start+270 , y_start, str(record['usd_dolar']))
        p.drawString(x_start+310 , y_start, str(record['euro_dolar']))
        p.drawString(x_start+360 , y_start, str(record['cad_dolar']))
        p.drawString(x_start+400 , y_start, str(record['gbp_dolar']))
        if employeee_data:
            p.drawString(x_start+440 , y_start, str(employeee_data['name']+' ' +employeee_data['surname']  ))
        if authorized_data:
           p.drawString(x_start+520 , y_start, str(authorized_data['name']+' ' +authorized_data['surname']  ) )      

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location']))        
        result = get_cash_desk_summary(date_begin, date_end,record['account_type_id'], location_idform) 
      
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 180, underline_y, x_start + 460, underline_y)
                y_start-=row_height
              
                p.setFont("Times-Roman", 9)
                p.drawString(x_start+180 , y_start, "Sum:")
            
              

                p.drawString(x_start+220 , y_start, str('TT$ ')+str( entry['tt_total']))
                p.drawString(x_start+295 , y_start, str(entry['usd_total']))
                p.drawString(x_start+355 , y_start, str(entry['euro_total']))
                p.drawString(x_start+395 , y_start, str(entry['cad_total']))
                p.drawString(x_start+435 , y_start, str(entry['gbp_total']))
                p.setFont("Times-Roman", 9)


        account_name=account
      
        y_start -= row_height
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
          p.setFont("Times-Roman", 10)
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)
       
  

    page_number_text = f"Page {p.getPageNumber()}"
    p.setFont("Times-Roman", 10)
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")     
    p.save()
    return response

def generate_daily_exception_by_type(request):

     
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')
    location_idform=request.GET.get('location')
    exeption_type=request.GET.get('type')
 
    employee_name=''     

    # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)  
    if not  exeption_type:
        exeption_type=0
    
    if location_idform:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end),location_id=location_idform,exception_type_id=exeption_type ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
    else:
        daily_exeption = DailyExeption.objects.filter(date__range=(date_begin,date_end),exception_type_id=exeption_type ).values( 'id', 'date', 'daily_from', 'daily_to','total_hours', 'old_shift', 'new_shift', 'detail', 'exception_type_id', 'location_id','employee_id').order_by('employee_id','date')
   
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    #attachment para salvar directamente
    
    # Create a PDF canvas
    page_size = portrait(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)

   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
 #   image = ImageReader(full_path)
  #  p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-130, height - 70, "CCTV Daily Exceptions Report")   
    p.setFont("Times-Bold", 11)
    p.drawString((width/2)-90, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width+20 , y_start, "Exception Type")     
  #  p.drawString(x_start+200 , y_start, "Over Time")    
 #   p.drawString(x_start+370 , y_start, "Shift Change")

   
    p.drawString(x_start+150 , y_start, "Time In")    
    p.drawString(x_start+200 , y_start, "Time Out")
    p.drawString(x_start+250 , y_start, "Branch")
    p.drawString(x_start+320 , y_start, "Notes")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 460, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 460, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")


 
    p.setFont("Times-Roman", 11) 
    for record in daily_exeption:
        exception_type=ExceptionType.objects.filter(id=record['exception_type_id']).values('exeption_type').first()    
        
        employee=Staff.objects.filter(id=record['employee_id']).values('name', 'surname').first()       
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
            
        if employee!=employee_name:          
                
           y_start-=row_height
           p.setFont("Times-Bold", 12)
           p.drawString(x_start , y_start,str( employee['name'] +' ' +employee['surname'] )+' - ( '+ str( record['employee_id'] )+')')
         
           # Línea discontinua debajo del texto
           underline_y_below_dashed = y_start - 3  # Ajusta la posición debajo del texto
           dash_length = 5  # Longitud de cada segmento
           gap_length = 3  # Longitud del espacio entre segmentos

        # Dibujar línea discontinua
           x_start_dashed = x_start 
           x_end_dashed = x_start + 150
           current_x = x_start_dashed

           while current_x < x_end_dashed:
            # Dibuja un segmento de línea
            p.line(current_x, underline_y_below_dashed, min(current_x + dash_length, x_end_dashed), underline_y_below_dashed)
            # Salta un espacio
            current_x += dash_length + gap_length
                #   p.drawString(x_start , y_start, str( record['employee_id'] ))              
           y_start-=row_height +5
           p.setFont("Times-Roman", 11)     
                
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width+20 , y_start, str(exception_type['exeption_type']))
        if record['daily_from']:
            p.drawString(x_start+150 , y_start, str(record['daily_from'].strftime('%H:%M')))
        if record['daily_to']:
            p.drawString(x_start+200 , y_start, str(record['daily_to'].strftime('%H:%M')))
      #  if record['total_hours']:
        #    p.drawString(x_start+280 , y_start, str(record['total_hours']))
      #  if record['new_shift']:
       #     p.drawString(x_start+410 , y_start, str(record['new_shift'].strftime('%H:%M')))
      #  if record['old_shift']:
      #      p.drawString(x_start+350 , y_start, str(record['old_shift'].strftime('%H:%M')))
        if record['detail']:
            p.drawString(x_start+320 , y_start, str(record['detail']))
       
        if location:
             p.drawString(x_start+250 , y_start, str(location['location']))

        employee_name=employee
       
        y_start -= row_height+5
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
         
          p.drawRightString(200 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
          p.showPage()      
          y_start=height - 50
       #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
       #   full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
      #    image = ImageReader(full_path)
        
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 11)

    page_number_text = f"Page {p.getPageNumber()}"
         
    p.drawRightString(200 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")    
    p.save()
    return response


def generate_poker_payouts_synopsis_staff(request):
  
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    dealer_id=request.GET.get('dealer')
    inspector_id=request.GET.get('inspector')
    pitboss_id=request.GET.get('pitboss')
    if not dealer_id:
        dealer_id=None
    if not inspector_id:
        inspector_id=None
    if not pitboss_id:
        pitboss_id=None
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_poker_payout_summary(start_date, end_date, combination_id,location,dealer,inspector,pitboss):  
           filters = {
                "date__range": (start_date, end_date),
                "combination_id": combination_id,
                "location_id": location,  # Incluir la ubicación si está presente
                "dealer_id": dealer_id,      # Agregar dealer solo si no es None
                "inspector_id": inspector_id,
                "pitboss_id": pitboss_id
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values("combination_id") .annotate( t_bet=Sum("bet"), t_payout=Sum("payout"), count=Count("combination_id") ) .order_by("combination_id") )

           return results
    def poker_payout(start_date, end_date, location,dealer,inspector,pitboss):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "dealer_id": dealer_id,      # Agregar dealer solo si no es None
                "inspector_id": inspector_id,
                "pitboss_id": pitboss_id
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values( 'id', 'date', 'time', 'bet','payout', 'customer_id', 'location_id', 'combination_id', 'table_id', 'dealer_id','inspector_id', 'pitboss_id').order_by('combination_id','date','time') )

           return results
   

    combination_name=''

    count=0
      

   
   
   
    poker_payout=poker_payout(date_begin,date_end,location_idform,dealer_id,pitboss_id,inspector_id)   

        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-120, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-200, height - 70, "CCTV Poker Payouts Synopsis Staff Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-120, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+90  , y_start, "Table")
    p.drawString(x_start+130 , y_start, "Bet")
    p.drawString(x_start+180 , y_start, "Payout")
    p.drawString(x_start+240 , y_start, "Customer")
    p.drawString(x_start+340 , y_start, "Dealer")
    p.drawString(x_start+430 , y_start, "Inspector")   
    p.drawString(x_start+530 , y_start, "Pitbos")
    p.drawString(x_start+620 , y_start, "Branch")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 680, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 680, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in poker_payout:
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()       
        dealer=Staff.objects.filter(id=record['dealer_id']).values('name', 'surname').first()
             
        inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
        pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        combination=PokerCombination.objects.filter(id=record['combination_id']).values('poker_combination').first()
        table=PokerTable.objects.filter(id=record['table_id']).values('poker_table').first()
        
            
        if combination!=combination_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start, underline_y, x_start + 75, underline_y)
           p.drawString(x_start , y_start, combination['poker_combination'])
           p.setFont("Times-Roman", 10)             
           y_start-=row_height+5 
          
           result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform,dealer_id,inspector_id,pitboss_id)            
           
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        p.drawString(x_start+90 , y_start, str(table['poker_table']))
        p.drawString(x_start+130 , y_start, str('TT$'+ str( record['bet'])))
        p.drawString(x_start+180 , y_start, str('TT$'+ str( record['payout'])))

        if custom:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+240 , y_start, custom['customer'])
            p.setFont("Times-Roman", 10)   
        if dealer:
            p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
        if inspector:
            p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
        if pitboss:
            p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+620 ,y_start,str(location['location'])) 
       
       
        result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform,dealer_id,inspector_id,pitboss_id) 
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 90, underline_y, x_start + 235, underline_y)
                p.drawString(x_start+90 , y_start, "Sum:")
                p.drawString(x_start+130 , y_start, str('TT$'+str(entry['t_bet'])))
                p.drawString(x_start+180 , y_start, str('TT$'+ str( entry['t_payout'])))
                p.setFont("Times-Roman", 10)
               

        combination_name=combination
       
        y_start -= row_height+7
        if y_start < 50:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(240 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          y_start=height - 50
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #   image = ImageReader(full_path)
      #    p.drawImage(image, 0, 0, width=width, height=height)

    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response


def generate_poker_payouts_combination(request):  
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    combination_id=request.GET.get('combination')   
    if not combination_id:
        combination_id=None 
    if not location_idform:
        location_idform=None   
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    def get_poker_payout_summary(start_date, end_date, combination_id,location):  
           filters = {
                "date__range": (start_date, end_date),
                "combination_id": combination_id,
                "location_id": location, 
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values("combination_id") .annotate( t_bet=Sum("bet"), t_payout=Sum("payout"), count=Count("combination_id") ) .order_by("combination_id") )

           return results
    def poker_payout(start_date, end_date, location,combination_id):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  
                "combination_id": combination_id,               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values( 'id', 'date', 'time', 'bet','payout', 'customer_id', 'location_id', 'combination_id', 'table_id', 'dealer_id','inspector_id', 'pitboss_id').order_by('combination_id','date','time') )

           return results 

    combination_name=''
    count=0
    poker_payout=poker_payout(date_begin,date_end,location_idform,combination_id)   
        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-120, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-200, height - 70, "CCTV Poker Payouts Combination Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-120, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+90  , y_start, "Table")
    p.drawString(x_start+130 , y_start, "Bet")
    p.drawString(x_start+180 , y_start, "Payout")
    p.drawString(x_start+240 , y_start, "Customer")
    p.drawString(x_start+340 , y_start, "Dealer")
    p.drawString(x_start+430 , y_start, "Inspector")   
    p.drawString(x_start+530 , y_start, "Pitbos")
    p.drawString(x_start+620 , y_start, "Branch")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 680, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 680, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in poker_payout:
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()       
        dealer=Staff.objects.filter(id=record['dealer_id']).values('name', 'surname').first()
             
        inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
        pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        combination=PokerCombination.objects.filter(id=record['combination_id']).values('poker_combination').first()
        table=PokerTable.objects.filter(id=record['table_id']).values('poker_table').first()
        
            
        if combination!=combination_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start, underline_y, x_start + 75, underline_y)
           p.drawString(x_start , y_start, combination['poker_combination'])
           p.setFont("Times-Roman", 10)             
           y_start-=row_height+5 
          
           result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform)            
           
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        p.drawString(x_start+90 , y_start, str(table['poker_table']))
        p.drawString(x_start+130 , y_start, str('TT$'+ str( record['bet'])))
        p.drawString(x_start+180 , y_start, str('TT$'+ str( record['payout'])))

        if custom:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+240 , y_start, custom['customer'])
            p.setFont("Times-Roman", 10)   
        if dealer:
            p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
        if inspector:
            p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
        if pitboss:
            p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+620 ,y_start,str(location['location'])) 
       
       
        result = get_poker_payout_summary(date_begin, date_end, record['combination_id'],location_idform) 
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 90, underline_y, x_start + 235, underline_y)
                p.drawString(x_start+90 , y_start, "Sum:")
                p.drawString(x_start+130 , y_start, str('TT$'+str(entry['t_bet'])))
                p.drawString(x_start+180 , y_start, str('TT$'+ str( entry['t_payout'])))
                p.setFont("Times-Roman", 10)
               

        combination_name=combination
       
        y_start -= row_height+7
        if y_start < 50:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
         
          y_start=height - 50
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #   image = ImageReader(full_path)
      #    p.drawImage(image, 0, 0, width=width, height=height)

    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response


def generate_poker_payouts_customer(request):  
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    customer_id=request.GET.get('customer')   
 
    if not customer_id:
        customer_id=None 
   
    if not location_idform:
        location_idform=None   
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    def get_poker_payout_summary(start_date, end_date, customer_id,location,combination_id):  
           filters = {
                "date__range": (start_date, end_date),
                "customer_id": customer_id,
                "location_id": location, 
                "combination_id":combination_id,
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values("combination_id") .annotate( t_bet=Sum("bet"), t_payout=Sum("payout"), count=Count("combination_id") ) .order_by("combination_id") )

           return results
    
    def poker_payout(start_date, end_date, location,customer_id):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  
                "customer_id": customer_id,               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Poker_Payout.objects.filter(**filters) .values( 'id', 'date', 'time', 'bet','payout', 'customer_id', 'location_id', 'combination_id', 'table_id', 'dealer_id','inspector_id', 'pitboss_id').order_by('combination_id','date','time') )

           return results 

    combination_name=''
    count=0
    poker_payout=poker_payout(date_begin,date_end,location_idform,customer_id)   
        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-120, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-200, height - 70, "CCTV Poker Payouts Customer Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-120, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+90  , y_start, "Table")
    p.drawString(x_start+130 , y_start, "Bet")
    p.drawString(x_start+180 , y_start, "Payout")
    p.drawString(x_start+240 , y_start, "Customer")
    p.drawString(x_start+340 , y_start, "Dealer")
    p.drawString(x_start+430 , y_start, "Inspector")   
    p.drawString(x_start+530 , y_start, "Pitbos")
    p.drawString(x_start+620 , y_start, "Branch")
    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 680, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 680, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in poker_payout:
        custom=Customer.objects.filter(id=record['customer_id']).values('customer').first()       
        dealer=Staff.objects.filter(id=record['dealer_id']).values('name', 'surname').first()
             
        inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
        pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        combination=PokerCombination.objects.filter(id=record['combination_id']).values('poker_combination').first()
        table=PokerTable.objects.filter(id=record['table_id']).values('poker_table').first()
        
            
        if combination!=combination_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start, underline_y, x_start + 75, underline_y)
           p.drawString(x_start , y_start, combination['poker_combination'])
           p.setFont("Times-Roman", 10)             
           y_start-=row_height+5 
          
           result = get_poker_payout_summary(date_begin, date_end, customer_id,location_idform,record['combination_id'])            
           
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        p.drawString(x_start+90 , y_start, str(table['poker_table']))
        p.drawString(x_start+130 , y_start, str('TT$'+ str( record['bet'])))
        p.drawString(x_start+180 , y_start, str('TT$'+ str( record['payout'])))

        if custom:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+240 , y_start, custom['customer'])
            p.setFont("Times-Roman", 10)   
        if dealer:
            p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
        if inspector:
            p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
        if pitboss:
            p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+620 ,y_start,str(location['location'])) 
       
       
        result = get_poker_payout_summary(date_begin, date_end,customer_id,location_idform, record['combination_id']) 
        print(result)
        print(result)
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 90, underline_y, x_start + 235, underline_y)
                p.drawString(x_start+90 , y_start, "Sum:")
                p.drawString(x_start+130 , y_start, str('TT$'+str(entry['t_bet'])))
                p.drawString(x_start+180 , y_start, str('TT$'+ str( entry['t_payout'])))
                p.setFont("Times-Roman", 10)
               

        combination_name=combination
       
        y_start -= row_height+7
        if y_start < 50:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
         
          y_start=height - 50
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
       #   image = ImageReader(full_path)
      #    p.drawImage(image, 0, 0, width=width, height=height)

    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_cd_error_synopsis(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end') 
    location_idform=request.GET.get('location')
    cashier_id=request.GET.get('cashier')
   
     
    # Valida y procesa las fechas
    if not date_begin:
        date_begin=datetime.datetime.now().date()       
    else:
        date_begin = parse_date(date_begin)

    if not date_end:
        date_end=datetime.datetime.now().date()
    else:
        date_end = parse_date(date_end) 
    
    if not cashier_id:
        cashier_id=0
    
    def get_error_type_summary(start_date, end_date, error_type_id,location,cashier_id):    # Realizar la consulta
       if location:
        results = (Cash_Desk_Error.objects.filter(date__range=(start_date, end_date), error_type_id=error_type_id,location_id=location,cashier_id=cashier_id ).values("error_type_id") .annotate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),count=Count("error_type_id")).order_by("error_type_id"))
       else:
        results = (Cash_Desk_Error.objects.filter(date__range=(start_date, end_date), error_type_id=error_type_id ).values("error_type_id") .annotate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),count=Count("error_type_id")).order_by("error_type_id"))

       return results
    
    def total_error_type_summary(start_date,end_date,location, cashier_id):
        if location:
            results=( Cash_Desk_Error.objects.filter(date__range=(start_date, end_date),location_id=location, cashier_id=cashier_id ).aggregate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),))
        else:
            results=( Cash_Desk_Error.objects.filter(date__range=(start_date, end_date),cashier_id=cashier_id).aggregate(tt_total=Sum("tt"),usd_total=Sum("usd"),euro_total=Sum("euro"),))    
        return results
    
   

    error_type_name=''
    count=0
      

    # Filter data using the query
    if location_idform:
        error_type = Cash_Desk_Error.objects.filter(date__range=(date_begin,date_end),location_id=location_idform,cashier_id=cashier_id ).values( 'date', 'time', 'tt','usd', 'euro', 'area_cashier_id', 'error_type_id', 'location_id','cashier_id', 'duty_manager_id', 'supervisor_id').order_by('error_type_id')
    else:
        error_type = Cash_Desk_Error.objects.filter(date__range=(date_begin,date_end),cashier_id=cashier_id ).values( 'date', 'time', 'tt','usd', 'euro', 'area_cashier_id', 'error_type_id', 'location_id','cashier_id', 'duty_manager_id', 'supervisor_id').order_by('error_type_id')
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cash_transactions_report.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)   
 
   # image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
  #  p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-130, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-170, height - 70, "CCTV Cash Desk Error Synopsis Cashier  Report")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-120, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 10)    
    x_start = 50
    y_start = height - 130
    row_height = 10
    col_width = 50
    
    p.drawString(x_start , y_start, "Date")
    p.drawString(x_start+col_width , y_start, "Time")
    p.drawString(x_start+100 , y_start, "Location")
    p.drawString(x_start+150 , y_start, "TT$")
    p.drawString(x_start+200 , y_start, "USD")
    p.drawString(x_start+250 , y_start, "Euro")
    p.drawString(x_start+290 , y_start, "Cashier")
    p.drawString(x_start+370 , y_start, "Duty Manager")
    p.drawString(x_start+470 , y_start, "Supervisor/Senior")    
    p.drawString(x_start+620 , y_start, "Branch") 
    p.setFont("Times-Roman", 10) 

    underline_y_below = y_start - 3  # Ligeramente debajo del texto
    p.line(x_start , underline_y_below, x_start + 680, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start , underline_y_above, x_start + 680, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

    for record in error_type:
        error_type=CDErrorType.objects.filter(id=record['error_type_id']).values('error_type').first()
        area_cashier=AreaCashier.objects.filter(id=record['area_cashier_id']).values('area_cashier').first()
        cashier=Staff.objects.filter(id=record['cashier_id']).values('name','surname').first()
        supervisor=Staff.objects.filter(id=record['supervisor_id']).values('name','surname').first()
        duty_manager=Staff.objects.filter(id=record['duty_manager_id']).values('name','surname').first()    
        location=Location.objects.filter(id=record['location_id']).values('location').first()        
            
        if error_type!=error_type_name:             
           count+=1         
           y_start-=row_height
           p.setFont("Times-Bold", 10)
           p.drawString(x_start , y_start, error_type['error_type'])
           p.setFont("Times-Roman", 10)             
           y_start-=row_height  +5         
           
        else:
           count+=1  
           y_start-=row_height  +5  
   
          
        p.drawString(x_start , y_start, str(record['date']))
        p.drawString(x_start+col_width , y_start, str(record['time'].strftime('%H:%M')))
        if cashier:
            p.drawString(x_start+290 , y_start, str(cashier['name']+' ' +cashier['surname']  ))
          
        if area_cashier:
            p.drawString(x_start+100 , y_start, area_cashier['area_cashier'])
        
        p.drawString(x_start+150 , y_start, str(record['tt']))
        p.drawString(x_start+200 , y_start, str(record['usd']))
        p.drawString(x_start+250 , y_start, str(record['euro']))
    
      
        if duty_manager:
           p.drawString(x_start+370 , y_start, str(duty_manager['name']+' ' +duty_manager['surname']  ) ) 
        if supervisor:
            p.drawString(x_start+470 , y_start, str(supervisor['name']+' ' +supervisor['surname']  ))     

        if location:
            p.drawString(x_start+620 ,y_start,str(location['location'])) 


        result = get_error_type_summary(date_begin, date_end, record['error_type_id'],location_idform,cashier_id)       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height
                p.setFont("Times-Bold", 10)
                p.drawString(x_start+100 , y_start, "Sum:")
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 100, underline_y, x_start + 280, underline_y)
                p.setFont("Times-Bold", 10) 

                p.drawString(x_start+150 , y_start, str(entry['tt_total']))
                p.drawString(x_start+200 , y_start, str(entry['usd_total']))
                p.drawString(x_start+250 , y_start, str(entry['euro_total']))
               
                p.setFont("Times-Roman", 10)


        error_type_name=error_type
      
        y_start -= row_height+5
        if y_start < 50:  # Check if space is running out
          page_number_text = f"Page {p.getPageNumber()}"
         
          p.drawRightString(260 * mm, 8 * mm, page_number_text)
          p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by Crc@Surveillance System")       
          p.showPage()      
          y_start=height - 50
         
        #  image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
        #  full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
        #  image = ImageReader(full_path)
        #  p.drawImage(image, 0, 0, width=width, height=height)
          p.setFont("Times-Roman", 10)

    result=total_error_type_summary(date_begin, date_end,location_idform,cashier_id) 
    y_start-=row_height+5
    p.setFont("Times-Bold", 10)
    p.drawString(x_start+80 , y_start, "Grand Total:")
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 80, underline_y, x_start + 280, underline_y)
    p.setFont("Times-Bold", 10) 
    p.drawString(x_start+150 , y_start, str(result['tt_total']))
    p.drawString(x_start+200 , y_start, str(result['usd_total']))
    p.drawString(x_start+250 , y_start, str(result['euro_total']))
    p.setFont("Times-Roman", 10)  

    page_number_text = f"Page {p.getPageNumber()}"
    p.drawRightString(260 * mm, 8 * mm, page_number_text)
    p.drawString(5 * mm, 8 * mm, "This report has been generated automatically by CRC@Surveillance System")       
       
    p.save()
    return response

def generate_report_synopsis_cctv(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    employee_id=request.GET.get('employee')
   
    if not employee_id:
        employee_id=None   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_report_synopsis_summary_cctv(start_date, end_date, employee_id,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,  # Incluir la ubicación si está presente
                "cctv_id_id": employee_id
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("cctv_id_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"),  t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("cctv_id_id") ).order_by("cctv_id_id") )

           return results
    
    def get_report_synopsis_total_summary_cctv(start_date, end_date,location,emlpoyee_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                  "cctv_id_id": employee_id      # Agregar dealer solo si no es None
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("report") ) )

           return results
    
    def report_synopsis_cctv(start_date, end_date, location,employee):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "cctv_id": employee      # Agregar dealer solo si no es None
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 'cctv_id_id', 'money_recovered',
                                                                 'money_not_recovered','money_paid', 'money_not_paid').order_by('cctv_id_id','date','time') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_cctv=report_synopsis_cctv(date_begin,date_end,location_idform,employee_id)   

        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-Surveillance")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Surveillance")
    p.drawString(x_start+col_width+30 , y_start, "No.")
    p.drawString(x_start+100  , y_start, "Report Tittle")
    p.drawString(x_start+290 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_cctv:
        #employee=Customer.objects.filter(id=record['customer_id']).values('customer').first()       
        employee=Staff.objects.filter(id=record['cctv_id_id']).values('name', 'surname').first()
             
      #  inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
    #    pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 100, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_cctv(date_begin, date_end, record['cctv_id_id'],location_idform) 
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+col_width+35, y_start+2, str(entry['count']))
             #  text_width = p.stringWidth(str(entry['count']), "Helvetica", 12)  # Ajusta la fuente y tamaño si es necesario
             #  text_height = 12  # Ajusta según el tamaño de fuente
             #  p.rect(x_start + col_width + 65, y_start - 2, text_width + 10, text_height + 4)
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+col_width+30  , y_start, str(record['report_nro']))
        p.drawString(x_start+100 , y_start, str(title['title']))
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+290 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

       
       # if dealer:
          #  p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
     #   if inspector:
         #   p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
      #  if pitboss:
        #    p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_cctv(date_begin, date_end, record['cctv_id_id'],location_idform) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value'] is not None:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                if entry['t_mrecov'] is not None:
                    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                if entry['t_mnotrecov'] is not None:
                    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                if entry['t_mpaid'] is not None:
                    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                if entry['t_mnotpaid'] is not None:
                    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
       

      
       
       
      

        y_start -= row_height+7
        if y_start < 60:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 60
    results = get_report_synopsis_total_summary_cctv(date_begin, date_end,location_idform,employee_id) 


    
  
    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start , y_start, "Sum of Report:")
    p.setFillColor(red)
    if results['reportcount'] is not None:
        p.drawString(x_start+80 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))

                


       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response


def generate_report_synopsis_dealer(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    employee_id=request.GET.get('employee')
   
   
    if not employee_id:
        employee_id=None   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_report_synopsis_summary_cctv(start_date, end_date, employee_id,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,  # Incluir la ubicación si está presente
                "dealer_id": employee_id,
                "dealer__isnull":False
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("dealer_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"),  t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("dealer_id") ).order_by("dealer_id") )

           return results
    
    def get_report_synopsis_total_summary_cctv(start_date, end_date,location,emlpoyee_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "dealer_id": employee_id,
                 "dealer__isnull":False
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("dealer_id") ) )

           return results
    
    def report_synopsis_cctv(start_date, end_date, location,employee):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "dealer_id": employee,
                "dealer__isnull":False
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 'dealer_id', 'money_recovered',
                                                                 'money_not_recovered','money_paid', 'money_not_paid').order_by('dealer_id','date') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_cctv=report_synopsis_cctv(date_begin,date_end,location_idform,employee_id)   



        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-Dealer/Cashier/Attendant")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Dealer/Cashier")
    p.drawString(x_start+col_width+30 , y_start, "No.")
    p.drawString(x_start+100  , y_start, "Report Tittle")
    p.drawString(x_start+290 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_cctv:
        #employee=Customer.objects.filter(id=record['customer_id']).values('customer').first() 
        if record['dealer_id']:
            employee=Staff.objects.filter(id=record['dealer_id']).values('name', 'surname').first()
   
             
      #  inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
    #    pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 70, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_cctv(date_begin, date_end, record['dealer_id'],location_idform) 
          
           for entry in result:
               p.setFillColor(red)
               if entry['count'] is not None:
                   p.drawString(x_start+col_width+35, y_start+2, str(entry['count']))
             #  text_width = p.stringWidth(str(entry['count']), "Helvetica", 12)  # Ajusta la fuente y tamaño si es necesario
             #  text_height = 12  # Ajusta según el tamaño de fuente
             #  p.rect(x_start + col_width + 65, y_start - 2, text_width + 10, text_height + 4)
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+col_width+30  , y_start, str(record['report_nro']))
        p.drawString(x_start+100 , y_start, str(title['title']))
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+290 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

       
       # if dealer:
          #  p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
     #   if inspector:
         #   p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
      #  if pitboss:
        #    p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_cctv(date_begin, date_end, record['dealer_id'],location_idform) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value'] is not None:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                if entry['t_mrecov'] is not None:
                    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                if entry['t_mnotrecov'] is not None:
                    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                if entry['t_mpaid'] is not None:
                    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                if entry['t_mnotpaid'] is not None:
                    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
       

      
       
       
      

        y_start -= row_height
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 40
    results = get_report_synopsis_total_summary_cctv(date_begin, date_end,location_idform,employee_id) 


    
  
    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+80 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))

                


       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_inspector(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    employee_id=request.GET.get('employee')
   
   
    if not employee_id:
        employee_id=None   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_report_synopsis_summary_inspector(start_date, end_date, employee_id,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,  # Incluir la ubicación si está presente
                "inspector_id": employee_id,
                "inspector__isnull":False
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("inspector_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"), 
                                                                                             t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("inspector_id") ).order_by("inspector_id") )

           return results
    
    def get_report_synopsis_total_summary_inspector(start_date, end_date,location,emlpoyee_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "inspector_id": employee_id,
                 "inspector__isnull":False
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("inspector_id") ) )

           return results
    
    def report_synopsis_inspector(start_date, end_date, location,employee):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "inspector_id": employee,
                "inspector__isnull":False
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 
                                                                'inspector_id', 'money_recovered','money_not_recovered','money_paid', 'money_not_paid')
                                                                .order_by('inspector_id','date') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_inspector=report_synopsis_inspector(date_begin,date_end,location_idform,employee_id)   



        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-(Inspector/Senior)")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Inspector/Senior")
    p.drawString(x_start+col_width+30 , y_start, "No.")
    p.drawString(x_start+100  , y_start, "Report Tittle")
    p.drawString(x_start+290 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_inspector:
        #employee=Customer.objects.filter(id=record['customer_id']).values('customer').first() 
        if record['inspector_id']:
            employee=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()
   
             
      #  inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
    #    pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 70, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_inspector(date_begin, date_end, record['inspector_id'],location_idform) 
          
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+col_width+35, y_start+2, str(entry['count']))
             #  text_width = p.stringWidth(str(entry['count']), "Helvetica", 12)  # Ajusta la fuente y tamaño si es necesario
             #  text_height = 12  # Ajusta según el tamaño de fuente
             #  p.rect(x_start + col_width + 65, y_start - 2, text_width + 10, text_height + 4)
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+col_width+30  , y_start, str(record['report_nro']))
        p.drawString(x_start+100 , y_start, str(title['title']))
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+290 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

       
       # if dealer:
          #  p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
     #   if inspector:
         #   p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
      #  if pitboss:
        #    p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_inspector(date_begin, date_end, record['inspector_id'],location_idform) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value'] is not None:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                if entry['t_mrecov'] is not None:
                    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                if entry['t_mnotrecov'] is not None:
                    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                if entry['t_mpaid'] is not None:
                    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                if entry['t_mnotpaid'] is not None:
                    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
       

      
       
       
      

        y_start -= row_height
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 40
    results = get_report_synopsis_total_summary_inspector(date_begin, date_end,location_idform,employee_id) 


    
  
    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+80 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))

                


       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_pitboss(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    employee_id=request.GET.get('employee')
   
   
    if not employee_id:
        employee_id=None   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)   
    


    def get_report_synopsis_summary_pitboss(start_date, end_date, employee_id,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,  # Incluir la ubicación si está presente
                "pittboss_id": employee_id,
                "pittboss__isnull":False
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("pittboss_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"), 
                                                                                             t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("pittboss_id") ).order_by("pittboss_id") )

           return results
    
    def get_report_synopsis_total_summary_pitboss(start_date, end_date,location,emlpoyee_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "pittboss_id": employee_id,
                 "pittboss__isnull":False
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("pittboss_id") ) )

           return results
    
    def report_synopsis_pitboss(start_date, end_date, location,employee):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "pittboss_id": employee,
                "pittboss__isnull":False
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 
                                                                'pittboss_id', 'money_recovered','money_not_recovered','money_paid', 'money_not_paid')
                                                                .order_by('pittboss_id','date') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_pitboss=report_synopsis_pitboss(date_begin,date_end,location_idform,employee_id)   



        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-(PitBoss/Supervisor)")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "PitBoss/Supervisor")
    p.drawString(x_start+col_width+30 , y_start, "No.")
    p.drawString(x_start+100  , y_start, "Report Tittle")
    p.drawString(x_start+290 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_pitboss:
        #employee=Customer.objects.filter(id=record['customer_id']).values('customer').first() 
        if record['pittboss_id']:
            employee=Staff.objects.filter(id=record['pittboss_id']).values('name', 'surname').first()
   
             
      #  inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
    #    pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 70, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_pitboss(date_begin, date_end, record['pittboss_id'],location_idform) 
          
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+col_width+35, y_start+2, str(entry['count']))
             #  text_width = p.stringWidth(str(entry['count']), "Helvetica", 12)  # Ajusta la fuente y tamaño si es necesario
             #  text_height = 12  # Ajusta según el tamaño de fuente
             #  p.rect(x_start + col_width + 65, y_start - 2, text_width + 10, text_height + 4)
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+col_width+30  , y_start, str(record['report_nro']))
        p.drawString(x_start+100 , y_start, str(title['title']))
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+290 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

       
       # if dealer:
          #  p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
     #   if inspector:
         #   p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
      #  if pitboss:
        #    p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_pitboss(date_begin, date_end, record['pittboss_id'],location_idform) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value'] is not None:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                if entry['t_mrecov'] is not None:
                    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                if entry['t_mnotrecov'] is not None:
                    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                if entry['t_mpaid'] is not None:
                    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                if entry['t_mnotpaid'] is not None:
                    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
      
      

        y_start -= row_height
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 40
    results = get_report_synopsis_total_summary_pitboss(date_begin, date_end,location_idform,employee_id) 

    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+80 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))
       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_title(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    title_id=request.GET.get('title')  
   
   
    if not title_id:
        title_id=None   

    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)        


    def get_report_synopsis_summary_title(start_date, end_date, title_id,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,  # Incluir la ubicación si está presente
                "report_title_id": title_id,
                "report_title__isnull":False
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("report_title_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"), 
                                                                                             t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("report_title_id") ).order_by("report_title_id") )

           return results
    
    def get_report_synopsis_total_summary_title(start_date, end_date,location,title_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "report_title_id": title_id,
                 "report_title__isnull":False
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("report_title_id") ) )

           return results
    
    def report_synopsis_title(start_date, end_date, location,title_id):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,  # Incluir la ubicación si está presente
                "report_title_id": title_id,
                "report_title__isnull":False
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 
                                                                'report_title_id', 'money_recovered','money_not_recovered','money_paid', 'money_not_paid')
                                                                .order_by('report_title_id','date') )

           return results
   

    title_name=''
    count=0
   
   
    synopsis_title=report_synopsis_title(date_begin,date_end,location_idform,title_id)   



        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-Report Title")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Report Title")
    p.drawString(x_start+230  , y_start, "Date")
    p.drawString(x_start+200, y_start, "No.")    
    p.drawString(x_start+290 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height
    #p.drawString(x_start+280 , y_start, "Overtime Hrs")
   # p.drawString(x_start+350 , y_start, "Old Shift")    
   # p.drawString(x_start+410 , y_start, "New Shift")

 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_title:
        #employee=Customer.objects.filter(id=record['customer_id']).values('customer').first() 
        if record['report_title_id']:
          #  employee=Staff.objects.filter(id=record['pittboss_id']).values('name', 'surname').first()
          title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
   
             
      #  inspector=Staff.objects.filter(id=record['inspector_id']).values('name', 'surname').first()     
    #    pitboss=Staff.objects.filter(id=record['pitboss_id']).values('name', 'surname').first()     
        location=Location.objects.filter(id=record['location_id']).values('location').first()
        title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if title!=title_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 180, underline_y)
           p.drawString(x_start-20 , y_start, str(title['title']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_title(date_begin, date_end, record['report_title_id'],location_idform) 
          
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+200, y_start+2, str(entry['count']))
             #  text_width = p.stringWidth(str(entry['count']), "Helvetica", 12)  # Ajusta la fuente y tamaño si es necesario
             #  text_height = 12  # Ajusta según el tamaño de fuente
             #  p.rect(x_start + col_width + 65, y_start - 2, text_width + 10, text_height + 4)
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start+230 , y_start, str(record['date']))
        p.drawString(x_start+200  , y_start, str(record['report_nro']))
       # p.drawString(x_start+100 , y_start, str(title['title']))
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+290 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

       
       # if dealer:
          #  p.drawString(x_start+340 , y_start, str(dealer['name']+' '+ dealer['surname']))
        
     #   if inspector:
         #   p.drawString(x_start+430 , y_start, str(inspector['name']+' '+ inspector['surname']))
        
      #  if pitboss:
        #    p.drawString(x_start+530 , y_start, str(pitboss['name']+' '+ pitboss['surname']))
       
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_title(date_begin, date_end, record['report_title_id'],location_idform) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value'] is not None:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                if entry['t_mrecov'] is not None:
                    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                if entry['t_mnotrecov'] is not None:
                    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                if entry['t_mpaid'] is not None:
                    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                if entry['t_mnotpaid'] is not None:
                    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        title_name=title
      
      

        y_start -= row_height
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 40
    results = get_report_synopsis_total_summary_title(date_begin, date_end,location_idform,title_id) 


    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start+130 , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+200, y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 250, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+250 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))
       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_overpayment(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    report_title=16
  
   
   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_report_synopsis_summary_overpayment(start_date, end_date, location,report_title,cctv_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "report_title_id" :report_title,
                 "cctv_id_id":cctv_id
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("cctv_id_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"),  t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("cctv_id_id") ).order_by("cctv_id_id") )

           return results
    
    def get_report_synopsis_total_summary_overpayment(start_date, end_date,location,report_title):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                "report_title_id" :report_title
                        
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("report") ) )

           return results
    
    def report_synopsis_overpayment(start_date, end_date, location,report_title):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,
                "report_title_id" :report_title
              
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 'cctv_id_id', 'money_recovered',
                                                                 'money_not_recovered','money_paid', 'money_not_paid').order_by('cctv_id_id','date','time') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_cctv=report_synopsis_overpayment(date_begin,date_end,location_idform,report_title)   

        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-100, height - 70, "CCTV Report Synopsis")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 14)
    p.setFillColor(red)
    p.drawString((width/2)-60, height - 110,"Overpayment")
    p.setFillColorRGB(0, 0, 0)  
   
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Surveillance")
    p.drawString(x_start+150 , y_start, "Report #.")   
    p.drawString(x_start+220 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height


 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_cctv:
        
        employee=Staff.objects.filter(id=record['cctv_id_id']).values('name', 'surname').first()
             
    
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 100, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_overpayment(date_begin, date_end,location_idform,report_title, record['cctv_id_id']) 
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+150, y_start+2, str(entry['count']))
          
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+150  , y_start, str(record['report_nro']))
    
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+220 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_overpayment(date_begin, date_end, location_idform,report_title,record['cctv_id_id']) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value']:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
       

      
       
       
      

        y_start -= row_height+7
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 60
    results = get_report_synopsis_total_summary_overpayment(date_begin, date_end,location_idform,report_title) 

    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start+85 , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+150 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))

    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_underpayment(request):

    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location')
    report_title=20  
   
   
    if not location_idform:
        location_idform=None
    
     # Valida y procesa las fechas
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)    
    


    def get_report_synopsis_summary_overpayment(start_date, end_date, location,report_title,cctv_id):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                 "report_title_id" :report_title,
                 "cctv_id_id":cctv_id
               
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values("cctv_id_id") .annotate( t_value=Sum("value_us"), t_mrecov=Sum("money_recovered"), 
                                                                                           t_mnotrecov=Sum("money_not_recovered"),  t_mpaid=Sum("money_paid"),  t_mnotpaid=Sum("money_not_paid"),
                                                                                             count=Count("cctv_id_id") ).order_by("cctv_id_id") )

           return results
    
    def get_report_synopsis_total_summary_overpayment(start_date, end_date,location,report_title):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,
                "report_title_id" :report_title
                        
                           
                    }

            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("report") ) )

           return results
    
    def report_synopsis_overpayment(start_date, end_date, location,report_title):  
           filters = {
                "date__range": (start_date, end_date),            
                "location_id": location,
                "report_title_id" :report_title
              
               
                     }

            # Filtrar valores None
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 'cctv_id_id', 'money_recovered',
                                                                 'money_not_recovered','money_paid', 'money_not_paid').order_by('cctv_id_id','date','time') )

           return results
   

    employee_name=''
    count=0
   
   
    synopsis_cctv=report_synopsis_overpayment(date_begin,date_end,location_idform,report_title)   

        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'inline; filename="report_synopisis_cctv.pdf"'
    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-100, height - 70, "CCTV Report Synopsis")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
    p.setFont("Times-Bold", 14)
    p.setFillColor(red)
    p.drawString((width/2)-60, height - 110,"Underpayment")
    p.setFillColorRGB(0, 0, 0)  
   
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Surveillance")
    p.drawString(x_start+150 , y_start, "Report #.")   
    p.drawString(x_start+220 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height


 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_cctv:
        
        employee=Staff.objects.filter(id=record['cctv_id_id']).values('name', 'surname').first()
             
    
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()
        
            
        if employee!=employee_name:          
           p.setFont("Times-Roman", 10) 
           count+=1
         
           y_start-=row_height+5
           p.setFont("Times-Bold", 10)
           underline_y = y_start - 2  # Slightly below the text
           p.line(x_start-20, underline_y, x_start + 100, underline_y)
           p.drawString(x_start-20 , y_start, str(employee['name']+' '+ employee['surname']))
          
           p.setFont("Times-Roman", 10)             
      
          
           result = get_report_synopsis_summary_overpayment(date_begin, date_end,location_idform,report_title, record['cctv_id_id']) 
           for entry in result:
               p.setFillColor(red)
               p.drawString(x_start+150, y_start+2, str(entry['count']))
          
               p.setFillColorRGB(0, 0, 0)          
           y_start-=row_height+5  
        else:
           count+=1      
        p.setFont("Times-Roman", 10)   
        p.drawString(x_start-20 , y_start, str(record['date']))
        p.drawString(x_start+150  , y_start, str(record['report_nro']))
    
        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+220 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))

        if location:
            p.drawString(x_start+640 ,y_start,str(location['location'])) 
       
       
        result = get_report_synopsis_summary_overpayment(date_begin, date_end, location_idform,report_title,record['cctv_id_id']) 
       
       
        for entry in result:
            count_value = entry['count']
         
            if  count==count_value:           
                
                count=0
                y_start-=row_height+5
                p.setFont("Times-Bold", 9)
              
                underline_y = y_start - 2  # Slightly below the text
                p.line(x_start + 290, underline_y, x_start + 630, underline_y)
                p.drawString(x_start+290 , y_start, "Sum:")
                if entry['t_value']:
                    p.drawString(x_start+360 , y_start, str('TT$'+str(round(entry['t_value'],2))))
                p.drawString(x_start+420 , y_start, str('TT$'+ str( round(entry['t_mrecov'],2))))
                p.drawString(x_start+480 , y_start, str('TT$'+ str( round(entry['t_mnotrecov'],2))))
                p.drawString(x_start+540 , y_start, str('TT$'+ str( round(entry['t_mpaid'],2))))
                p.drawString(x_start+590 , y_start, str('TT$'+ str( round(entry['t_mnotpaid'],2))))
              
                p.setFont("Times-Roman", 10)
                y_start -= row_height
               

        employee_name=employee
       

      
       
       
      

        y_start -= row_height+7
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 60
    results = get_report_synopsis_total_summary_overpayment(date_begin, date_end,location_idform,report_title) 

    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start+85 , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+150 , y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 200, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+200 , y_start, "Grand Total:")
    p.drawString(x_start+360 , y_start, str('TT$'+str(round(results['t_value'],2))))
    p.drawString(x_start+420 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    p.drawString(x_start+480 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    p.drawString(x_start+540 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    p.drawString(x_start+590 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))

    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

def generate_report_synopsis_summary(request):
    date_begin = request.GET.get('date_begin')
    date_end = request.GET.get('date_end')  
    location_idform=request.GET.get('location') 

    if not location_idform:
        location_idform=None    
    
    if not date_begin:        
        date_begin=datetime.datetime.now().strftime('%Y-%m-%d')       
    else:
        date_begin = parse_date(date_begin)
    if not date_end:       
        date_end=datetime.datetime.now().strftime('%Y-%m-%d')    
    else:
        date_end = parse_date(date_end)       
    
    def get_report_synopsis_total_summary_title(start_date, end_date,location):  
           filters = {
                "date__range": (start_date, end_date),              
                "location_id": location,        
                           
                    }            
           filters = {key: value for key, value in filters.items() if value is not None}  
           results = ( Report.objects.filter(**filters) . aggregate(
                                                                     t_value=Sum("value_us"),
                                                                     t_mrecov=Sum("money_recovered"), 
                                                                     t_mnotrecov=Sum("money_not_recovered"),
                                                                     t_mpaid=Sum("money_paid"),
                                                                     t_mnotpaid=Sum("money_not_paid"),
                                                                     reportcount=Count("report_title_id") ) )

           return results
    
    def report_synopsis_title(start_date, end_date, location):  
         filters = {
              "date__range": (start_date, end_date),            
              "location_id": location,  
                    }
      
         filters = {key: value for key, value in filters.items() if value is not None}  
         results = ( Report.objects.filter(**filters) .values( 'report', 'date', 'report_nro', 'report_title_id','origination_id', 'value_us', 'location_id', 
                                                               'report_title_id', 'money_recovered','money_not_recovered','money_paid', 'money_not_paid')
                                                               .order_by('report_nro','report_title_id','date') )

         return results
     
    synopsis_title=report_synopsis_title(date_begin,date_end,location_idform)
        # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report_synopisis_summary.pdf"'    
    # Create a PDF canvas
    page_size = landscape(letter)
    width, height =  page_size
    p = canvas.Canvas(response, page_size)
 #   image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
              
   # full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
   # image = ImageReader(full_path)
        
   # p.drawImage(image, 0, 0, width=width, height=height)
    image_path = "/static/background-crc.jpg"  # Resolve the path to the static file
               
    full_path = os.path.join(settings.BASE_DIR, image_path.strip('/'))  # For absolute paths
    image = ImageReader(full_path)
        
    p.drawImage(image, 100, height-100, width=60, height=70)
    
    # Title
    p.setFont("Times-Bold", 18)
    p.drawString((width/2)-100, height - 50, "Club Royal Caribbean")
    p.drawString((width/2)-150, height - 70, "CCTV Report Synopsis-Summary")   
    p.setFont("Times-Bold", 10)
    p.drawString((width/2)-100, height - 90, "Dates Between "+str(date_begin)+" and "+str(date_end))
   
    # Table Header
    p.setFont("Times-Bold", 11)    
    x_start = 50
    y_start = height - 130
    row_height = 12
    col_width = 50
    
    p.drawString(x_start-20 , y_start, "Report Title")
    p.drawString(x_start+190  , y_start, "Date")
    p.drawString(x_start+160, y_start, "No.")    
    p.drawString(x_start+260 , y_start, "Origination")
    p.drawString(x_start+360 , y_start, "Value")
    p.drawString(x_start+420 , y_start, "Money")
    p.drawString(x_start+420 , y_start-12, "Recovered")
    p.drawString(x_start+480 , y_start, "Money Not")
    p.drawString(x_start+480 , y_start-12, "Recovered")
    p.drawString(x_start+540 , y_start, "Money")  
    p.drawString(x_start+540 , y_start-12, "Paid")  
    p.drawString(x_start+580 , y_start, "Money Not ")
    p.drawString(x_start+590 , y_start-12, "Paid")
    p.drawString(x_start+640 , y_start, "Branch")
    underline_y_below = y_start - 15  # Ligeramente debajo del texto
    p.line(x_start-20 , underline_y_below, x_start + 700, underline_y_below)

# Línea encima del texto
    underline_y_above = y_start + 12  # Ajusta este valor según la altura del texto
    print(underline_y_above)
    p.line(x_start-20, underline_y_above, x_start + 700, underline_y_above)
    y_start-=row_height+12 
    p.setFont("Times-Roman", 10) 
    for record in synopsis_title:
  
        if record['report_title_id']:  
          title=ReportTitle.objects.filter(id=record['report_title_id']).values('title').first()
          p.setFont("Times-Roman", 9)   
          p.drawString(x_start-20  , y_start, title['title'])
          p.setFont("Times-Roman", 10)   
   
        if record['report_nro']:
          p.setFont("Times-Roman", 9)   
          p.drawString(x_start+160  , y_start, str(record['report_nro']))
          p.setFont("Times-Roman", 10)  
        
        if record['date']:
          p.setFont("Times-Roman", 9)   
          p.drawString(x_start+190  , y_start, str(record['date']))
          p.setFont("Times-Roman", 10)               

    
        location=Location.objects.filter(id=record['location_id']).values('location').first()
       
        origination=ReportOrigination.objects.filter(id=record['origination_id']).values('origination').first()           

        if origination:
            p.setFont("Times-Roman", 9)   
            p.drawString(x_start+260 , y_start, origination['origination'])
            p.setFont("Times-Roman", 10)   
        p.drawString(x_start+360 , y_start, str( record['value_us']))
        p.drawString(x_start+420 , y_start, str( record['money_recovered']))
        p.drawString(x_start+480 , y_start, str( record['money_not_recovered']))
        p.drawString(x_start+540 , y_start, str( record['money_paid']))
        p.drawString(x_start+590 , y_start, str( record['money_not_paid']))  
    
           
        if location:
            p.drawString(x_start+640 ,y_start,str(location['location']))    
      

        y_start -= row_height
        if y_start < 80:  # Check if space is running out
          p.setFont("Times-Roman", 10)
          p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
          page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
          p.drawRightString(260 * mm, 10 * mm, page_number_text)
          # Finalize the PDF
          p.showPage()  # Add a new page
    
          y_start=height - 40
    results = get_report_synopsis_total_summary_title(date_begin, date_end,location_idform) 


    y_start-=row_height+5
    p.setFont("Times-Bold", 9)
    p.drawString(x_start+90 , y_start, "Sum of Report:")
    p.setFillColor(red)
    p.drawString(x_start+160, y_start, str(round(results['reportcount'],2)))
    p.setFillColorRGB(0, 0, 0)  
    underline_y = y_start - 2  # Slightly below the text
    p.line(x_start + 250, underline_y, x_start + 630, underline_y)
    p.drawString(x_start+250 , y_start, "Grand Total:")
    if results['t_value'] is not None:
        p.drawString(x_start+350 , y_start, str('TT$'+str(round(results['t_value'],2))))
    if results['t_mrecov'] is not None:
        p.drawString(x_start+410 , y_start, str('TT$'+ str( round(results['t_mrecov'],2))))
    if results['t_mnotrecov'] is not None:
        p.drawString(x_start+470 , y_start, str('TT$'+ str( round(results['t_mnotrecov'],2))))
    if results['t_mpaid'] is not None:
        p.drawString(x_start+530 , y_start, str('TT$'+ str( round(results['t_mpaid'],2))))
    if results['t_mnotpaid'] is not None:
        p.drawString(x_start+580 , y_start, str('TT$'+ str( round(results['t_mnotpaid'],2))))
       
    p.setFont("Times-Roman", 10)
    p.drawString(50, 30, "This report has been generated automatically by CRC@Surveillance System")
    page_number_text = f"Page {p.getPageNumber()}"
          # Set the position of the page number
    p.drawRightString(260 * mm, 10 * mm, page_number_text)
       # first_time=False  
    p.save()
    return response

