rem =================get number of cores====================
rem specify number of cores in numOfWorkers.txt as a number
rem in range from 1 to max number of available cores
CD /D "%~dp0"
FOR /F "tokens=*" %%F IN (numOfWorkers.txt) DO (SET cores=%%F)
rem ====================Visibility==========================
title WORKER
rem nircmd.exe win hide ititle "WORKER"
rem ======================find IP===========================
rem using IPv4 
SET ip_address_string="IPv4 Address"
FOR /f "usebackq tokens=2 delims=:" %%P IN (`ipconfig ^| findstr /c:%ip_address_string%`) DO (
    SET IPaddress=%%P
)


rem ======================START=============================
ping -n 1 161.53.71.1 | findstr TTL && GOTO a
ping -n 1 161.53.71.1 | findstr TTL || GOTO Disconnected

:a
python dispyPath.py
FOR /F "tokens=* USEBACKQ" %%F IN (`python dispyPath.py`) DO (
SET var=%%F
)
CD %var%
taskkill /f /im python.exe
python dispynode.py -d -c %cores% -i %IPaddress% --clean 
pause
GOTO :eof





:Disconnected
netsh interface SET interface "Ethernet" disable
timeout 5
netsh interface SET interface "Ethernet" enable
timeout 60
python dispyPath.py
FOR /F "tokens=* USEBACKQ" %%F IN (`py -2  dispyPath.py`) DO (
SET var=%%F
)
CD %var%
taskkill /f /im python.exe
python dispynode.py -d -c %cores% -i %IPaddress% --clean 
