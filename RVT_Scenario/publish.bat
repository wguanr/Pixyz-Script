
rem Compile plugin sources with feature Publish cracked
"D:\PiXYZStudio\PiXYZStudioPublishPlugin.exe" "%cd%\DataProcessor" "%cd%\DataProcessor.pxzext"

copy "%cd%\DataProcessor.pxzext" "C:\ProgramData\PiXYZScenarioProcessor\plugins\"
copy "%cd%\DataProcessor.pxzext" "D:\PiXYZStudio\plugins\"

pause
