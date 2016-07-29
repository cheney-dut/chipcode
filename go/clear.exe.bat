@echo off 

set/p "input=是否清空该目录（%cd%）下的所有exe文件（Y/N）:"

if "%input%" == "N" (GOTO _EXIT)
if "%input%" == "n" (GOTO _EXIT)

echo 以下文件已被删除：
for /R %%s in (*.exe) do (
	echo %%s
	del %%s
)

:_EXIT

REM pause
