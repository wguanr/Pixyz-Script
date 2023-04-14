rem Compile plugin sources
"C:\Program Files\PiXYZStudio\PiXYZStudioPublishPlugin.exe" "%cd%\sample" "%cd%\sample.pxzext"

rem Copy scenario plugin in SP installation folder
copy "%cd%\sample.pxzext" "C:\ProgramData\PiXYZScenarioProcessor\plugins\"

pause