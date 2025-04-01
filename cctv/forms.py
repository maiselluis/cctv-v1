from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django import template
from django.db.models import Q


#Login

def get_customers_by_location(location_id): 
         if location_id:
               customer= Customer.objects.filter(
                  location_id=location_id,
                  fk_customer__isnull=False  # Asegura que haya transacciones relacionadas
            ).distinct()
         else:
                customer= Customer.objects.filter(                 
                  fk_customer__isnull=False  # Asegura que haya transacciones relacionadas
            ).distinct()
                         
        
       
         return customer


def get_customers_by_location_poker_payout(location_id): 
         if location_id:
               customer= Customer.objects.filter(
                  location_id=location_id,
                  fk_poker_payout__isnull=False  
            ).distinct()
         else:
                customer= Customer.objects.filter(                 
                  fk_poker_payout__isnull=False  
            ).distinct()
                         
        
       
         return customer

class LoginForm(AuthenticationForm):
    username = forms.CharField(
          label='Username', 
          max_length=100,
          widget=forms.TextInput( 
           attrs={'placeholder': 'Username', 'class': 'form-control'}
               ))
    
    password = forms.CharField(
          label='Password',
          widget=forms.PasswordInput(                 
           attrs={'placeholder': 'Password', 'class': 'form-control'}
               ))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Remember Me")

    class Meta:
            fields = ['username', 'password', 'remember_me']

#User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

#UserProfile
class CreateUserProfileForm(ModelForm):
      user=  forms.ModelChoiceField(
             queryset=User.objects.all(), 
             widget=forms.Select(
              attrs={'class': 'form-select'}
                    ))

      location=  forms.ModelChoiceField(
             queryset=Location.objects.all(), 
             widget=forms.Select(
              attrs={'class': 'form-select'}
                    ))
      class Meta:
            model=UserProfile
            fields=['user','location']  
#Permission

class AddPermissionForm(forms.Form):
    permission = forms.ModelChoiceField(queryset=Permission.objects.all(), label="Select Permission")
#Main
class CreateMainForm(ModelForm):
      date = forms.DateField(
            widget=forms.DateInput(
                 format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
            )
      )
     
      
      usd_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'USD Rate', 'min': '0','class': 'form-control'}
               ))
      
      euro_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'EURO Rate',  'min': '0','class': 'form-control'}
               ))

      gbp_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'GBP Rate','min': '0', 'class': 'form-control'}
    ))

      location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
     ))
      
      casino_open=forms.TimeField(
            widget=forms.TimeInput(
                  format='%H:%M',                  
              attrs={'class':'form-control','type': 'time',}    
            )
      )
      casino_close=forms.TimeField(
            widget=forms.TimeInput(format='%H:%M', attrs={'class':'form-control','type': 'time'} )

            )
       
     

      class Meta:
           model=Main
           fields=['date','location','usd_rate','euro_rate','gbp_rate','casino_open','casino_close']

#Token form
class CreateTokenForm(forms.ModelForm):
      token=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter token'
                         }
            )

      )
      class Meta:
            model=Token
            fields=['token']    

#Report Type Form
class CreateReportTypeForm(forms.ModelForm):
      report_type=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter report type'
                         }
            )

      )
      class Meta:
            model=ReportType
            fields=['report_type'] 

#Customer
class CreateCustomerForm(forms.ModelForm):
    #  location = forms.ModelChoiceField(
     #   queryset=Location.objects.all(), 
    #    widget=forms.Select(
  #          attrs={'class': 'form-select'}
  #   ))
      customer=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter customer'
                         }
            )

      )
      photo=forms.ImageField(
            required=False,
             widget=forms.ClearableFileInput(
                  attrs={'class': 'form-control-file','accept': 'image/*',  }

             )

      )
      class Meta:
            model=Customer
            fields=['customer','photo']  

#Area
class CreateCasinoAreaForm(forms.ModelForm):
      area=forms.CharField(
            label='Casino Location',
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter casino location'
                         }
            )

      )
      class Meta:
            model=Area
            fields=['area']  
#Cashier Area
class CreateCashierAreaForm(forms.ModelForm):
      area_cashier=forms.CharField(
            label='Cashier Location',
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter cashier location'
                         }
            )

      )
      class Meta:
            model=AreaCashier
            fields=['area_cashier']  

#Report Origination
class CreateReportOriginationForm(forms.ModelForm):
      origination=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter report origination'
                         }
            )

      )
      class Meta:
            model=ReportOrigination
            fields=['origination']   
#Report Title
class CreateReportTitleForm(forms.ModelForm):
      type_report=  forms.ModelChoiceField(
             queryset=ReportType.objects.all(), 
             widget=forms.Select(
              attrs={'class': 'form-select'}
                    ))

      title=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter report title'
                         }
            )

      )
      class Meta:
            model=ReportTitle
            fields=['type_report','title']  
            
#AccountType
class CreateAccountTypeForm(ModelForm):
    
      account_type=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter account type'
                         }
            )

      )
      class Meta:
            model=AccountType
            fields=['account_type']  
#Shift
class CreateShiftForm(ModelForm):
    
      shift=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter shift'
                         }
            )

      )
      class Meta:
            model=Shift
            fields=['shift'] 

#Location
class CreateLocationForm(ModelForm):
    
      location=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter location'
                         }
            )

      )
      class Meta:
            model=Location
            fields=['location'] 

#Sex
class CreateSexForm(ModelForm):
    
      sex=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter sex'
                         }
            )

      )
      class Meta:
            model=Sex
            fields=['sex']   

#Race
class CreateRaceForm(ModelForm):
    
      race=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter race'
                         }
            )

      )
      class Meta:
            model=Race
            fields=['race']      

#Slot Machine
class CreateSlotMachineForm(ModelForm):
    
      name=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter Machine No',
                         'min': '0'
                         }
                        
            )

      )
      class Meta:
            model=Slot_Machine
            fields=['name']           
#Reason
class CreateReasonForm(ModelForm):
    
      reason=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter reason'
                         }
            )

      )
      class Meta:
            model=Reason
            fields=['reason']    

#Duration
class CreateDurationForm(ModelForm):
    
      duration=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter duration'
                         }
            )

      )
      class Meta:
            model=Duration
            fields=['duration']                    

