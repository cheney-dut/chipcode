@echo off 

echo 准备删除以下文件：
for /R %%s in (*.exe) do (
	echo %%s
)

set/p "input=是否清空该目录（%cd%）下所列出的exe文件（Y/N）:"

if "%input%" == "N" (GOTO _EXIT)
if "%input%" == "n" (GOTO _EXIT)
for /R %%s in (*.exe) do (
	echo %%s
	del %%s
)

:_EXIT

pause
