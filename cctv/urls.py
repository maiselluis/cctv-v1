from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from .views import *
from .report import *
from .report import generate_cd_error_synopsis
from .models import *
from .timeline import transaction_timeline




urlpatterns = [
    #login
    path('accounts/login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
   # path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
    path('profile/', profile_view, name='profile'),
    #index
    path('',index,name='index')  , 
    path('dashboard/',dashboard,name='dashboard')  , 
    #mainindex
    path('main/index/',IndexMainView.as_view(),name='main-index')  ,     
    path('main/create/', CreateMainView.as_view(), name='main-create'),
    path('main/update/<int:pk>/', UpdateMainView.as_view(), name='main-update'),
    path('main/delete/<int:pk>/', DeleteMainView.as_view(), name='main-delete'),  
   
   #User
    path('user/',ListUserView.as_view(),name='user-list'),
    path('user/create/', CreateUserView.as_view(), name='user-create'),
    path('user/update/<int:pk>/', UpdateUserView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', DeleteUserView.as_view(), name='user-delete'),
    path('user/detail/<int:pk>/', DetailUserView.as_view(), name='user-detail'),

    #UserProfile
    path('userprofile/',ListUserProfileView.as_view(),name='user_profile-list'),
    path('userprofile/create/', CreateUserProfileView.as_view(), name='user_profile-create'),
    path('userprofile/update/<int:pk>/', UpdateUserProfileView.as_view(), name='user_profile-update'),
    path('userprofile/delete/<int:pk>/', DeleteUserProfileView.as_view(), name='user_profile-delete'),
    path('userprofile/detail/<int:pk>/', DetailUserProfileView.as_view(), name='user_profile-detail'),

    #PERMISSIONS 

    path('permissions/user/<int:user_id>/', ManageUserPermissionsView.as_view(), name='manage_user_permissions'),
    path('permissions/user/<int:user_id>/add/', AddPermissionView.as_view(), name='add_permission'),
    path('permissions/user/<int:user_id>/remove/<int:permission_id>/',RemovePermissionView.as_view(), name='remove_permission'),
    #staffList
    path('staff/',ListStaffView.as_view(),name='staff-list'),
    path('staff/create/', CreateStaffView.as_view(), name='staff-create'),
    path('staff/update/<int:pk>/', UpdateStaffView.as_view(), name='staff-update'),
    path('staff/delete/<int:pk>/', DeleteStaffView.as_view(), name='staff-delete'),
    path('staff/detail/<int:pk>/', DetailStaffView.as_view(), name='staff-detail'),
    #blackList
 
    path('blacklist/',ListBlackListView.as_view(),name='blacklist-list'),
    path('blacklist/create/', CreateBlackListView.as_view(), name='blacklist-create'),
    path('blacklist/update/<int:pk>/', UpdateBlackListView.as_view(), name='blacklist-update'),
    path('blacklist/delete/<int:pk>/', DeleteBlackListView.as_view(), name='blacklist-delete'),
    path('blacklist/detail/<int:pk>/', DetailBlackListView.as_view(), name='blacklist-detail'),
    path("magnifying/<int:id>/",magnifyin,name='magnifying'),

     #blackList-Resintated 
    path('blacklist_reinstated/',ListBlackListView_Reinstated.as_view(),name='blacklist-list-reinstated'),   
    path('blacklist_reinstated/update/<int:pk>/', UpdateBlackListView_Reinstated.as_view(), name='blacklist-update-reinstated'),
    path('blacklist_reinstated/detail/<int:pk>/', DetailBlackListView_Reinstated.as_view(), name='blacklist-detail-reinstated'),
    path("magnifying_reinstated/<int:id>/",magnifyin_Reinstated,name='magnifying-reinstated'),
    
    #Report
    path('report/',ListReportView.as_view(),name='report-list'),
    path('report/create/', CreateReportView.as_view(), name='report-create'),
    path('report/update/<int:pk>/', UpdateReportView.as_view(), name='report-update'),
    path('report/delete/<int:pk>/', DeleteReportView.as_view(), name='report-delete'),
    path('report/detail/<int:pk>/', DetailReportView.as_view(), name='report-detail'),
    path('report_filter/',FilterReportView,name='filter-report'),
    path('report_filter_id/',FilterReportByIdView,name='filter-report-id'),
    path('report_filter_by_type/',FilterReportByTypeView,name='filter-report-type'),

    #video
    path('report/<str:report_id>/videos/', ReportVideoListView.as_view(), name='reportvideo_list'),
    path('report/<str:report_id>/videos/add/', ReportVideoCreateView.as_view(), name='reportvideo_add'),
    path('report/<str:report_id>/videos/<int:pk>/edit/', ReportVideoUpdateView.as_view(), name='reportvideo_edit'),
    path('report/<str:report_id>/videos/<int:pk>/delete/', ReportVideoDeleteView.as_view(), name='reportvideo_delete'),
    path('report/<str:report_id>/videos/upload/', MultiVideoUploadView.as_view(), name='reportvideo_upload'),
    path('video/<int:video_id>/download/', download_video, name='download_video'),
    

    #Token
    path('token/',ListTokenView.as_view(),name='token-list')  , 
    path('token/create/', CreateTokenView.as_view(), name='token-create'),
    path('token/update/<int:pk>/', UpdateTokenView.as_view(), name='token-update'),
    path('token/delete/<int:pk>/', DeleteTokenView.as_view(), name='token-delete'),
    path('token/detail/<int:pk>/', DetailTokenView.as_view(), name='token-detail'),

    #Report Type
    path('report_type/',ListReportTypeView.as_view(),name='report_type-list')  , 
    path('report_type/create/', CreateReportTypeView.as_view(), name='report_type-create'),
    path('report_type/update/<int:pk>/', UpdateReportTypeView.as_view(), name='report_type-update'),
    path('report_type/delete/<int:pk>/', DeleteReportTypeView.as_view(), name='report_type-delete'),
    path('report_type/detail/<int:pk>/', DetailReportTypeView.as_view(), name='report_type-detail'),
    
    #Customer 
    path('customer/',ListCustomerView.as_view(),name='customer-list')  , 
    path('customer/create/', CreateCustomerView.as_view(), name='customer-create'),
    path('customer/update/<int:pk>/', UpdateCustomerView.as_view(), name='customer-update'),
    path('customer/delete/<int:pk>/', DeleteCustomerView.as_view(), name='customer-delete'), 
    path('customer/detail/<int:pk>/', DetailCustomerView.as_view(), name='customer-detail'),
     #Casino Area 
    path('area/',ListCasinoAreaView.as_view(),name='area-list')  , 
    path('area/create/', CreateCasinoAreaView.as_view(), name='area-create'),
    path('area/update/<int:pk>/', UpdateCasinoAreaView.as_view(), name='area-update'),
    path('area/delete/<int:pk>/', DeleteCasinoAreaView.as_view(), name='area-delete'), 
    path('area/detail/<int:pk>/', DetailCasinoAreaView.as_view(), name='area-detail'), 

      #Cashier Area 
    path('cashier_area/',ListCashierAreaView.as_view(),name='cashier_area-list')  , 
    path('cashier_area/create/', CreateCashierAreaView.as_view(), name='cashier_area-create'),
    path('cashier_area/update/<int:pk>/', UpdateCashierAreaView.as_view(), name='cashier_area-update'),
    path('cashier_area/delete/<int:pk>/', DeleteCashierAreaView.as_view(), name='cashier_area-delete'), 
    path('cashier_area/detail/<int:pk>/', DetailCashierAreaView.as_view(), name='cashier_area-detail'), 

      #Report Origination 
    path('report_origination/',ListReportOriginationView.as_view(),name='origination-list')  , 
    path('report_origination/create/', CreateReportOriginationView.as_view(), name='origination-create'),
    path('report_origination/update/<int:pk>/', UpdateReportOriginationView.as_view(), name='origination-update'),
    path('report_origination/delete/<int:pk>/', DeleteReportOriginationView.as_view(), name='origination-delete'), 
    path('report_origination/detail/<int:pk>/', DetailReportOriginationView.as_view(), name='origination-detail'), 
    #Report Tittle
    path('report_title/',ListReportTitleView.as_view(),name='report_title-list')  , 
    path('report_title/create/', CreateReportTitleView.as_view(), name='report_title-create'),
    path('report_title/update/<int:pk>/', UpdateReportTitleView.as_view(), name='report_title-update'),
    path('report_title/delete/<int:pk>/', DeleteReportTitleView.as_view(), name='report_title-delete'),
    path('report_title/detail/<int:pk>/', DetailReportTitleView.as_view(), name='report_title-detail'),
    #Account Type    
    path('account_type/',ListAccount_TypeView.as_view(),name='account_type-list')  , 
    path('account_type/create/', CreateAccount_TypeView.as_view(), name='account_type-create'),
    path('account_type/update/<int:pk>/', UpdateAccount_TypeView.as_view(), name='account_type-update'),
    path('account_type/delete/<int:pk>/', DeleteAccount_TypeView.as_view(), name='account_type-delete'),
    path('account_type/detail/<int:pk>/', DetailAccount_TypeView.as_view(), name='account_type-detail'), 
    
    #Shift  
    path('shift/',ListShiftView.as_view(),name='shift-list')  , 
    path('shift/create/', CreateShiftView.as_view(), name='shift-create'),
    path('shift/update/<int:pk>/', UpdateShiftView.as_view(), name='shift-update'),
    path('shift/delete/<int:pk>/', DeleteShiftView.as_view(), name='shift-delete'),
    path('shift/detail/<int:pk>/', DetailShiftView.as_view(), name='shift-detail'),
    #location
    path('location/',ListLocationView.as_view(),name='location-list')  , 
    path('location/create/', CreateLocationView.as_view(), name='location-create'),
    path('location/update/<int:pk>/', UpdateLocationView.as_view(), name='location-update'),
    path('location/delete/<int:pk>/', DeleteLocationView.as_view(), name='location-delete'),
    path('location/detail/<int:pk>/', DetailLocationView.as_view(), name='location-detail'),
     #Sex
    path('sex/',ListSexView.as_view(),name='sex-list')  , 
    path('sex/create/', CreateSexView.as_view(), name='sex-create'),
    path('sex/update/<int:pk>/', UpdateSexView.as_view(), name='sex-update'),
    path('sex/delete/<int:pk>/', DeleteSexView.as_view(), name='sex-delete'),
    path('sex/detail/<int:pk>/', DetailSexView.as_view(), name='sex-detail'),
    #Race
    path('race/',ListRaceView.as_view(),name='race-list')  , 
    path('race/create/', CreateRaceView.as_view(), name='race-create'),
    path('race/update/<int:pk>/', UpdateRaceView.as_view(), name='race-update'),
    path('race/delete/<int:pk>/', DeleteRaceView.as_view(), name='race-delete'),
    path('race/detail/<int:pk>/', DetailRaceView.as_view(), name='race-detail'),
    #Reason
    path('reason/',ListReasonView.as_view(),name='reason-list')  , 
    path('reason/create/', CreateReasonView.as_view(), name='reason-create'),
    path('reason/update/<int:pk>/', UpdateReasonView.as_view(), name='reason-update'),
    path('reason/delete/<int:pk>/', DeleteReasonView.as_view(), name='reason-delete'),
    path('reason/detail/<int:pk>/', DetailReasonView.as_view(), name='reason-detail'),
    
    #Duration
    path('duration/',ListDurationView.as_view(),name='duration-list')  , 
    path('duration/create/', CreateDurationView.as_view(), name='duration-create'),
    path('duration/update/<int:pk>/', UpdateDurationView.as_view(), name='duration-update'),
    path('duration/delete/<int:pk>/', DeleteDurationView.as_view(), name='duration-delete'),
    path('duration/detail/<int:pk>/', DetailDurationView.as_view(), name='duration-detail'),
   #Cash Desk Error Type
    path('cash_desk_error_type/',ListCDErrorTypeView.as_view(),name='cash_desk_error_type-list')  , 
    path('cash_desk_error_type/create/', CreateCDErrorTypeView.as_view(), name='cash_desk_error_type-create'),
    path('cash_desk_error_type/update/<int:pk>/', UpdateCDErrorTypeView.as_view(), name='cash_desk_error_type-update'),
    path('cash_desk_error_type/delete/<int:pk>/', DeleteCDErrorTypeView.as_view(), name='cash_desk_error_type-delete'),
    path('cash_desk_error_type/detail/<int:pk>/', DetailCDErrorTypeView.as_view(), name='cash_desk_error_type-detail'),
     #Daily Exeption Type
    path('daily_exeption_type/',ListCDExeptionTypeView.as_view(),name='exeption_type-list')  , 
    path('daily_exeption_type/create/', CreateCDExeptionTypeView.as_view(), name='exeption_type-create'),
    path('daily_exeption_type/update/<int:pk>/', UpdateCDExeptionTypeView.as_view(), name='exeption_type-update'),
    path('daily_exeption_type/delete/<int:pk>/', DeleteCDExeptionTypeView.as_view(), name='exeption_type-delete'),
    path('daily_exeption_type/detail/<int:pk>/', DetailCDExeptionTypeView.as_view(), name='exeption_type-detail'), 
     #Poker Combination
    path('poker_combination/',ListPokerCombinationView.as_view(),name='poker_combination-list')  , 
    path('poker_combination/create/', CreatePokerCombinationView.as_view(), name='poker_combination-create'),
    path('poker_combination/update/<int:pk>/', UpdatePokerCombinationView.as_view(), name='poker_combination-update'),
    path('poker_combination/delete/<int:pk>/', DeletePokerCombinationView.as_view(), name='poker_combination-delete'),
    path('poker_combination/detail/<int:pk>/', DetailPoker_CombinationView.as_view(), name='poker_combination-detail'),
     #Poker Table
    path('poker_table/',ListPokerTableView.as_view(),name='poker_table-list')  , 
    path('poker_table/create/', CreatePokerTableView.as_view(), name='poker_table-create'),
    path('poker_table/update/<int:pk>/', UpdatePokerTableView.as_view(), name='poker_table-update'),
    path('poker_table/delete/<int:pk>/', DeletePokerTableView.as_view(), name='poker_table-delete'),
    path('poker_table/detail/<int:pk>/', DetailPokerTableView.as_view(), name='poker_table-detail'),
     #Daily Shift
    path('daily_shift/',ListDailyShiftView.as_view(),name='daily_shift-list')  , 
    path('daily_shift/create/', CreateDailyShiftView.as_view(), name='daily_shift-create'),
    path('daily_shift/update/<int:pk>/', UpdateDailyShiftView.as_view(), name='daily_shift-update'),
    path('daily_shift/delete/<int:pk>/', DeleteDailyShiftView.as_view(), name='daily_shift-delete'),
    path('daily_shift/detail/<int:pk>/', DetailDailyShiftView.as_view(), name='daily_shift-detail'),
    path('find_dailyshift_by_day/', FilterDailyShiftByDateView,name='dailyshift-by-day'),

     #Cash Desk Transactions
    path('cash_desk_transactions/',ListCashDeskTransactionsView.as_view(),name='cash_desk_transactions-list')  , 
    path('cash_desk_transactions/create/', CreateCashDeskTransactionsView.as_view(), name='cash_desk_transactions-create'),
    path('cash_desk_transactions/update/<int:pk>/', UpdateCashDeskTransactionsView.as_view(), name='cash_desk_transactions-update'),
    path('cash_desk_transactions/delete/<int:pk>/', DeleteCashDeskTransactionsView.as_view(), name='cash_desk_transactions-delete'),
    path('cash_desk_transactions/detail/<int:pk>/', DetailCashDeskTransactionsView.as_view(), name='cash_desk_transactions-detail'),
    path('find_transaction_by_day/', FilterTransactionsByDateView,name='transactions-by-day'),
    path('find_transaction_by_customer/', FilterTransactionsByCustomerView,name='transactions-by-customer'),
    path('find_transaction_by_account/', FilterTransactionsByAccountView,name='transactions-by-account'),
    path('find_customer_expense/', FilterCustomerExpense,name='customer-expense'),
    path('customer_complimentary/', FilterCustomerCumplimentary,name='customer-complimentary'),

     #Cash Desk Error
    path('cd_error_shift/',ListCdErrorView.as_view(),name='cash_desk_error-list')  , 
    path('cd_error_shift/create/', CreateCdErrorView.as_view(), name='cash_desk_error-create'),
    path('cd_error_shift/update/<int:pk>/', UpdateCdErrorView.as_view(), name='cash_desk_error-update'),
    path('cd_error/delete/<int:pk>/', DeleteCdErrorView.as_view(), name='cash_desk_error-delete'),
    path('cd_errordetail/<int:pk>/', DetailCdErrorView.as_view(), name='cash_desk_error-detail'),
    path('cd_error_by_day/', FilterCdErrorByDateView,name='cash_desk_error-by-day'),
    path('synopsis_cashier/', FilterSynopsisCashierView,name='synopsis_cashier'),
    path('get_report_id/<str:report_value>/<str:location>/', get_report_id, name='get_report_id'),

     #Poker Payouts
    path('poker_payouts/',ListPokerPayoutsView.as_view(),name='poker_payouts-list')  , 
    path('poker_payouts/create/', CreatePokerPayoutsView.as_view(), name='poker_payouts-create'),    
    path('poker_payoutst/update/<int:pk>/', UpdatePokerPayoutsView.as_view(), name='poker_payouts-update'),
    path('poker_payouts/delete/<int:pk>/', DeletePokerPayoutsView.as_view(), name='poker_payouts-delete'),
    path('poker_payouts/<int:pk>/', DetailPokerPayoutsView.as_view(), name='poker_payouts-detail'),
    path('poker_payouts/poker_payouts_by-date', FilterPokerPayoutsByDateView,name='poker_payouts-by-day'),
    path('poker_payouts/synopsis_staff', FilterSynopsisStaffView,name='synopsis-staff'),
    path('poker_payout/payout_combination',FilterPokerPayoutCombinationView,name='poker_payout-combination'),
    path('poker_payout/payout_customer',FilterPokerPayoutCustomerView,name='poker_payout-customer'),
    path('poker-payout/concurrencia/', poker_payout_concurrency_view, name='poker_payout_concurrency'),
    


    #Report Synopsis
    path('report_synopsis/',ListReportSynopsisView.as_view(),name='report_synopsis-list')  , 
    path('report_synopsis_cctv/',ReportSynopsisCCTV,name='report_synopsis-list-cctv')  , 
    path('report_synopsis_dealer/',ReportSynopsisDEALER,name='report_synopsis-list-dealer')  ,
    path('report_synopsis_inspector/',ReportSynopsisINSPECTOR,name='report_synopsis-list-inspector')  ,
    path('report_synopsis_pitboss/',ReportSynopsisPITBOSS,name='report_synopsis-list-pitboss')  ,
    path('report_synopsis_summary/',ReportSynopsisSUMMARY,name='report_synopsis-list-summary')  ,
    path('report_synopsis_tittle/',ReportSynopsisTITLE,name='report_synopsis-list-tittle')  ,
    path('report_synopsis_underpayment/',ReportSynopsisUNDERPAYMENT,name='report_synopsis-list-underpayment')  ,
    path('report_synopsis_overpayment/',ReportSynopsisOVERPAYMENT,name='report_synopsis-list-overpayment')  ,
   
    #Counterfeit    
    path('counterfeit/',ListCounterfaitView.as_view(),name='counterfeit-list')  , 
    path('counterfeit/create/', CreateCounterfaitView.as_view(), name='counterfeit-create'),
    path('counterfeit/update/<int:pk>/', UpdateCounterfaitView.as_view(), name='counterfeit-update'),
    path('counterfeit/delete/<int:pk>/', DeleteCounterfaitView.as_view(), name='counterfeit-delete'),
    path('counterfeit/<int:pk>/', DetailCounterfaitView.as_view(), name='counterfeit-detail'),
    path('counterfeit/counterfeit_by-date', FilterCounterfaitByDateView,name='counterfeit-by-day'),

 #Daily Exeptions
    path('daily_exeption/',ListDailyExeptionView.as_view(),name='daily_exeption-list')  , 
    path('daily_exeption/create/', CreateDailyExeptionView.as_view(), name='daily_exeption-create'),
    path('daily_exeption/update/<int:pk>/', UpdateDailyExeptionView.as_view(), name='daily_exeption-update'),
    path('daily_exeption/delete/<int:pk>/', DeleteDailyExeptionView.as_view(), name='daily_exeption-delete'),
    path('daily_exeption/detail/<int:pk>/', DetailDailyExeptionView.as_view(), name='daily_exeption-detail'),
    path('daily_exeption_by_day/', FilterDailyExeptionByDateView,name='daily_exeption-by-day'),
    path('daily_exeption_by_employee/', FilterDailyExeptionByEmployeeView,name='daily_exeption-by-employee'),
    path('daily_exeption_by_type/', FilterDailyExeptionByTypeView,name='daily_exeption-by-exeption'),

 #Department
    path('department/',ListDepartmentView.as_view(),name='department-list')  , 
    path('department/create/', CreateDepartmentView.as_view(), name='department-create'),
    path('department/update/<int:pk>/', UpdateDepartmentView.as_view(), name='department-update'),
    path('department/delete/<int:pk>/', DeleteDepartmentView.as_view(), name='department-delete'),
    path('department/detail/<int:pk>/', DetailDepartmentView.as_view(), name='department-detail'),

   #Position
    path('position/',ListPositionView.as_view(),name='position-list')  , 
    path('position/create/', CreatePositionView.as_view(), name='position-create'),
    path('position/update/<int:pk>/', UpdatePositionView.as_view(), name='position-update'),
    path('position/delete/<int:pk>/', DeletePositionView.as_view(), name='position-delete'),
    path('position/detail/<int:pk>/', DetailPositionView.as_view(), name='position-detail'),

    #Machine
    path('machine/',ListMachineView.as_view(),name='machine-list')  , 
    path('machine/create/', CreateMachineView.as_view(), name='machine-create'),
    path('machine/update/<int:pk>/', UpdateMachineView.as_view(), name='machine-update'),
    path('machine/delete/<int:pk>/', DeleteMachineView.as_view(), name='machine-delete'),
    path('machine/detail/<int:pk>/', DetailMachineView.as_view(), name='machine-detail'),



#AJAX
path('load-reporttitle/', LoadReportTitle, name='ajax_load_report_title'),
path('load-position/', LoadPosition, name='ajax_load_position'),


#Report in report.py
  path('report/<int:report>/pdf/', generate_report, name='reporte_pdf'),
  path('report_by_date/pdf/', generate_report_by_date, name='reporte_by_date_pdf'),

#Daily Shift
  path('daily_shift_report/<int:id>/pdf/', generate_daily_shift, name='daily_shift_report'),
 #CAsh DeskTransaction
 path('transactions_pdf/pdf', generate_cash_desk_transaction, name='transaction_view'),
 path('transactions_customer_expense_pdf/pdf', generate_cash_desk_transaction_customer_expense, name='transaction_customer_expense_view'),
 path('transactions_customer_complemimentary_pdf/pdf', generate_cash_desk_transaction_customer_cumplimentary, name='transaction_customer_cumplimentary_view'),
 path('transactions_customer_pdf/pdf', generate_cash_desk_transaction_by_customer, name='transaction_customer_view'),
 path('transactions_account_type_pdf/pdf', generate_cash_desk_transaction_by_account_type, name='transaction_account_type_view'),
 #Poker Payout
 path('poker_payouts_pdf/pdf', generate_poker_payouts, name='poker_payouts_view'),
 path('poker_payouts_pdf_synopsis_staff/pdf', generate_poker_payouts_synopsis_staff, name='poker_payouts_synopsis_staff_view'),
 path('poker_payouts_pdf_combination/pdf', generate_poker_payouts_combination, name='poker_payouts_combination'),
 path('poker_payouts_pdf_customer/pdf', generate_poker_payouts_customer, name='poker_payouts_customer'),
 #Daily Exeption
 path('daily_exception_pdf/pdf', generate_daily_exception, name='daily_exception_pdf'),
 path('daily_exception_by_employee_pdf/pdf', generate_daily_exception_by_employee, name='daily_exception_by_employee_pdf'),
 path('daily_exception_by_type_pdf/pdf', generate_daily_exception_by_type, name='daily_exception_by_type_pdf'),
 
#Counterfeit
path('counterfeit_pdf/pdf', generate_counterfeit, name='counterfeit_pdf'),

#Cash Desk Error
path('generate_cd_error/pdf', generate_cd_error, name='generate_cd_error_pdf'),
path('generate_cd_error_synopsis/pdf', generate_cd_error_synopsis, name='generate_cd_error_synopsis_pdf'),
#BlackList 
path('blacklist-customer/<int:id>/pdf/', generate_customer_blacklist, name='blacklist_pdf'),
#Report Synopsis
path('report_synopsis_cctv/pdf/', generate_report_synopsis_cctv, name='report_synopsis_cctv_pdf'),
path('report_synopsis_dealer/pdf/', generate_report_synopsis_dealer, name='report_synopsis_dealer_pdf'),
path('report_synopsis_inspector/pdf/', generate_report_synopsis_inspector, name='report_synopsis_inspector_pdf'),
path('report_synopsis_pitboss/pdf/', generate_report_synopsis_pitboss, name='report_synopsis_pitboss_pdf'),
path('report_synopsis_title/pdf/', generate_report_synopsis_title, name='report_synopsis_title_pdf'),
path('report_synopsis_overpayment/pdf/', generate_report_synopsis_overpayment, name='report_synopsis_overpayment_pdf'),
path('report_synopsis_underpayment/pdf/', generate_report_synopsis_underpayment, name='report_synopsis_underpayment_pdf'),
path('report_synopsis_summary/pdf/', generate_report_synopsis_summary, name='report_synopsis_summary_pdf'),

#Supplies

path('supplies/', SuppliesListView.as_view(), name='supplies_list'),
path('supplies/<int:pk>/', SuppliesDetailView.as_view(), name='supplies_detail'),
path('supplies/new/', SuppliesCreateView.as_view(), name='supplies_create'),
path('supplies/<int:pk>/edit/', SuppliesUpdateView.as_view(), name='supplies_update'),
path('supplies/<int:pk>/delete/', SuppliesDeleteView.as_view(), name='supplies_delete'),
path('supplies_synopsis/', SynopsisSupplies, name='supplies_synopsis'),


#Timeline
path('transaction_timeline/', transaction_timeline, name='transaction-timeline'),


#mostrar el login dfe ultimos acceso de lo susuarios
path('last_login/', user_last_login_view, name='user_last_login'),

]