#CDErrorType
class CreateCDErrorTypeForm(ModelForm):
    
      error_type=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter cash desk error type'
                         }
            )

      )
      class Meta:
            model=CDErrorType
            fields=['error_type']   
#CDExeptionType
class CreateCDExeptionTypeForm(ModelForm):
    
      exeption_type=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter daily exeption type'
                         }
            )

      )
      class Meta:
            model=ExceptionType
            fields=['exeption_type']   
#PokerCombination
class CreatePokerCombinationForm(ModelForm):
    
      poker_combination=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter poker combination'
                         }
            )

      )
      class Meta:
            model=PokerCombination
            fields=['poker_combination']   
#PokerTable
class CreatePokerTableForm(ModelForm):
    
      poker_table=forms.CharField(
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter poker table'
                         }
            )

      )
      class Meta:
            model=PokerTable
            fields=['poker_table']     

#Report
class CreateReportForm(ModelForm): 

      report_nro=forms.IntegerField(
            required=True,
            label='Report #',
            
            widget=forms.NumberInput(
            attrs={'placeholder': 'Report #',
                   'min': '0',
                     'class': 'form-control'}
      ))           
  
     
      date = forms.DateField(
            widget=forms.DateInput(
                 format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
            )
      )
     
      time=forms.TimeField(
            
            widget=forms.TimeInput(
                  format='%H:%M',
                                    attrs={'class':'form-control','type': 'time'} )

            )
      report_type = forms.ModelChoiceField(
            required=True,
            queryset=ReportType.objects.all()  , 
            widget=forms.Select(
              attrs={'class': 'form-select'}
      ))
      report_title = forms.ModelChoiceField(  
           required=True,      
       queryset=ReportTitle.objects.all() , 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
      area = forms.ModelChoiceField(  
            label='Location',
           
        queryset=Area.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-select','placeholder': 'Casino Area',}
      ))
      duty_manager = forms.ModelChoiceField(  
            required=True,
            label='Duty Manager',
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
     
      pittboss = forms.ModelChoiceField(  
            required=False,
            label='PitBoss/Supervisor',
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
     
      inspector = forms.ModelChoiceField( 
            required=False, 
            label='Inspector/Senior',
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
    
      dealer = forms.ModelChoiceField(  
            label='Dealer/Cashier/Attendant',
            required=False,
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
     
      
      other = forms.ModelChoiceField(  
            label='Others',
            required=False,
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
      ))
     
      detail = forms.CharField(
            required=False,
        widget=forms.Textarea(
            attrs={'name':'deatil', "rows":6, "cols":10,"class":'form-control p-3', "placeholder":'Detail','spellcheck':'true'}
               ))
      
      action_token = forms.CharField(
            required=False,
            label='Action Taken',
        widget=forms.Textarea(
              attrs={'name':'action_token', "rows":6, "cols":10,"class":'form-control p-3', "placeholder":'Action Taken','spellcheck':'true'}
            
               ))

      value_us = forms.FloatField(
            required=False,
        widget=forms.NumberInput(
            attrs={'placeholder': 'Value US','min': '0', 'class': 'form-control'}
      ))    
      
      winning=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Winning#','min': '0', 'class': 'form-control'}
      ))
      box=forms.IntegerField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Box', 
                   'min': '0',
                   'class': 'form-control'}
      ))
      money_recovered=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Money Recovered','min': '0', 'class': 'form-control'}
      ))
      money_not_recovered=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Money Not Recovered','min': '0', 'class': 'form-control'}
      ))
      money_paid=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Money Paid','min': '0', 'class': 'form-control'}
      ))
      money_not_paid=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={'placeholder': 'Money Paid','min': '0', 'class': 'form-control'}
      ))
      
    
      
      origination = forms.ModelChoiceField(  
         required=True,
        queryset=ReportOrigination.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
     ))
     
      cctv_id = forms.ModelChoiceField(  
            label='Cctv Officer',
            required=True,
        queryset=Staff.objects.all().order_by('name'), 
        widget=forms.Select(
            attrs={'class': 'form-select'}
     ))    
      customer = forms.ModelChoiceField( 
            required=False, 
        queryset=Customer.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-select','placeholder':'Customer'}
     )) 
      usd_rate=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={ 'class': 'form-control','min': '0','placeholder': 'USD Rate'},
           
      ))    
      euro_rate=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={ 'class': 'form-control','min': '0','placeholder': 'Euro Rate'},
            
      ))
      gbp_rate=forms.FloatField(
            required=False,
            widget=forms.NumberInput(
            attrs={ 'class': 'form-control','min': '0','placeholder': 'GBP Rate'},
           
      ))  
      
      dubbed_to = forms.BooleanField(
      required=False,
      label='Footage',
      widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
               )
      )

     
     

      class Meta:
           model=Report
           fields=['report_nro','date','time','report_title','area','duty_manager','pittboss','inspector','dealer','detail','action_token',
                   'value_us','winning','box','money_recovered','money_not_recovered','money_paid','money_not_paid','dubbed_to','origination',
                   'report_type','cctv_id','customer','usd_rate','euro_rate','gbp_rate','other']  
      
     
      def __init__(self, *args, **kwargs):
             
            
             super().__init__(*args, **kwargs)
               # Filtrar el campo 'categoria' para que solo muestre ciertas categorías
             self.fields['duty_manager'].queryset = Staff.objects.filter(   Q(active=1)  &   ( Q(location_id=3 )  | Q(location_id=self.initial['location_id'])) & Q(department__exact=8) ).order_by('name')  
            # self.fields['duty_manager1'].queryset = Staff.objects.filter(   Q(active=1)  &   ( Q(location_id=3 )  | Q(location_id=self.initial['location_id'])) & Q(department__exact=8) ).order_by('name')      
             self.fields['pittboss'].queryset =  Staff.objects.filter( Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3)) ).exclude(department=8).order_by('name')
             #self.fields['supervisor'].queryset =  Staff.objects.filter( Q(department__exact=7) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3)) ).order_by('name')
             self.fields['inspector'].queryset = Staff.objects.filter( Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).exclude(department=8).order_by('name')
           #  self.fields['senior'].queryset = Staff.objects.filter(  Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name')
             self.fields['dealer'].queryset = Staff.objects.filter( Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).exclude(department=8).order_by('name')
           #  self.fields['cashier'].queryset = Staff.objects.filter(Q(department__exact=4) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name')
           #  self.fields['attendant'].queryset = Staff.objects.filter(Q(department__exact=1) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name')
             self.fields['other'].queryset = Staff.objects.filter( Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) | Q(location_id=4) )).order_by('name').order_by('name')
           #  self.fields['other1'].queryset = Staff.objects.filter( Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name').order_by('name')
             self.fields['cctv_id'].queryset = Staff.objects.filter( Q(department__exact=11) & Q(active=1) & Q(location_id= self.initial['location_id']) | Q(location_id=4) ).order_by('name')
             self.fields['customer'].queryset = Customer.objects.filter( Q(location_id= self.initial['location_id'])).order_by('customer')
            


