::rd /q/s dist
python device_ids_exe.py py2exe
COPY "dist\device_ids.exe" "."
::COPY "C:\Python27\DLLs\msvcp90.dll" dist
::"C:\Program Files\NSIS\makensis" "provision_exe.nsi"
rd /q/s build
rd /q/s dist
pause