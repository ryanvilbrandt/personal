::rd /q/s dist
python vamp_exe.py py2exe
COPY "dist\VampHelper.exe" "."
::COPY "C:\Python27\DLLs\msvcp90.dll" dist
::"C:\Program Files\NSIS\makensis" "provision_exe.nsi"
rd /q/s build
rd /q/s dist
pause