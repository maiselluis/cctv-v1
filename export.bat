@echo off
chcp 65001 > nul
set PYTHONUTF8=1
echo Exporting data from the SQLite database...

:: Definir los modelos a exportar
set MODELS=auth.User cctv.Location ^
 cctv.Customer cctv.Department cctv.Position cctv.Sex cctv.Race ^
 cctv.Reason cctv.Duration cctv.ReportType cctv.ReportTitle cctv.Area  ^
 cctv.ReportOrigination cctv.AreaCashier cctv.AccountType cctv.Token cctv.Slot_Machine ^
 cctv.ExceptionType cctv.CDErrorType cctv.PokerCombination cctv.PokerTable cctv.Shift cctv.UserProfile ^
 auth.Permission  cctv.Notification  cctv.Staff cctv.BlackList cctv.Cash_Desk_Error ^
 admin.logentry  contenttypes.ContentType  sessions.session cctv.report ^
 cctv.counterfait cctv.reportvideo cctv.poker_payout cctv.dailyexeption cctv.cash_desk_transaction  ^
 cctv.dailyshift 

:: Carpeta de exportación
set EXPORT_DIR=export_import-data

:: Crear la carpeta si no existe
if not exist %EXPORT_DIR% mkdir %EXPORT_DIR%

:: Exportar cada modelo en UTF-8
for %%M in (%MODELS%) do (
    echo Exporting %%M...
    python -X utf8 manage.py dumpdata %%M --indent 2 > %EXPORT_DIR%\%%M.json
)

echo Export completed.
pause
