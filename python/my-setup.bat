@echo off
rem
rem  Copyright (c) Bentley Systems, Incorporated. All rights reserved.
rem  See COPYRIGHT.md in the repository root for full copyright notice.
rem
rem This file contains the commands necessary for installing the RAM Concept API.
rem
rem PREREQUISITES:
rem     1) Python 3.8 (or later 3.x) must be installed on the machine
rem     2) Python must be in the path
rem     3) You must have an internet connection
rem

py -3 -m ensurepip --upgrade

rem Check if ram_concept is already installed
py -3 -c "import ram_concept" >nul 2>&1
if %errorlevel% neq 0 (
    echo [RAM Concept Setup] Installing ram_concept package...
    py -3 -mpip install "%~dp0."
) else (
    echo [RAM Concept Setup] ram_concept already installed. Skipping installation.
)

rem === Now run the Python script passed in as arguments ===
py -3 %*
