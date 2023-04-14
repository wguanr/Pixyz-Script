![](documentation/banner.png)

# What is the Scenario Processor sample?

This sample demonstrates how to take control over Pixyz Scenario Processor capabilities:
1. *Folder Watcher* service: launch a Python service to listen to a folder on your disk. Each file popping in this folder will be processed and converted by an *SP* instance.
2. *Sample scenario* creation and publication from command line
3. *Folder Watcher* service with Sample scenario: launch a Python service to listen to a folder on your disk. Each file popping in this folder will be processed and converted by an *SP* published scenario.

<p align="center">
    <img src="documentation/folder-watcher.png">
</p>

# Getting Started

## Required Software
* [Pixyz Scenario Processor](https://www.pixyz-software.com/download/)
* [Pixyz Studio](https://www.pixyz-software.com/download/) (*Scenario* creation and publication)
* [Python](https://www.python.org/downloads/) (*Folder Watcher* service)

## Setup
* Clone repository (or download .zip)
* [Install](setup/README.md) Pixyz Scenario Processor trial nodelocked license (if needed)

# Samples

## 1. *Folder Watcher* service
This sample shows an *integration* of Pixyz Scenario Processor as being used by a Python service.

### How to use?
* Double click on `run.bat` (make sure you installed Python)
* Copy/Paste 3D files in the `_input` folder. Soon, converted files will appear in the `_output` folder!
* If you don't want for the service to optimize your files: open `config.json` and replace `"optimization":  "True"` by `"optimization":  "False"`

## 2. *Sample* scenario creation and publication
This sample provides the sources of a basic data preparation scenario. It allows to convert one 3D/CAD file to multiple output formats (.fbx, .gltf, .usdz...), optionnaly optimizing (polygon reduction such as decimation, holes removal, hidden parts removal...) the result.
* *sample* folder: source files of the scenario (delivered as a [plugin](https://pixyz-software.com/documentations/html/2021.1/studio/Plugins.html)) created in Pixyz Studio using the [Plugin Editor](https://www.pixyz-software.com/documentations/html/2021.1/studio/UsingthePluginEditor.html)
* *publish.bat*: double click on it to compile and publish rapidly the *sample* scenario to the .pxzext format if you modified it
* *sample.pxzext*: compiled version of the *sample* scenario. Ready to be used in Scenario Processor.

### How to use?
* With Pixyz Scenario Processor:
    * Publish it by double clicking on `publish.bat`
    * Run it in your favorite CLI tool: `"C:\Program Files\PiXYZScenarioProcessor\PiXYZScenarioProcessor.exe" sample convertFile "\"*INPUT_FILE*\"" "\"*OUTPUT_FOLDER*\"" "[\".fbx\", \".glb\"]" "True"`
* With Pixyz Studio:
    * Copy/Paste the `sample` folder to `C:/ProgramData/PiXYZStudio/plugins` and begin editing it in Pixyz Studio *Plugin Editor*

---
**NOTE**

Checkout the source Python script (*sampleScript.py*) and the commented lines to learn more about the different steps of the data preparation scenario.  
Adapt the scenario for your needs by modifying the functions and adjusting parameters values.

---

## 3. *Folder Watcher* service with published Scenario
This sample shows an *integration* of Pixyz Scenario Processor as being used by a Python service.

### How to use?
* Publish the *Sample* scenario from part 1
* Double click on `run.bat` (make sure you installed Python)
* Copy/Paste 3D files in the `_input` folder. Soon, converted files will appear in the `_output` folder!
* If you don't want for the service to optimize your files: open `config.json` and replace `"optimization":  "True"` by `"optimization":  "False"`

