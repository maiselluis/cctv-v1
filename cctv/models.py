from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User,Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
import datetime
import os




# Create your models here.

def validate_decimals(value):
    try:
        return round(float(value), 2)
    except:
        raise ValidationError(
            _('%(value)s is not an integer or a float  number'),
            params={'value': value},
        )

def video_upload_to(instance, filename):
    branch=Location.objects.get(id=instance.report.location_id)
    branch_name=branch.location
    report_nro = 'Report #'+ ''+ str(instance.report.report_nro)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
   
   # return os.path.join('videos/', f'{timestamp}_{filename}')
    folder_path = os.path.join('videos',branch_name, report_nro, f'{timestamp}_{filename}')
    return folder_path

def supplies_upload_to(instance, filename):
    branch=Location.objects.get(id=instance.branch.id)
    branch_name=branch.location
    supplies_forms='supplies_forms'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')

    folder_path = os.path.join('images',branch_name, supplies_forms, f'{timestamp}_{filename}')
    return folder_path 
class Location(models.Model):
    id = models.BigAutoField(primary_key=True)
    location = models.TextField(max_length=255,verbose_name='Location')

    def __str__(self):
        return self.location
    

    class Meta:
        ordering = ['id']
        verbose_name = "Branch"
        verbose_name_plural = "Branchs"
        db_table="tb_location"
        get_latest_by ="id"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['location']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profile"
        db_table="tb_userprofile"
        get_latest_by ="location"

class Main(models.Model):
  id = models.BigAutoField(primary_key=True)
  date=models.DateField(verbose_name='Date')
  location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_main',verbose_name='Location')
  usd_rate=models.FloatField(verbose_name='USD Rate',default=7.5)
  euro_rate=models.FloatField(verbose_name='EURO Rate',default=8.5)
  gbp_rate=models.FloatField(verbose_name='GBP Rate',validators=[validate_decimals],default=8.5)
  casino_open=models.TimeField(verbose_name='Opening')
  casino_close=models.TimeField(verbose_name='Close')  
  detail=models.TextField(verbose_name='Notes',null=True, blank=True)
  

  class Meta:
       unique_together = (('date','location'),)
       ordering = ['date','location']
       verbose_name = "Main"
       verbose_name_plural = "Main"
       db_table='tb_main'
       get_latest_by ='date'

class ReportType(models.Model):
    id=models.AutoField(primary_key=True)
    report_type=models.TextField(max_length=255,verbose_name='Report Type')

    def __str__(self):
        return self.report_type
    
    class Meta:
      ordering = ['id']
      verbose_name = "Report Type"
      verbose_name_plural = "Report Types"
      db_table='tb_report_type'
      get_latest_by ='id'

class ReportTitle(models.Model):
    id=models.BigAutoField(primary_key=True)
    type_report=models.ForeignKey("ReportType",on_delete=models.CASCADE,verbose_name='Report Type', related_name='fk_report_title')
    title=models.TextField( max_length=255, verbose_name='Report')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['type_report']
        verbose_name = "Report Title"
        verbose_name_plural = "Reports Titles"
        db_table='tb_report_title'
        get_latest_by ='id'

class Area(models.Model):
    id=models.BigAutoField(primary_key=True)
    area=models.CharField(max_length=50)

    def __str__(self):
        return self.area
    
    class Meta:
       ordering = ['id']
       verbose_name = "Casino Location"
       verbose_name_plural = "Casino Locations"
       db_table='tb_area'
       get_latest_by ='id'

class Token(models.Model):
 id =models.AutoField(primary_key=True)
 token=models.TextField(max_length=255, verbose_name='Token')

 def __str__(self):
     return self.token
 
 class Meta:
      ordering = ['id']
      verbose_name = "Token"
      verbose_name_plural = "Tokens"
      db_table='tb_token'
      get_latest_by ='id'
      