class FilterReport(forms.Form):
       date_begin = forms.DateField(
             
        widget=forms.DateInput(
              format='%Y-%m-%d',
              attrs={'type': 'date', 'placeholder':'Select date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput(
              format='%Y-%m-%d',
              attrs={'type': 'date', 'placeholder':'Select date','class':'form-control'}),
        required=True,
        label="and",
    
        )
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       
   
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location'] 
            #  self.initial['date_begin'] = datetime.datetime.now()
             # self.initial['date_end'] = datetime.datetime.now()
              
     
    #Este metodo lo mofique y cambie la busqueda por numero de reporte  
class FilterReportById(forms.Form):
       report_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class':'form-control','min': '0','placeholder':'Enter Report No.'} ),
        required=True,
        label="Report No.",
        
          )
       
class   FilterReportByType(forms.Form):
        report_type = forms.ModelChoiceField(
           
            queryset=ReportType.objects.all()  , 
            widget=forms.Select( attrs={'class':'form-select'}
                  ))
#DailyShift
class CreateDailyShiftForm(ModelForm):
      
      date = forms.DateField(
            label='Date',
            widget=forms.DateInput(
                  
                 format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
                  'type': 'date'
               }
            )
      )

      
     
      shift= forms.ModelChoiceField(
            label='Shift',
            queryset= Shift.objects.all(),
            widget=forms.Select(
                  {
               'class':'form-select'

                   }
                 )
            

                     )
      
      supervisor = forms.ModelChoiceField(
             label='Supervisor',
            queryset=Staff.objects.all().order_by('name'),
            widget=forms.Select(
                
            attrs={'class': 'form-select',
                   'placeholder': 'Select a date',
              
                  }
     ))
      officer1 = forms.ModelChoiceField(
             label='Officer 1',
             required=False,
              queryset=Staff.objects.all().order_by('name'),
           widget=forms.Select(
                
           attrs={'class': 'form-select',
                   'placeholder': 'Select a officer',
              
                  }
     ))
      officer2 = forms.ModelChoiceField(
             label='Officer 2',
             required=False,
      queryset=Staff.objects.all().order_by('name'),
           widget=forms.Select(
                
           attrs={'class': 'form-select',
                   'placeholder': 'Select a officer',
              
                  }
     ))
      usd_rate = forms.FloatField(
            
        widget=forms.NumberInput(
            attrs={'placeholder': 'USD Rate', 'min': '0','class': 'form-control'}
               ))
      
      euro_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'EURO Rate','min': '0', 'class': 'form-control'}
               ))

      gbp_rate = forms.FloatField(
        widget=forms.NumberInput(
            attrs={'placeholder': 'GBP Rate', 'min': '0','class': 'form-control'}
        ))
      casino_open=forms.TimeField(
            widget=forms.TimeInput(
                  format='%H:%M',                  
              attrs={'class':'form-control','type': 'time',}    
            )
      )
      casino_close=forms.TimeField(
            widget=forms.TimeInput(format='%H:%M', attrs={'class':'form-control','type': 'time'} )

            )
		
      detail = forms.CharField(
            required=False,
        widget=forms.Textarea(
            attrs={'name':'deatil', "rows":3, "cols":5,"class":'form-control p-3', "placeholder":'Detail','spellcheck':'true'}
               ))
      
    
      
   

     
      class Meta:
            model=DailyShift
            fields=['date','supervisor', 'shift','officer1','officer2','usd_rate','euro_rate','gbp_rate','casino_open','casino_close','detail',]  
      
      def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
             
              self.fields['officer1'].queryset =Staff.objects.filter( Q(department__exact=11) & Q(active=1) & Q(location_id= self.initial['location_id']) | Q(location_id=4) ).order_by('name')  
              self.fields['officer2'].queryset = Staff.objects.filter( Q(department__exact=11) & Q(active=1) & Q(location_id= self.initial['location_id']) | Q(location_id=4) ).order_by('name') 
              self.fields['supervisor'].queryset =Staff.objects.filter( Q(department__exact=11) & Q(active=1) & Q(location_id= self.initial['location_id']) | Q(location_id=4) ).order_by('name')  
              
     
class FilterDailyShiftByDate(forms.Form) :
        date_begin = forms.DateField(
            widget=forms.DateInput(format='%Y-%m-%d',
                                   attrs={'type': 'date','class':'form-control'}),
            required=True,
            label="Date between"
          )
        date_end = forms.DateField(
            widget=forms.DateInput(format='%Y-%m-%d',
                                   attrs={'type': 'date','class':'form-control'}),
            required=True,
            label="and",
    
        )   
