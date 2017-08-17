rmdir dist /s /q
pyinstaller vrmtool.spec
copy dist\vrmtool.exe .
vrmtool.exe