class ReportOrigination(models.Model):
    id=models.AutoField(primary_key=True)
    origination=models.TextField(max_length=255,verbose_name='Origination')

    def __str__(self):
        return self.origination

    class Meta:
       ordering = ['id']
       verbose_name = "Report Origination"
       verbose_name_plural = "Report Originations"
       db_table='tb_report_origination'
       get_latest_by ='id'
   
     
class Report(models.Model):
     report=models.BigAutoField(primary_key=True,verbose_name='Report')     
     date=models.DateField(verbose_name='Date',blank=False,null=False)
     location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_report',verbose_name='Location',blank=False,null=False)
     time=models.TimeField(verbose_name='Time',blank=False,null=False)
     report_title=models.ForeignKey( "ReportTitle", on_delete=models.PROTECT,verbose_name='Report Title',related_name='fk_report_title_report',blank=False,null=False)
     area=models.ForeignKey("Area", on_delete=models.PROTECT,verbose_name='Area', related_name='fk_area',blank=False,null=False)
     duty_manager=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name='Duty Manager',related_name='fk_duty_manager',blank=True,null=True)
    
     pittboss=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name='Pit Boss',related_name='fk_pitboss',blank=True,null=True)
    
     inspector=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name='Inspector',related_name='fk_inspector',blank=True,null=True)
    
     dealer = models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name='Inspector',related_name='fk_dealer',blank=True,null=True)
    
     other = models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name='Other',related_name='fk_other',blank=True,null=True)
    
     detail=models.TextField(max_length=255,verbose_name='Detail',blank=True,null=True)
     action_token=models.TextField(max_length=255,verbose_name='Action Taken',blank=True,null=True)
     value_us=models.FloatField(verbose_name='Values',blank=True,null=True)
     winning=models.IntegerField(verbose_name='Winning Numbers',null=True,blank=True)
     box=models.IntegerField(verbose_name='Box',null=True,blank=True)
     money_recovered=models.FloatField(verbose_name='Money Recovered',null=True,blank=True)
     money_not_recovered=models.FloatField(verbose_name='Money Not Recovered',null=True,blank=True)
     money_paid=models.FloatField(verbose_name='Money Payd',null=True,blank=True)
     money_not_paid=models.FloatField(verbose_name='Money Not Payd',null=True,blank=True)
     dubbed_to=models.BooleanField(default=False,verbose_name='Footage',null=True,blank=True)
     origination=models.ForeignKey("ReportOrigination", on_delete=models.PROTECT,verbose_name='Report Origination', related_name='fk_origination',blank=True,null=True)
     report_type=models.ForeignKey('ReportType', on_delete=models.PROTECT, verbose_name='Report Type', related_name='fk_report_type',blank=True,null=True)
     cctv_id=models.ForeignKey("Staff", on_delete=models.PROTECT,verbose_name='Cctc Id',related_name='fk_cctv_Staff',blank=True,null=True)
     customer=models.ForeignKey("Customer",on_delete=models.PROTECT,verbose_name='Customer',related_name="fk_customer_report",blank=True,null=True)
     usd_rate=models.FloatField(verbose_name='USD Rate',default=7.5,blank=True,null=True)
     euro_rate=models.FloatField(verbose_name='EURO Rate',default=8.5,blank=True,null=True)
     gbp_rate=models.FloatField(verbose_name='GBP Rate',default=8.5,blank=True,null=True)  
     report_nro=models.IntegerField(verbose_name='Report #',null=False,blank=False)

     def __str__(self):
         return f"Report {self.report_nro}"
     
     class Meta:
       unique_together = (('date','location','time','report',),)
       ordering = ['report']
       verbose_name = "Report"
       verbose_name_plural = "Reports"
       db_table='tb_report'
       get_latest_by ='-report'

     def save(self, *args, **kwargs):
        # Reemplaza valores nulos o vacíos con 0
        for field in ['money_recovered', 'money_not_recovered','money_paid','money_not_paid','value_us']:
            if getattr(self, field) in [None, '']:
                setattr(self, field, 0)
        
        super().save(*args, **kwargs)
    
     def get_absolute_url(self):
         return reverse('report-detail',args=[str(self.report)])
     
     def get_edit_url(self):
         return reverse('report-update',args=[str(self.report)])
   
     def get_delete_url(self):
         return reverse('report-delete',args=[str(self.report)])
     
     def get_report_video(self):
         return reverse('reportvideo_list',args=[str(self.report)])