#CashDeskTransactions
class CreateCashDeskTransactionsForm(ModelForm):
            date = forms.DateField(
            widget=forms.DateInput(
                  format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
                      )
               )
            time=forms.TimeField(
            
                   widget=forms.TimeInput(
                  format='%H:%M',
                                    attrs={'class':'form-control','type': 'time'} )
                        )
            
          
            area_cashier=forms.ModelChoiceField(
                  label='Cashier Location',
                  
                  queryset=AreaCashier.objects.all(),
            widget=forms.Select(
                  attrs={'class':'form-select',
                         'placeholder':'Enter cashier location'
                         }
                          )

                   )
                      
            account_type=forms.ModelChoiceField(
                 
                  queryset=AccountType.objects.all().order_by('account_type'),
            widget=forms.Select(
                  attrs={'class':'form-select',
                         'placeholder':'Enter account type'
                         }
            )

                  )
         
         
            customer = forms.ModelChoiceField( 
            required=False, 
             queryset=Customer.objects.all(),         
              widget=forms.Select(
                  attrs={'class': 'form-select','placeholder':'Customer'}
                    )) 
          
            token=forms.ModelChoiceField(
                  queryset=Token.objects.all(),
            widget=forms.Select(
                  attrs={'class':'form-select',
                         'placeholder':'Enter token'
                         }
                                )

                    )
            tt_dolar = forms.FloatField(
                  required=False, 
                  label='TT$',
        widget=forms.NumberInput(
              
            attrs={'placeholder': 'TT$', 'min': '0','class': 'form-control'}
               ))
      
            usd_dolar = forms.FloatField(
                  label='USD',
                  required=False, 
        widget=forms.NumberInput(
            attrs={'placeholder': 'USD Dolar', 'min': '0','class': 'form-control'}
               ))

            euro_dolar  = forms.FloatField(
                  label='EURO',
                  required=False, 
        widget=forms.NumberInput(
            attrs={'placeholder': 'EURO Dolar','min': '0', 'class': 'form-control'}
              ))
            gbp_dolar  = forms.FloatField(
                  label='GBP',
                  required=False, 
        widget=forms.NumberInput(
            attrs={'placeholder': 'GBP Dolar', 'min': '0','class': 'form-control'}
              ))
            cad_dolar  = forms.FloatField(
                  label='CAD',
                  required=False, 
        widget=forms.NumberInput(
            attrs={'placeholder': 'GBP Dolar', 'min': '0','class': 'form-control'}
              ))
            employee= forms.ModelChoiceField(
                  required=False, 
                   queryset=Staff.objects.all().order_by('name'),
                   widget=forms.Select(
                         attrs={'placeholder':'Employee','class':'form-select'}
                   )     

            )
            autorized_by= forms.ModelChoiceField(
                  required=False, 
                   queryset=Staff.objects.all().order_by('name'),
                   widget=forms.Select(
                         attrs={'placeholder':'Employee','class':'form-select'}
                   )     

            )
            detail = forms.CharField(
                  required=False,
            widget=forms.Textarea(
                  attrs={'name':'deatil', "rows":5, "cols":10,"class":'form-control', "placeholder":'Detail','spellcheck':'true'}
                  ))  
            machine_no= forms.ModelChoiceField(
                  required=False, 
                   queryset=Slot_Machine.objects.all().order_by('name'),
                   widget=forms.Select(
                         attrs={'placeholder':'Machine No.','class':'form-select'}
                   )     

            )           
            
            
           
            
            
            class Meta:
                  model=Cash_Desk_Transaction
                  fields=['date','time','area_cashier','account_type','token','customer','machine_no','tt_dolar','usd_dolar','euro_dolar','gbp_dolar','cad_dolar','employee','autorized_by','detail']  
           
            def clean_my_integer_field(self):
                  data = self.cleaned_data.get('tt_dolar')
                  return data or 0  
            

            def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
               # Filtrar el campo 'categoria' para que solo muestre ciertas categorías
              self.fields['autorized_by'].queryset = Staff.objects.filter(   Q(active=1)  &   ( Q(location_id=3 )  | Q(location_id=self.initial['location_id'])) & Q(department__exact=8)  | ( Q(position__exact=118 )  | Q(position__exact=119))).order_by('name')     
              self.fields['employee'].queryset =  Staff.objects.filter(   Q(active=1)   ).order_by('name')           
              self.fields['customer'].queryset = Customer.objects.filter( Q(location_id= self.initial['location_id']) ).order_by('customer') 

              # &   ( Q(location_id=3 )  |Q(location_id=4 )  | Q(location_id=self.initial['location_id']))


class FilterTransactionsByDate(forms.Form):
       date_begin = forms.DateField(
       
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date', 'class':'form-control'}),
        required=True,
       
        label="Date between"
          )
       date_end = forms.DateField(
      
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
        
    
        )
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
      
class FilterTtransactionsByCustomer(forms.Form):
       
       date_begin = forms.DateField(
       
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date', 'class':'form-control'}),
        required=True,
       
        label="Date between"
          )
       date_end = forms.DateField(
      
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
        
    
        ) 
       customer = forms.ModelChoiceField(
             required=True,
              queryset=Customer.objects.all(),
        
                  widget=forms.Select(
                         attrs={'placeholder':'Customer','class': 'form-select'}
                   )   
        
          )   
       
       location = forms.ModelChoiceField(
            queryset=Location.objects.all(), 
            required=False, 
            label='Branch',
            widget=forms.HiddenInput()
            )
       
       customer = forms.ModelChoiceField(
             required=True,
              queryset= Customer.objects.none(),
        
                  widget=forms.Select(
                         attrs={'placeholder':'Customer','class': 'form-select'}
                   )   
        
          )   
      
       def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            self.location=self.initial['location']
            location_id=self.initial['location_id']     
                       
            self.fields['customer'].queryset = get_customers_by_location(location_id)      
       
class   FilterTransactionsByType(forms.Form):
        date_begin = forms.DateField(
       
          widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date', 'class':'form-control'}),
           required=True,
       
           label="Date between"
            )
        date_end = forms.DateField(
      
         widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
         required=True,
         label="and",
        
    
         )
        account_type = forms.ModelChoiceField(
           
            queryset=AccountType.objects.all()  , 
            widget=forms.Select(
                         attrs={'placeholder':'Account Type','class': 'form-select'}
                   )   
                  )
        
        location = forms.ModelChoiceField(
            queryset=Location.objects.all(), 
            required=False, 
            label='Branch',
            widget=forms.HiddenInput()
         )
      
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            self.location=self.initial['location'] 
      
