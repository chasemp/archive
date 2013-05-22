
copyfiles.bat
set server=%1
start "" "\\%server%\c$\Program Files"
mkdir "\\%server%\c$\Program Files\NSClient++-Win32-0.3.5"
xcopy "C:\Program Files\NSClient++-Win32-0.3.5\*" "\\%server%\c$\Program Files\NSClient++-Win32-0.3.5" /e /Y
psexec \\%server% "\\%server%\c$\Program Files\NSClient++-Win32-0.3.5\nagplusplusinstall.bat"



nagplusplusinstall.bat
@ECHO OFF

ECHO stopping nagios client
net stop "nagios agent"

ECHO removing nagios client

C:\GSI-TOOLS\Nagios\pnsclient.exe /uninstall

"C:\Program Files\NSClient++-Win32-0.3.5\NSClient++.exe" /install

net start nsclientpp


EXIT