class ReportVideo(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="videos")
    video_file = models.FileField(upload_to=video_upload_to, blank=True, null=True)  
    caption = models.CharField(max_length=250)

    def __str__(self):
       return f"Video for {self.report}: {self.video_url or self.video_file.name}"
   
    class Meta:
       ordering = ['report']
       verbose_name = "Videos"
       verbose_name_plural = "Videos"
       db_table='tb_videos'
       get_latest_by ='-report'

class DailyShift(models.Model):
   id=models.AutoField(primary_key=True)
   date=models.DateField(verbose_name='Date')
   location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_daily',verbose_name='Location')
   shift=models.ForeignKey("Shift", on_delete=models.PROTECT,verbose_name='Shift', related_name='fk_shift')
   supervisor=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='supervisor', related_name='fk_supervisor',null=True,blank=True)
   officer1=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='officer1', related_name='fk_officer1',null=True,blank=True)
   officer2=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='officer2', related_name='fk_officer2',null=True,blank=True)
   usd_rate=models.FloatField(verbose_name='USD Rate',default=7.5)
   euro_rate=models.FloatField(verbose_name='EURO Rate',default=8.5)
   gbp_rate=models.FloatField(verbose_name='GBP Rate',validators=[validate_decimals],default=8.5)
   casino_open=models.TimeField(verbose_name='Opening',default='10:00:00')
   casino_close=models.TimeField(verbose_name='Close',default='04:00:00')  
   detail=models.TextField(verbose_name='Notes',null=True, blank=True)
   message_book=models.TextField(verbose_name='Message')
   
   def __str__(self):
       return  f"Shift {self.shift}"
   
   class Meta:
   # unique_together = (('date','location','shift'),)
    ordering = ['id','date','location','shift']
    verbose_name = "Daily Shift"
    verbose_name_plural = "Daily Shifts"
    db_table='tb_daily_shift'
    get_latest_by ='id'

   def get_absolute_url(self):
        return reverse('daily_shift-detail', args=[str(self.id)])
    
   def get_edit_url(self):
        return reverse('daily_shift-update', args=[str(self.id)])
    
   def get_delete_url(self):
        return reverse('daily_shift-delete', args=[str(self.id)])
  
class Cash_Desk_Transaction(models.Model):
   transactions=models.BigAutoField(primary_key=True,verbose_name='Transaction' )  
   location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_cash_transaction',verbose_name='Location')
   date=models.DateField(verbose_name='Date')
   time=models.TimeField(verbose_name='Time')   
   area_cashier=models.ForeignKey("AreaCashier",on_delete=models.PROTECT,verbose_name='Area Cashier',related_name='fk_area_cashier_transaction')   
   account_type=models.ForeignKey("AccountType", on_delete=models.PROTECT,verbose_name='Account Type',related_name='fk_account_type')
   customer=models.ForeignKey("Customer",on_delete=models.PROTECT,verbose_name='Customer',related_name='fk_customer',null=True,blank=True)
   token=models.ForeignKey("Token", on_delete=models.PROTECT,verbose_name='Token', related_name='fk_token',null=True,blank=True)
   tt_dolar=models.FloatField(verbose_name='TT Dolar',null=True,blank=True,default=0, )
   usd_dolar=models.FloatField(verbose_name='USD Dolar',null=True,blank=True,default=0, )
   euro_dolar=models.FloatField(verbose_name='EURO Dolar',null=True,blank=True,default=0, )
   gbp_dolar=models.FloatField(verbose_name='GBP Dolar',null=True,blank=True,default=0, )
   cad_dolar=models.FloatField(verbose_name='CAD Dolar',null=True,blank=True,default=0, )
   employee=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name="Employee", related_name='fk_employee',null=True,blank=True)
   autorized_by=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name="Autorized by", related_name='fk_autorized',null=True,blank=True)
   machine_no=models.ForeignKey('Slot_Machine',on_delete=models.PROTECT, verbose_name='Machine Slot', related_name='fk_machine_transaction',blank=True,null=True)
   detail=models.TextField(max_length=255,verbose_name='Detail',null=True,blank=True)
  
   def __str__(self):
       return f"Transaction {self.transactions}"
   
   class Meta:
    
    ordering = ['-transactions','date','time','location']
    verbose_name = "Cash Desk Tansactions"
    verbose_name_plural = "Cash Desk Transactions"
    db_table='tb_cash_desk_transactions'
    get_latest_by ='-transactions'

   def save(self, *args, **kwargs):
        # Reemplaza valores nulos o vacíos con 0
        for field in ['tt_dolar', 'usd_dolar','euro_dolar','gbp_dolar','cad_dolar']:
            if getattr(self, field) in [None, '']:
                setattr(self, field, 0)
        
        super().save(*args, **kwargs)
    
  # def formatted_fecha(self):
    #    return self.fecha.strftime("%d-%m-%Y")