class CustomerExpenseForm(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d',attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )
       customer = forms.ModelChoiceField(
             required=True,
             label='Customer',
              queryset=Customer.objects.all(),
         widget=forms.Select(
                         attrs={'placeholder':'Customer','class':'form-select'}
                   )   
        
          ) 
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
       def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            self.location=self.initial['location'] 
            location_id=self.initial['location_id']      
          
            self.fields['customer'].queryset = get_customers_by_location(location_id) 
       
class CustomerComplimentaryForm(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )
       customer = forms.ModelChoiceField(
             required=True,
              queryset=Customer.objects.all(),
        widget=forms.Select(
                         attrs={'placeholder':'Customer','class': 'form-select'}
                   )   
        
          ) 

       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
       def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            self.location=self.initial['location'] 
            location_id=self.initial['location_id']      
          
            self.fields['customer'].queryset = get_customers_by_location(location_id) 


class CreateStaffForm(ModelForm):
      location = forms.ModelChoiceField(
              queryset=Location.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select'}
               ))

      id=forms.IntegerField(
             widget=forms.NumberInput(
            attrs={'placeholder': 'Staff Id',
                    'class': 'form-control',
                    'min': '0',
                    }
              ))
      name=forms.CharField(

              widget=forms.TextInput(
            attrs={'placeholder': 'Name', 'class': 'form-control'}
              ))
      surname=forms.CharField(

              widget=forms.TextInput(
            attrs={'placeholder': 'Surname', 'class': 'form-control'}
              ))
      active=forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(
                          attrs={'placeholder': 'Active', 'class': 'form-control form-check-input','type':'checkbox'}
            )      
           
              )
      photo=forms.ImageField(
            required=False,
             widget=forms.ClearableFileInput(
                  attrs={'class': 'form-control-file','accept': 'image/*',  }

             )

      )
      department = forms.ModelChoiceField(
              queryset=Department.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select'}
               ))
      position = forms.ModelChoiceField(
              queryset=Position.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select'}
               ))

      class Meta:
            model=Staff
            fields=['id','name','surname','photo','department','position','active','location'] 
    
      

      

     
#BlackList  
class CreateBlackListForm(ModelForm): 
      location = forms.ModelChoiceField(
              queryset=Location.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select'}
               ))


      
      name=forms.CharField(

              widget=forms.TextInput(
            attrs={'placeholder': 'Name', 'class': 'form-control'}
              ))
      surname=forms.CharField(

              widget=forms.TextInput(
            attrs={'placeholder': 'Surname', 'class': 'form-control'}
              ))
      blacklistby = forms.ModelChoiceField(
              queryset=Staff.objects.all().order_by('name'),
        
               widget=forms.Select(
                  attrs={'class': 'form-select'}
               ))
      date = forms.DateField(
            widget=forms.DateInput(
                   format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
            )
      )
      details = forms.CharField(
            required=False,
        widget=forms.Textarea(
            attrs={'name':'deatil', "rows":3, "cols":5,"class":'form-control p-3', "placeholder":'Detail','spellcheck':'true'}
               ))


      picture=forms.ImageField(
             widget=forms.ClearableFileInput(
                  attrs={'class': 'form-control-file','accept': 'image/*',  }

             )

      )
    
      sex = forms.ModelChoiceField(
              queryset=Sex.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select','placeholder':'Select Sex'}
               ))
      reason = forms.ModelChoiceField(
              queryset=Reason.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select','placeholder':'Select Reason'}
               ))
      duration = forms.ModelChoiceField(
              queryset=Duration.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select','placeholder':'Select Reason'}
               ))
      race = forms.ModelChoiceField(
              queryset=Race.objects.all(),
        
               widget=forms.Select(
                  attrs={'class': 'form-select','placeholder':'Select Reason'}
               ))
     
      
     
     
  


      class Meta:
            model=BlackList
            fields=['id','name','surname','blacklistby','date','picture','sex','reason','race','duration','details','location' ]

      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
       
       
        self.fields['blacklistby'].queryset =  Staff.objects.all().order_by('name')  


 #####*****CashDeskError***#########   

class CashDeskErrorForm(ModelForm):
            date = forms.DateField(
            widget=forms.DateInput(
                format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
                      )
               )
            time=forms.TimeField(
            
                   widget=forms.TimeInput(
                  format='%H:%M',
                                    attrs={'class':'form-control','type': 'time'} )
                        )
            
           
            area_cashier=forms.ModelChoiceField(
                  label='Cashier Location',
                  
                  queryset=AreaCashier.objects.all(),
            widget=forms.Select(
                  attrs={'class':'form-select',
                         'placeholder':'Select cashier location'
                         }
                          )

                   )
            
            error_type= forms.ModelChoiceField(
                  queryset=CDErrorType.objects.all(),
                  widget=forms.Select(
                     attrs={'class':'form-select',
                         'placeholder':'Select error type'
                         }    
                  )



            )
            duty_manager = forms.ModelChoiceField(  
            required=True,
              queryset=Staff.objects.all().order_by('name'), 
                widget=forms.Select(
              attrs={'class': 'form-select','placeholder':'Select duty manager'}
                  ))
            tt  = forms.FloatField(
                  required=False, 
                  label='TTD',
                    widget=forms.NumberInput(
                    attrs={'placeholder': 'TTD', 'min': '0','class': 'form-control'}
              ))
            usd  = forms.FloatField(
                  required=False, 
                  label='USD',
        widget=forms.NumberInput(
            attrs={'placeholder': 'USD','min': '0', 'class': 'form-control'}
              ))
            euro  = forms.FloatField(
                  required=False, 
                  label='EURO',
        widget=forms.NumberInput(
            attrs={'placeholder': 'EURO','min': '0', 'class': 'form-control'}
              ))

            

            
            cashier = forms.ModelChoiceField(  
            required=True,
             queryset=Staff.objects.all().order_by('name'), 
                    widget=forms.Select(
                attrs={'class': 'form-select','placeholder':'Select cashier','name':'Cashier'}
               ))
            supervisor = forms.ModelChoiceField(  
            required=True,
             queryset=Staff.objects.all().order_by('name'), 
                    widget=forms.Select(
                attrs={'class': 'form-select','placeholder':'Select supervisor'}
               ))
           
            report=forms.IntegerField(
                  required=False,
                  label='Report No.',
                  widget=forms.NumberInput(
                   attrs={'class':'form-control','min':0,'placeholder':'Report No.'}
                        
            ))

            found=forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(
                          attrs={'placeholder': 'Found', 'class': 'form-control form-check-input','type':'checkbox'}
            )      
           
              )
            
            
            class Meta:
             model=Cash_Desk_Error
             fields=['date','time','area_cashier','error_type','duty_manager','tt','usd','euro','cashier','supervisor','report','found']  
            
            def __init__(self, *args, **kwargs):
                  super().__init__(*args, **kwargs)
                 
                  self.fields['duty_manager'].queryset = Staff.objects.filter(   Q(active=1)  &   ( Q(location_id=3 )  | Q(location_id=self.initial['location_id'])) & Q(department__exact=8) ).order_by('name')    
                  self.fields['cashier'].queryset = Staff.objects.filter(department__exact=4,active=True).order_by('name')
                  self.fields['supervisor'].queryset = Staff.objects.filter(department__exact=4,active=True).order_by('name')

