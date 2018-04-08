echo on

if exist "%~dp0\distpath\KEK420_Connect" (rmdir "%~dp0\distpath\KEK420_Connect")
if exist "%~dp0\distpath\KEK420_Connect" (goto EXIT)
if exist "%~dp0\workpath\KEK420_Connect" (rmdir "%~dp0\workpath\KEK420_Connect")
if exist "%~dp0\workpath\KEK420_Connect" (goto EXIT)

cd "%~dp0\..\..\KEK420\Python Scripts"

"C:\Program Files\Python36\Scripts\pyinstaller.exe" KEK420_Connect.py -p "%%~dp0\..\..\KEK420\Python Scripts" -p "%~dp0\..\..\Library\Python Scripts" --distpath "%~dp0\distpath" --workpath "%~dp0\workpath"

:EXIT
pause