class Slot_Machine(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='Id machine')
    name=models.IntegerField(verbose_name='Machine No.')

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
         ordering = ['id']
         verbose_name = "Slot Machine"
         verbose_name_plural = "Slot Machine"
         db_table='tb_slot_machine'
         get_latest_by ='-id'

class Cash_Desk_Error(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='Cash Desk Error')
    location=models.ForeignKey('Location',on_delete=models.PROTECT,verbose_name='Branh',related_name='fk_branch_cd_error',default=1)
    date=models.DateField(verbose_name='Date',default=timezone.now)
    time=models.TimeField(verbose_name='Time',default='06:00:00') 
    area_cashier=models.ForeignKey("AreaCashier",on_delete=models.PROTECT,verbose_name='Area Cashier',related_name='fk_area_cashier_cderror',default=1) 
    error_type=models.ForeignKey('CDErrorType',on_delete=models.PROTECT,verbose_name='CD Error Type',related_name='error_type_cash_desk_error',default=1)
    duty_manager=models.ForeignKey('Staff',on_delete=models.PROTECT,verbose_name='Duty Manager', related_name='fk_duty_manager_dalily_cash_desk_error',default=1)
    tt=models.FloatField(verbose_name='TTD',default=1)
    usd=models.FloatField(verbose_name='USD',default=1)
    euro=models.FloatField(verbose_name='EURO',default=1)
    cashier=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='Cashier', related_name='fk_cashier_cash_desk_error',default=1)
    supervisor=models.ForeignKey('Staff',on_delete=models.PROTECT,verbose_name='Supervisor/Senior',related_name='fk_supervisor_cash_desk_error',default=1)
    report=models.IntegerField(verbose_name='Report Nr.',blank=True,null=True)
    found=models.BooleanField(default=False)
    

    def __str__(self):
       return  f"Cash Desk Error {self.id}"

    class Meta:
         ordering = ['id']
         verbose_name = "Cash Desk Error"
         verbose_name_plural = "Cash Desk Errors"
         db_table='tb_cash_desk_error'
         get_latest_by ='-id'
        
    def save(self, *args, **kwargs):
        # Reemplaza valores nulos o vacíos con 0
        for field in ['tt', 'usd','euro']:
            if getattr(self, field) in [None, '']:
                setattr(self, field, 0)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return  reverse('cash_desk_error-detail',args=[ str(self.id)])
    def get_edit_url(self):
        return reverse('cash_desk_error-update',args=[str(self.id)])
    def get_delete_url(self):
       return reverse('cash_desk_error-delete',args=[str(self.id)])