class FilterCdErrorByDate(forms.Form):

       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )  
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  

class   FilterCashierSynopsis(forms.Form):
        date_begin = forms.DateField(
            widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
            required=True,
            label="Date between"
            )
        date_end = forms.DateField(
            widget=forms.DateInput( format='%d-%m-Y',
                                    attrs={'type': 'date','class':'form-control'}),
            required=True,
            label="and",
    
         )  
        

        cashier = forms.ModelChoiceField(
           
            queryset=Staff.objects.all().order_by('name')  , 
             widget=forms.Select(
                         attrs={'placeholder':'Cashier','class':'form-select'}
                   )   ) 
        location = forms.ModelChoiceField(
            queryset=Location.objects.all(), 
            required=False, 
            label='Branch',
            widget=forms.HiddenInput()
            )
        
        def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']               
              self.fields['cashier'].queryset = Staff.objects.filter(department__exact=4,active=True).order_by('name')  
 #####*************************#####################END CASH DESK ERROR**********############
#######***************************POKER PAYOUT **********#####################################
class PokerPayoutForm(ModelForm):
       date = forms.DateField(
            widget=forms.DateInput(
                  format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
                      )
               )
       time=forms.TimeField(
            
                   widget=forms.TimeInput(
                  format='%H:%M',
                                    attrs={'class':'form-control','type': 'time'} )
                        )
            
     
       table=forms.ModelChoiceField(
             queryset=PokerTable.objects.all().order_by('poker_table'),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Table',
             
               }   
             )

       )
       combination=forms.ModelChoiceField(
             queryset=PokerCombination.objects.all().order_by('poker_combination'),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Combination',
             
               }   
             )

       )

       bet=forms.FloatField(
             widget=forms.NumberInput(
                  attrs={'class':'form-control',
                         'min': '0',
                  'placeholder': 'Enter a bet',
             
               }     
             )
       )
      
       payout =forms.FloatField(
             widget=forms.NumberInput(
                  attrs={'class':'form-control',
                         'min': '0',
                  'placeholder': 'Enter a payout',
             
               }     
             )
       )

       customer=forms.ModelChoiceField(
             queryset=Customer.objects.all(),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Customer',
             
               }   
             )

       )
       dealer=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Dealer',
             
               }   
             )

       )
       inspector=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Inspector',
             
               }   
             )

       )
       pitboss=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Pitboss',
             
               }   
             )

       )
       class Meta:
             model=Poker_Payout
             fields=['date','time','table','combination','bet','payout','customer','dealer','inspector','pitboss']  

       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)           
             
              self.fields['pitboss'].queryset =  Staff.objects.filter( Q(department__in=[7, 8]) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3)) ).order_by('name')
              self.fields['inspector'].queryset = Staff.objects.filter(Q(department__in=[7, 8]) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name')
              self.fields['dealer'].queryset = Staff.objects.filter(Q(department__in=[7, 8]) & Q(active=1) & ( Q(location_id=self.initial['location_id']) | Q(location_id=3) )).order_by('name')
              self.fields['customer'].queryset = Customer.objects.filter( Q(location_id=self.initial['location_id']))


class FilterPokerPayoutsDate(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )  
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  

class FilterSynopsisStaffForm(forms.Form):
      date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
      date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  
      pitboss=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             required=False,
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Pitboss',
             
               }   
             )

       )
      dealer=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             required=False,
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Dealer',
             
               }   
             )

       )
      inspector=forms.ModelChoiceField(
             queryset=Staff.objects.all().order_by('name'),
             required=False,
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Inspector',
             
               }   
             )

       )
      location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs) 
              self.fields['pitboss'].queryset = Staff.objects.filter(department__exact=7,active=True).order_by('name').order_by('name')
              self.fields['inspector'].queryset = Staff.objects.filter(department__exact=7,active=True).order_by('name').order_by('name')
              self.fields['dealer'].queryset = Staff.objects.filter(department__exact=7,active=True).order_by('name').order_by('name')
              self.location=self.initial['location']  

class FilterPokerPayoutCustomerForm(forms.Form):
      date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
      date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  
      customer=forms.ModelChoiceField(
             queryset=Customer.objects.none(),
             
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Customer',
             
               }   
             )

       )
      location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location'] 
              location_id=self.initial['location_id'] 
              self.fields['customer'].queryset = get_customers_by_location_poker_payout(location_id)  

             

class FilterPokerPayoutCombinationForm(forms.Form):
      date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
      date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  
      combination=forms.ModelChoiceField(
             queryset=PokerCombination.objects.all().order_by('poker_combination'),
             
             widget=forms.Select(
                   attrs={'class':'form-select',
                  'placeholder': 'Select a Combination',
             
               }   
             )

       )
      location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  
     
