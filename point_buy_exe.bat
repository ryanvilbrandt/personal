python point_buy_exe.py py2exe
COPY "dist\Point_Buy_Calc_v*" "."
::COPY "C:\Python27\DLLs\msvcp90.dll" dist
rd /q/s build
rd /q/s dist
pause