class Poker_Payout(models.Model):
    id = models.AutoField(primary_key=True)
    location=models.ForeignKey('Location',on_delete=models.PROTECT,verbose_name='Branh',related_name='fk_poker_error',default=1)
    date=models.DateField(verbose_name='Date',default=timezone.now)
    time=models.TimeField(verbose_name='Time',default='06:00:00') 
    table=models.ForeignKey('PokerTable',on_delete=models.PROTECT,verbose_name='Poker Table',related_name='fk_poker_table',default=1)
    combination=models.ForeignKey('PokerCombination', on_delete=models.PROTECT,verbose_name='Combination',related_name='fk_poquer_combination', default=1)
    bet=models.FloatField(verbose_name='Bet')
    payout=models.FloatField(verbose_name='Payout')
    customer=models.ForeignKey('Customer', on_delete=models.PROTECT,verbose_name='Customer',related_name='fk_poker_payout')
    dealer=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='Dealer',related_name='fk_dealer_poker')
    inspector=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='Inspector',related_name='fk_inspector_poker')
    pitboss=models.ForeignKey('Staff', on_delete=models.PROTECT,verbose_name='Customer',related_name='fk_pitboos_poker')
    
    def __str__(self):
        return f"Payout {self.id}"


    class Meta:
         ordering = ['id']
         verbose_name = "Poker Payout"
         verbose_name_plural = "Poker Payouts"
         db_table='tb_poker_payout'
         get_latest_by ='-id'
    
    
    def save(self, *args, **kwargs):
        # Reemplaza valores nulos o vacíos con 0
        for field in ['bet', 'payout']:
            if getattr(self, field) in [None, '']:
                setattr(self, field, 0)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return  reverse('poker_payouts-detail',args=[ str(self.id)])
    def get_edit_url(self):
        return reverse('poker_payouts-update',args=[str(self.id)])
    def get_delete_url(self):
       return reverse('poker_payouts-delete',args=[str(self.id)])
 
class DailyExeption(models.Model):
   id=models.BigAutoField(primary_key=True)
   date=models.DateField(verbose_name='Date')
   location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_daily_exception',verbose_name='Location')
   employee=models.ForeignKey('Staff',on_delete=models.PROTECT,verbose_name='Employeee',related_name='employee_daily_exception')
   exception_type=models.ForeignKey("ExceptionType", on_delete=models.PROTECT,verbose_name='Exeption Type',related_name='fk_daily_exception')
   daily_from=models.TimeField(verbose_name='From',null=True,blank=True)
   daily_to=models.TimeField(verbose_name='To',null=True,blank=True)
   total_hours=models.DecimalField(max_digits=5, decimal_places=2, editable=False)
   old_shift=models.TimeField(verbose_name='Old Shift',null=True,blank=True)
   new_shift=models.TimeField(verbose_name='New Shift',null=True,blank=True)
   detail=models.TextField(max_length=255,verbose_name='Detail')
   

   def __str__(self):
    return f"{self.id}"

   class Meta:        
        ordering = ['id','date','location']
        verbose_name = "Daily Exeption"
        verbose_name_plural = "Daily Exeptions"
        db_table='tb_daily_exeption'
        get_latest_by ='id'
    
  
   def save(self, *args, **kwargs):
        if self.daily_to and self.daily_from:
            # Combine times with a reference date
            daily_from_dt = datetime.datetime.combine(datetime.datetime.min, self.daily_from)
            daily_to_dt = datetime.datetime.combine(datetime.datetime.min, self.daily_to)

            # Handle cases where `daily_to` is earlier than `daily_from` (crosses midnight)
            if daily_to_dt <= daily_from_dt:
                daily_to_dt += timedelta(days=1)

            # Calculate time difference
            time_difference = daily_to_dt - daily_from_dt

            # Calculate total hours based on exception type
            if self.exception_type.id == 13:
                self.total_hours = (time_difference.total_seconds() / 3600) -8
            else:
              #  self.total_hours = time_difference.total_seconds() / 3600
                self.total_hours = 0 
        else:
            self.total_hours = 0 
        

       
        super().save(*args, **kwargs)
    
   def get_absolute_url(self):
        return reverse('daily_exeption-detail',args=[str(self.id)])
   
   def get_edit_url(self):
       return reverse('daily_exeption-update',args=[str(self.id)])
 
   def get_delete_url(self):
       return reverse('daily_exeption-delete',args=[(str(self.id))])
 
   