###***********POKER PAYOUT***********#######
###*************CounterFait***********#######
class CounterfaitForm(ModelForm):

      date = forms.DateField(
             required=True,
            widget=forms.DateInput(
                 

                 format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
                      )
               )
      area_cashier=forms.ModelChoiceField(
            required=True,
            label='Location',
            queryset=AreaCashier.objects.all(),
                   widget=forms.Select(
              
                                    attrs={'class':'form-select'} )                        )
      
            
   
      usd_dolar = forms.FloatField(
                  required=False, 
                  label='USD',
        widget=forms.NumberInput(
            attrs={'placeholder': 'USD Dolar', 'min': '0','class': 'form-control '}
               ))
      tt_dolar = forms.FloatField(
                  required=False, 
                  label='TTD',
        widget=forms.NumberInput(
            attrs={'placeholder': 'TTD Dolar','min': '0', 'class': 'form-control '}
               ))
      euro_dolar  = forms.FloatField(
                  required=False, 
                  label='EURO',
        widget=forms.NumberInput(
            attrs={'placeholder': 'EURO ','min': '0', 'class': 'form-control '}
              ))
      gbp_dolar  = forms.FloatField(
                  required=False, 
                  label='GBP',
        widget=forms.NumberInput(
            attrs={'placeholder': 'GBP','min': '0','class': 'form-control '}
              ))
      serial_number=forms.CharField(
            required=True,
           
             widget=forms.TextInput(
                  attrs={'class':'form-control ',
                         'placeholder':'Enter serial number'
                         }
            )

      )

      report_nro =forms.IntegerField(
            required=True,
          

             widget=forms.NumberInput(
                  attrs={'class':'form-control',
                         'min': '0',
                  'placeholder': 'Enter report #',
             
               }     
             )
       )


      notes = forms.CharField(
            required=False,
        widget=forms.Textarea(
            attrs={'name':'deatil', "rows":2, "cols":10,"class":'form-control p-3', "placeholder":'Detail','spellcheck':'true'}
               ))
      
      employee=forms.ModelChoiceField(
            label='Cashier',
            required=False,
                  
                  queryset=Staff.objects.all().order_by('name'),
            widget=forms.Select(
                  attrs={'class':'form-control',
                         'placeholder':'Select Cashier'
                         }
                          )

                   )
     
      customer = forms.ModelChoiceField( 
            required=False, 
        queryset=Customer.objects.all(), 
        widget=forms.Select(
            attrs={'class': 'form-select','placeholder':'Customer'}
     )) 


      class Meta:
            model=Counterfait   
            fields=['date','area_cashier','report_nro' ,'employee','customer','tt_dolar','usd_dolar','euro_dolar','gbp_dolar','serial_number','notes']
    
      def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
          
            #  self.fields['autorized_by'].queryset = Staff.objects.filter(   Q(active=1)  &   ( Q(location_id=3 )  | Q(location_id=self.initial['location_id'])) & Q(department__exact=8)  | ( Q(position__exact=118 )  | Q(position__exact=119))).order_by('name')     
              self.fields['employee'].queryset =  Staff.objects.filter(   Q(active=1) &  Q(department__exact=4) &  Q(location_id=self.initial['location_id'])  ).order_by('name')           
              self.fields['customer'].queryset = Customer.objects.filter( Q(location_id= self.initial['location_id']) ).order_by('customer') 
             

class FilterCounterfaitDate(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-%Y',
                               attrs={'type': 'date','class':'form-control'}),
        input_formats=['%d-%m-%Y'],
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        ) 
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  

#DailyException
class CreateDailyExeptionForm(ModelForm):
            date = forms.DateField(
            widget=forms.DateInput(
                  format='%Y-%m-%d',
                  attrs={'class':'form-control',
                  'placeholder': 'Select a date',
               'type': 'date'
               }
                      )
               )          
            
          
            employee=forms.ModelChoiceField(
                  
                  queryset=Staff.objects.all().order_by('name'),
            widget=forms.Select(
                  attrs={'class':'form-control',
                         'placeholder':'Select employee'
                         }
                          )

                   )
                      
            exception_type=forms.ModelChoiceField(
                 
                  queryset=ExceptionType.objects.all(),
            widget=forms.Select(
                  attrs={'class':'form-control form-control',
                         'placeholder':'Select exeption type'
                         }
            )

                  )
             
            daily_from = forms.TimeField(
                  required=False, 
                  label='Time In',
        widget=forms.TimeInput(
             
                  format='%H:%M',                  
              attrs={'class':'form-control form-control','type': 'time'}    
            ))
            daily_to = forms.TimeField(
                  required=False, 
                   label='Time Out',
       widget=forms.TimeInput(
                  format='%H:%M',                  
              attrs={'class':'form-control form-control','type': 'time','placeholder':'Over Time To'}    
            )
               )
           
          #  old_shift = forms.TimeField(
         #         required=False, 
        # widget=forms.TimeInput(
        #          format='%H:%M',                  
        #      attrs={'class':'form-control form-control','type': 'time','placeholder':'Select Old Shift'}    
         #   ))
           # new_shift = forms.TimeField(
          #        required=False, 
       # widget=forms.TimeInput(
         #         format='%H:%M',                  
         #     attrs={'class':'form-control form-control','type': 'time','placeholder':'Select New Shift'}    
         #   ))
            detail = forms.CharField(
            required=False,
        widget=forms.Textarea(
            attrs={'name':'deatil', "rows":2, "cols":10,"class":'form-control p-3', "placeholder":'Detail','spellcheck':'true'}
               ))    
            
            
            class Meta:
                  model=DailyExeption
                  fields=['date','employee','exception_type','daily_from','daily_to','detail']  
  
         
            def __init__(self, *args, **kwargs):             
            
             super().__init__(*args, **kwargs)
               # Filtrar el campo 'categoria' para que solo muestre ciertas categorías
             self.fields['employee'].queryset = Staff.objects.filter(   Q(active=1)    ).order_by('name')    
            
class FilterDailyExeptionByDate(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
       exclude = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label="Exclude Staff")
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
      
class FilterDailyExeptionByEmployee(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

       employee = forms.ModelChoiceField(
             required=True,
              queryset=Staff.objects.all().order_by('name'),
        widget=forms.Select(
                         attrs={'placeholder':'Employee','class':'form-control'}
                   )   
        
             )
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  
       

class FilterDailyExeptionByType(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
          )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
        )
     
       type= forms.ModelChoiceField(
             required=True,
              queryset=ExceptionType.objects.all(),
        widget=forms.Select(
                         attrs={'placeholder':'Type','class':'form-select'}
                   )   
        
          )
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']  

#DepartmentForm
class CreateDepartmentForm(forms.ModelForm):
      name=forms.CharField(
            label='Department',
            widget=forms.TextInput(
                  
                  attrs={'class':'form-control ',
                         'placeholder':'Enter Department'
                         }
            )

      )
      class Meta:
            model=Department
            fields=['name']   
            
#Position
class CreatePositionForm(forms.ModelForm):
      department=  forms.ModelChoiceField(
             queryset=Department.objects.all(), 
             widget=forms.Select(
              attrs={'class': 'form-select','placeholder':'Select Department'}
                    ))

      name=forms.CharField(
            label='Position',
            widget=forms.TextInput(
                  attrs={'class':'form-control',
                         'placeholder':'Enter position'
                         }
            )

      )
      class Meta:
            model=Position
            fields=['department','name']

