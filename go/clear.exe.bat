@echo off 

set/p "input=�Ƿ���ո�Ŀ¼��%cd%���µ�����exe�ļ���Y/N��:"

if "%input%" == "N" (GOTO _EXIT)
if "%input%" == "n" (GOTO _EXIT)

echo �����ļ��ѱ�ɾ����
for /R %%s in (*.exe) do (
	echo %%s
	del %%s
)

:_EXIT

REM pause
