
rem Compile plugin sources with feature Publish cracked
"D:\PiXYZStudio\PiXYZStudioPublishPlugin.exe" "%cd%\ScriptLibrary" "%cd%\RVT.pxzext"

copy "%cd%\RVT.pxzext" "C:\ProgramData\PiXYZScenarioProcessor\plugins\"

python scripts/watcher.py config.json

pause