class ReportVideoForm(forms.ModelForm):

     
      video_file = forms.FileField( 
            widget=forms.FileInput(
                  attrs={'accept': 'video/*'}
                  )   ) 
            
            
      caption=forms.CharField(
                  widget=forms.TextInput(
                        attrs={'class':'form-control',
                              'placeholder':'Enter caption'
                              }
                  )  )
      
   
      class Meta:
                  model = ReportVideo

                  fields = ['report', 'caption','video_file', ]
                  
      def __init__(self, *args, **kwargs):
                  report_id = kwargs.pop('report_id', None)  # Obtén el ID del reporte desde kwargs
                  super().__init__(*args, **kwargs)
                  if report_id:
                        # Prellenar el campo 'report' con la instancia del reporte
                        self.fields['report'].initial = report_id
                        # Opcional: Si el campo 'report' debe estar oculto
                        self.fields['report'].widget = forms.HiddenInput()

class MultiVideoUploadForm(forms.Form):
   
    video_files = forms.FileField(
        widget=forms.FileInput(attrs={'allow_multiple_selected': True, 'accept': 'video/*'}),
        required=True
    )

class Synopsis_CCTV(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       employee = forms.ModelChoiceField(
             required=False,
             label='Cctv staff',
              queryset=Staff.objects.none(),
        widget=forms.Select(
                         attrs={'placeholder':'Cctv','class':'form-control form-select'}
                   )   
        
             )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
              if self.location:
                    self.fields['employee'].queryset=Staff.objects.filter(department=11,location=self.location,active=1).order_by('name') 
              else:
                    self.fields['employee'].queryset=Staff.objects.filter(department=11,active=1).order_by('name')

class Synopsis_DEALER(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       employee = forms.ModelChoiceField(
             required=False,
             label='Dealer',
              queryset=Staff.objects.none(),
        widget=forms.Select(
                         attrs={'placeholder':'Dealer','class':'form-control form-select'}
                   )   
        
             )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
              if self.location:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_dealer__isnull=False,location=self.location).distinct().order_by('name') 
              else:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_dealer__isnull=False).distinct().order_by('name')


class Synopsis_INSPECTOR(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       employee = forms.ModelChoiceField(
             required=False,
             label='Inspector',
              queryset=Staff.objects.none(),
        widget=forms.Select(
                         attrs={'placeholder':'Inspector','class':'form-control form-select'}
                   )   
        
             )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
              if self.location:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_inspector__isnull=False,location=self.location).distinct().order_by('name') 
              else:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_inspector__isnull=False).distinct().order_by('name')

class Synopsis_PITBOSS(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       employee = forms.ModelChoiceField(
             required=False,
             label='PitBoss',
              queryset=Staff.objects.none(),
        widget=forms.Select(
                         attrs={'placeholder':'Employee','class':'form-control form-select'}
                   )   
        
             )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
              if self.location:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_pitboss__isnull=False,location=self.location).distinct().order_by('name') 
              else:
                    self.fields['employee'].queryset=Staff.objects.filter(fk_pitboss__isnull=False).distinct().order_by('name')

class Synopsis_SUMMARY(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']
            
                    
class Synopsis_TITTLE(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       tittle = forms.ModelChoiceField(
             required=False,
             label='Report Title',
              queryset=ReportTitle.objects.none(),
        widget=forms.Select(
                         attrs={'placeholder':'Report Title','class':'form-control form-select'}
                   )   
        
             )
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']    
             
              self.fields['tittle'].queryset=ReportTitle.objects.filter(fk_report_title_report__isnull=False).distinct().order_by('title') 

class Synopsis_UNDERPAYMENT(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']    

class Synopsis_OVERPAYMENT(forms.Form):
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
      
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.location=self.initial['location']    
             
             

class FilterTtransactionsByTimeLine(forms.Form):
       
       date_begin = forms.DateField(
       
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date', 'class':'form-control'}),
        required=True,
       
        label="Date between"
          )
       date_end = forms.DateField(
      
        widget=forms.DateInput( format='%Y-%m-%d',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
        
    
        ) 
      
       location = forms.ModelChoiceField(
            queryset=Location.objects.all(), 
            required=False, 
            label='Branch',
            widget=forms.HiddenInput()
            )
       
       customer = forms.ModelChoiceField(
             required=False,
              queryset= Customer.objects.none(),
        
                  widget=forms.Select(
                         attrs={'placeholder':'Customer','class': 'form-select'}
                   )   
        
          )   
      
       def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)            
            self.location=self.initial['location']
            location_id=self.initial['location_id']     
                       
            self.fields['customer'].queryset = get_customers_by_location(location_id)   

class CreateSuppliesForm(forms.ModelForm):
    
    class Meta:
        model = Supplies
        fields = ['date', 'department', 'prepared_by', 'approved_by', 'request_for', 'description','picture']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'prepared_by': forms.Select(attrs={'class': 'form-select'}),
            'approved_by': forms.Select(attrs={'class': 'form-select'}),
            'request_for': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),          
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class Synopsis_Supplies(forms.Form):
       request_choices=[('', 'Select an option'), ('supplies','SUPPLIES'),('equipment','EQUIPMENT'),('service','SERVICE'),('other','OTHER') ]
       date_begin = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y', attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="Date between"
                )
       date_end = forms.DateField(
        widget=forms.DateInput( format='%d-%m-Y',
                               attrs={'type': 'date','class':'form-control'}),
        required=True,
        label="and",
    
                )  

     
       branch = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False, 
        label='Branch',
        widget=forms.HiddenInput()
         )
       department = forms.ModelChoiceField(
             required=False,
             label='Department',
              queryset=Department.objects.all(),
        widget=forms.Select(
                         attrs={'placeholder':'Department','class':'form-select'}
                   )   
        
             )
       prepared_by = forms.ModelChoiceField(
             required=False,
             label='Prepared by',
              queryset=Staff.objects.all(),
        widget=forms.Select(
                         attrs={'placeholder':'Prepared by','class':'form-select'}
                   )   
        
             )
       approved_by = forms.ModelChoiceField(
             required=False,
             label='Approbed by',
              queryset=Staff.objects.all(),
        widget=forms.Select(
                         attrs={'placeholder':'Approbed by','class':'form-select'}
                   )   
        
             )
       request_for = forms.ChoiceField(
        choices=request_choices,
        required=False,
        label='Request for',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
       
     
       def __init__(self, *args, **kwargs):
              super().__init__(*args, **kwargs)
              self.branch=self.initial['branch']
