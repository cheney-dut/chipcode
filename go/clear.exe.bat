@echo off 

echo ׼��ɾ�������ļ���
for /R %%s in (*.exe) do (
	echo %%s
)

set/p "input=�Ƿ���ո�Ŀ¼��%cd%�������г���exe�ļ���Y/N��:"

if "%input%" == "N" (GOTO _EXIT)
if "%input%" == "n" (GOTO _EXIT)
for /R %%s in (*.exe) do (
	echo %%s
	del %%s
)

:_EXIT

pause