class Department(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField(max_length=255,verbose_name='Department')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        db_table='tb_department'
        get_latest_by ='id'

class Position(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, help_text='Position',verbose_name='Position')
    department = models.ForeignKey(Department,related_name='fk_position_department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('department', 'id')
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        db_table="tb_position"
        get_latest_by ='id'

class Staff(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    surname = models.CharField(max_length=50, blank=False, null=False)
    photo = models.ImageField(upload_to='images/', default='images/noimage.jpg')
    department = models.ForeignKey(Department, related_name='position_department', on_delete=models.PROTECT)
    position = models.ForeignKey(Position, related_name='position_position', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    location=models.ForeignKey("Location",verbose_name=("location"), on_delete=models.PROTECT)
    
    def __str__(self):
        return f'{self.name}  {self.surname}'

    class Meta:
        
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"
        db_table="tb_staff"
        get_latest_by ='-id'
    
    def get_absolute_url(self):
        return reverse('staff-detail', args=[str(self.id)])
    
    def get_edit_url(self):
        return reverse('staff-update', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('staff-delete', args=[str(self.id)])
 
class Sex(models.Model):
    id=models.BigAutoField(primary_key=True)
    sex=models.CharField(max_length=10, verbose_name='Sex')

    def __str__(self):
        return self.sex
    
    class Meta:
        ordering =["id"]
        verbose_name = "Sex"
        verbose_name_plural = "Sex"
        db_table="tb_sex"
        get_latest_by = "-id"

class BlackList(models.Model):
    id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    surname =models.CharField(max_length=50)
    blacklistby = models.ForeignKey("Staff",  verbose_name=('blacklistby'), on_delete=models.PROTECT,related_name='blacklistby')
    date = models.DateField()
    details= models.TextField()
    picture = models.ImageField(upload_to='images/', default='images/noimage.jpg')   
    sex= models.ForeignKey("Sex", verbose_name=("sex"),on_delete=models.PROTECT,default='1')    
    reason =models.ForeignKey("Reason",verbose_name=("reason"),on_delete=models.PROTECT)
    race =models.ForeignKey("Race",verbose_name=("race"),on_delete=models.PROTECT)
    duration =models.ForeignKey("Duration",verbose_name=("duration"),on_delete=models.PROTECT)
    location=models.ForeignKey("Location",verbose_name=("location"), on_delete=models.PROTECT, default=1)
    notified=models.BooleanField(default=False)
    
    
    def __str__(self):
       return f'{self.name}  {self.surname}'

    class Meta:
        ordering =["-date"]
        verbose_name = "Costumer in Black List"
        verbose_name_plural = "Costumers in Black List"
        db_table="tb_blacklist"
        get_latest_by = "-date"
    
    def get_absolute_url(self):
        return reverse('blacklist-detail', args=[str(self.id)])
    
    def get_edit_url(self):
        return reverse('blacklist-update', args=[str(self.id)])
    
    def get_pdf_url(self):
        return reverse('blacklist_pdf', args=[str(self.id)])

    def get_absolute_reinstated_url(self):
        return reverse('blacklist-detail-reinstated', args=[str(self.id)])
    
        
    def get_edit_reinstated_url(self):
        return reverse('blacklist-update-reinstated', args=[str(self.id)])

class Counterfait(models.Model):
   id=models.BigAutoField(primary_key=True,verbose_name='Nro.')
   date=models.DateField()   
   location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_counterfait',verbose_name='Location')
   area_cashier=models.ForeignKey("AreaCashier", on_delete=models.PROTECT,related_name='fk_counterfeit_area_cashier',verbose_name='Area Cashier')
   usd_dolar=models.FloatField(verbose_name='USD Dolar',)
   tt_dolar=models.FloatField(verbose_name='TTL Dolar', )
   euro_dolar=models.FloatField(verbose_name='EURO Dolar',)
   gbp_dolar=models.FloatField(verbose_name='GBP Dolar', )
   serial_number=models.TextField(max_length=11)
   report_nro=models.IntegerField(null=False,blank=False,verbose_name='Report #')
   notes=models.TextField(max_length=255,verbose_name='Detail')
   employee=models.ForeignKey("Staff",on_delete=models.PROTECT,verbose_name="Cashier", related_name='fk_employee_counterfeit',null=True,blank=True)
   customer=models.ForeignKey("Customer",on_delete=models.PROTECT,verbose_name='Customer',related_name="fk_customer_counterfeit",blank=True,null=True)

  
   class Meta:   
    ordering = ['id','date','location']
    verbose_name = "Counterfait"
    verbose_name_plural = "Counterfait"
    db_table='tb_counterfait'
    get_latest_by ='-id'

    def __str__(self):
        return f"{self.id}"


   def save(self, *args, **kwargs):
        # Reemplaza valores nulos o vacíos con 0
        for field in ['usd_dolar', 'tt_dolar','euro_dolar','gbp_dolar']:
            if getattr(self, field) in [None, '']:
                setattr(self, field, 0)
        
        super().save(*args, **kwargs)

   def get_absolute_url(self):
       return reverse('counterfeit-detail', args=[str(self.id)])
   
   def get_edit_url(self):
       return reverse('counterfeit-update', args=[str(self.id)])
   
   def get_delete_url(self):
       return reverse('counterfeit-delete', args=[str(self.id)])

class Shift(models.Model):
   id=models.AutoField(primary_key=True)
   shift=models.TextField(max_length=50)

   def __str__(self):
       return f"{self.shift}"
   
   class Meta:
     ordering = ["-id"]
     verbose_name_plural = "Shifts"
     verbose_name = "Shift"
     db_table="tb_shift"
   
class PokerCombination(models.Model):
   id=models.AutoField(primary_key=True)
   poker_combination=models.TextField(max_length=255, verbose_name='Poker Combination')

   def __str__(self):
         return f"{self.poker_combination}"
   
   class Meta:
        ordering = ["id"]
        verbose_name_plural = "Poker Combination"
        verbose_name = "Poker Combination"
        db_table="tb_poker_combination"
        get_latest_by = "id"
    
class PokerTable(models.Model):
   id=models.AutoField(primary_key=True)
   poker_table=models.TextField(max_length=255, verbose_name='Poker Table')

   def __str__(self):
         return f"{self.poker_table}"
   
   class Meta:
        ordering = ["id"]
        verbose_name_plural = "Poker Table"
        verbose_name = "Poker Table"
        db_table="tb_poker_table"
        get_latest_by = "id"
   
class Duration(models.Model):
    id = models.AutoField( primary_key=True)
    duration =models.CharField(max_length=50)
    
    
    def __str__(self):
        return f"{self.duration}"

    class Meta:
        ordering =["id"]
        verbose_name = "Duration"
        verbose_name_plural = "Durations"
        db_table="tb_duration"

class Customer(models.Model):
    id=models.BigAutoField(primary_key=True)
    location=models.ForeignKey("Location",on_delete=models.PROTECT,related_name='fk_location_customer',verbose_name='Branch',default=1)
    customer=models.TextField(max_length=255, verbose_name='Customers')  
    photo = models.ImageField(upload_to='images/', default='images/noimage.jpg')  
    
    def __str__(self):
        return f"{self.customer}"
    
    class Meta:
        ordering = ["customer"]
        verbose_name_plural = "Customers"
        verbose_name = "Customers"
        db_table="tb_customer"
    
    def get_absolute_url(self):
        return reverse('customer-detail', args=[str(self.id)])
    
    def get_edit_url(self):
        return reverse('customer-update', args=[str(self.id)])
    
    def get_delete_url(self):
        return reverse('customer-delete', args=[str(self.id)])

class Race(models.Model):

    id = models.AutoField( primary_key=True)
    race =models.CharField(max_length=30)

    class Meta:
        ordering =["id"]
        verbose_name_plural = "Races"
        verbose_name = "Race"
        db_table="tb_race"
    

    def __str__(self):
        return f"{self.race}"

class Reason(models.Model):
    id = models.AutoField( primary_key=True)
    reason =models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.reason}"
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Reasons"
        verbose_name = "Reason"
        db_table="tb_reason"
        get_latest_by = "id"

class AreaCashier(models.Model):
   id = models.BigAutoField(primary_key=True)
   area_cashier=models.TextField(max_length=255,verbose_name='Area Cashier')

   def __str__(self):
       return self.area_cashier
   
   class Meta:
       db_table='tb_area_cashier'      
       ordering = ["id"]
       verbose_name = "Cashier Location"
       verbose_name_plural = "Cashiers Location"
       get_latest_by = "id"
     
class AccountType(models.Model):
    id=models.BigAutoField(primary_key=True)
    account_type=models.TextField(max_length=255,verbose_name='Account Type')

    def __str__(self):
        return f"{self.account_type}"
    
    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Accounts Type"
        verbose_name = "Account Type"
        db_table="tb_account_type"
        get_latest_by = "id"
   
class ExceptionType(models.Model):
   id = models.BigAutoField(primary_key=True)
   exeption_type=models.TextField(max_length=255,verbose_name='Cash Desk Exeption Type')

   def __str__(self):
       return f"{self.exeption_type}"
   
   class Meta:
       db_table='tb_cd_exeption_type'
       ordering = ["id"]
       verbose_name = "Daily Exeption Type"
       verbose_name_plural = "Daily Exeption Types"
       get_latest_by = "id"

class CDErrorType(models.Model):
   id = models.BigAutoField(primary_key=True)
   error_type=models.TextField(max_length=255,verbose_name='Cash Desk Error Type')

   def __str__(self):
       return f"{self.error_type}"
   
   class Meta:
       db_table='tb_cd_error_type'
       ordering = ["id"]
       verbose_name = "Cash Desk Error Type"
       verbose_name_plural = "Cash Desk Errors Types"
       get_latest_by = "id"
    

class Supplies(models.Model):
    request_choices=[ ('supplies','SUPPLIES'),('equipment','EQUIPMENT'),('service','SERVICE'),('other','OTHER') ]

    id=models.BigAutoField(primary_key=True,verbose_name='Nro.')
    date=models.DateField(default=timezone.now) 
    branch=models.ForeignKey(Location,related_name='fk_supplies_branch',on_delete=models.PROTECT,verbose_name='Branch')  
    department=models.ForeignKey("Department",related_name="fk_supplies",on_delete=models.PROTECT,verbose_name='Department')
    prepared_by=models.ForeignKey("Staff",related_name="fk_staff_supplies",on_delete=models.PROTECT,verbose_name='Prepared by')
    approved_by=models.ForeignKey("Staff",related_name="fk_staff_approved",on_delete=models.PROTECT,verbose_name='Approved by')
    request_for = models.CharField(max_length=20, choices=request_choices, default='supplies')
    description=models.TextField(max_length=255,verbose_name='Detail',null=True,blank=True)
    picture=models.ImageField(upload_to=supplies_upload_to, blank=True,null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name_plural = "Supplies"
        verbose_name = "Supplies"
        db_table="tb_supplies"
        get_latest_by = "-id"

    def __str__(self):
        return f"Supplies #{self.id}"

class Notification(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE,verbose_name='Branch' , related_name="notifications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
  

    class Meta:
        db_table="tb_notification"
        unique_together = ('location','user' )
        ordering = ["-location"]  

    def __str__(self):
        return f"{self.user.username} - {self.location.location}"
    
class UserLocation(models.Model):
    ip = models.GenericIPAddressField()
    user = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        db_table="tb_user_location"       
        ordering = ["-user"]  

    def __str__(self):
        return f"{self.user} - {self.ip}- {self.city}"
    


class UserActionLog(models.Model):
    ACTION_CHOICES = (
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('VIEW', 'View'),
    )
    class Meta:
        db_table = 'tb_user_action_log'
        ordering = ['-timestamp']
        verbose_name = "User Action Log"           

    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_actions')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    url = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.url}"