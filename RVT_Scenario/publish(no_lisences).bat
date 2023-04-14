rem Compile plugin sources
"D:\PiXYZStudio\PiXYZStudioPublishPlugin.exe" "%cd%\advanced_process" "%cd%\RVT.pxzext"

rem Copy scenario plugin in SP installation folder
copy "%cd%\RVT.pxzext" "C:\ProgramData\PiXYZScenarioProcessor\plugins\"

pause