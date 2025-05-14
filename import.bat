@echo off
REM Directorio donde se encuentran los archivos exportados
set EXPORT_DIR=export_import-data

REM Importa los datos al nuevo servidor Postgres
echo Importing ContentType.
python manage.py loaddata %EXPORT_DIR%\contenttypes.ContentType.json
echo Importing Permission.
python manage.py loaddata %EXPORT_DIR%\auth.Permission.json  
echo Importing User.
python manage.py loaddata %EXPORT_DIR%\auth.User.json
echo Importing Location.
python manage.py loaddata %EXPORT_DIR%\cctv.Location.json
echo Importing Customer.
python manage.py loaddata %EXPORT_DIR%\cctv.Customer.json
echo Importing Department.
python manage.py loaddata %EXPORT_DIR%\cctv.Department.json 
echo Importing Position.
python manage.py loaddata %EXPORT_DIR%\cctv.Position.json
echo Importing Sex.
python manage.py loaddata %EXPORT_DIR%\cctv.Sex.json
echo Importing Race.
python manage.py loaddata %EXPORT_DIR%\cctv.Race.json
echo Importing Reason.
python manage.py loaddata %EXPORT_DIR%\cctv.Reason.json
echo Importing Duration.
python manage.py loaddata %EXPORT_DIR%\cctv.Duration.json
echo Importing ReportType.
python manage.py loaddata %EXPORT_DIR%\cctv.ReportType.json
echo Importing ReportTitle.
python manage.py loaddata %EXPORT_DIR%\cctv.ReportTitle.json
echo Importing Area.
python manage.py loaddata %EXPORT_DIR%\cctv.Area.json
echo Importing ReportOrigination.
python manage.py loaddata %EXPORT_DIR%\cctv.ReportOrigination.json 
echo Importing AreaCashier.
python manage.py loaddata %EXPORT_DIR%\cctv.AreaCashier.json
echo Importing AccountType.
python manage.py loaddata %EXPORT_DIR%\cctv.AccountType.json
echo Importing Token.
python manage.py loaddata %EXPORT_DIR%\cctv.Token.json
echo Importing Slot_Machine.
python manage.py loaddata %EXPORT_DIR%\cctv.Slot_Machine.json
echo Importing ExceptionType.
python manage.py loaddata %EXPORT_DIR%\cctv.ExceptionType.json 
echo Importing CDErrorType.
python manage.py loaddata %EXPORT_DIR%\cctv.CDErrorType.json
echo Importing PokerCombination.
python manage.py loaddata %EXPORT_DIR%\cctv.PokerCombination.json
echo Importing PokerTable.
python manage.py loaddata %EXPORT_DIR%\cctv.PokerTable.json
echo Importing Shift.
python manage.py loaddata %EXPORT_DIR%\cctv.Shift.json
echo Importing UserProfile.
python manage.py loaddata %EXPORT_DIR%\cctv.UserProfile.json 
echo Importing Notification.
python manage.py loaddata %EXPORT_DIR%\cctv.Notification.json
echo Importing Staff.
python manage.py loaddata %EXPORT_DIR%\cctv.Staff.json
echo Importing BlackList.
python manage.py loaddata %EXPORT_DIR%\cctv.BlackList.json
echo Importing Cash_Desk_Error.
python manage.py loaddata %EXPORT_DIR%\cctv.Cash_Desk_Error.json
echo Importing logentry.
python manage.py loaddata %EXPORT_DIR%\admin.logentry.json 
echo Importing session.
python manage.py loaddata %EXPORT_DIR%\sessions.session.json
echo Importing report.
python manage.py loaddata %EXPORT_DIR%\cctv.report.json
echo Importing counterfait.
python manage.py loaddata %EXPORT_DIR%\cctv.counterfait.json 
echo Importing reportvideo.
python manage.py loaddata %EXPORT_DIR%\cctv.reportvideo.json
echo Importing poker_payout.
python manage.py loaddata %EXPORT_DIR%\cctv.poker_payout.json
echo Importing dailyexeption.
python manage.py loaddata %EXPORT_DIR%\cctv.dailyexeption.json
echo Importing cash_desk_transaction.
python manage.py loaddata %EXPORT_DIR%\cctv.cash_desk_transaction.json
echo Importing dailyshift.
python manage.py loaddata %EXPORT_DIR%\cctv.dailyshift.json



REM Aquí puedes agregar más comandos loaddata para cada archivo JSON
REM Ejemplo:
REM python manage.py loaddata %EXPORT_DIR%\Modelo.json

echo Import completed.
pause
