#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# this script checks that the RAM Concept API is installed and functioning
import sys
import os

# ANSI codes for terminal colors
red_text_flag ='\033[31m'
green_text_flag ='\033[32m'
lightgrey_text_flag ='\033[37m'

def print_std(text: str) -> None:
    """Prints the text in non-special color"""
    print(lightgrey_text_flag  + text + lightgrey_text_flag) 

def print_red(text: str) -> None:
    """Prints the text in red"""
    print(red_text_flag + text + lightgrey_text_flag) 

def print_green(text: str) -> None:
    """Prints the text in green"""
    print(green_text_flag + text + lightgrey_text_flag) 

os.system("") # for some reason this call is required to allow you to use ANSI codes....(and the colors)

# CHECK FOR PYTHON 3.8
version_info = sys.version_info
if (version_info.major < 3) or (version_info.major > 3):
    print_red("RAM Concept API requires version 3 of Python. Version, currently running version is: " + str(version_info))
    print_red("Python 3.8 is available at: https://www.python.org/downloads/release/python-380/ ")
    print_red("You may have more than one version of Python installed. Try using 'py -3' to launch scripts.")
    exit()
elif version_info.minor < 8:
    print_red("RAM Concept API requires version 3.8 (or later 3.x) of Python, currently running version is: " + str(version_info))
    print_red("Python 3.8 is available at: https://www.python.org/downloads/release/python-380/ ")
    exit()

# CHECK FOR RAM CONCEPT API
try:
    import ram_concept
except:
    print_red("ram_concept (Python library) is not installed. Have you run setup.bat?")
    exit()

# CHECK FOR REQUESTS
try:
    import requests
except:
    print_red("Requests (Python library) is not installed. Use this command to install: 'py -3 -m pip install requests'")
    exit()

# CHECK THAT THE API THAT IS INSTALLED IS THE ONE FOR THIS INSTALLATION
# This is a bit tricky because we don't want to hard code the version number in this file.
# Instead we rely on the existence of the file ram_concept\version_constant.py which has the right version number
from os import path
import sys
this_directory = os.path.dirname(os.path.realpath(__file__))
version_constant_path = os.path.join(this_directory, "ram_concept\\version_constant.py")

if not path.exists(version_constant_path):
    print_red("check_install.py needs to be run from the directory it was installed in.")
    exit()

with open(version_constant_path, "r") as version_constant_file:
    lines = version_constant_file.readlines()

    # we are looking for a line like this: API_VERSION = "99.99.0"
    found_constant = False
    for line in lines:
        if line.startswith("API_VERSION = "):
            found_constant = True
            required_api_version = line.strip().strip("API_VERSION = ")
            break

if not found_constant:
    print_red("Internal error: could not find API_VERSION line")
    exit()

if not (required_api_version.startswith('"') and required_api_version.endswith('"')):
    print_red("Internal error: unexpected format of API_VERSION line")
    exit()
required_api_version = required_api_version.strip('"')

from ram_concept.api_version import api_version
actual_api_version = api_version()
if required_api_version != actual_api_version:
    message = "Installed API version {0} does not match required API version {1}".format(actual_api_version, required_api_version)
    print_red(message)
    exit()

# CHECK FOR RUNNABLE RAM CONCEPT

try:
    import winreg
    path = r"Software\Bentley\Engineering\Concept\Integration"
    registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
except BaseException as e:
    print_red("There does not appear to be an installation of RAM Concept on this machine.")
    exit()

try:
    # get the path
    path_key_name = "LatestConceptExePath"
    path_value, path_registry_type = winreg.QueryValueEx(registry_key, path_key_name)
    if path_registry_type != winreg.REG_SZ:
        print_red("Unexpected problem: 'SOFTWARE\\Bentley\\Engineering\\Concept\\Integration\\LatestConceptExePath is not a registry SZ value'.")
        exit()

    # get the version
    # version is a int of the version number * 100: 3.2.1 becomes 321
    version_key_name = "LatestConceptExeVersion"
    version_value, version_registry_type = winreg.QueryValueEx(registry_key, version_key_name)
    winreg.CloseKey(registry_key)
    if version_registry_type != winreg.REG_DWORD:
        print_red("Unexpected problem: 'SOFTWARE\\Bentley\\Engineering\\Concept\\Integration\\LatestConceptExeVersion is not a registry DWORD value'.")
        exit()

except BaseException as e:
    print_red("Unknown registry error trying to find LatestConceptExeVersion.")
    print_red("The exception message below may provide some information:")
    print(str(e))
    exit()

# we need to check that the exe is at least that of the API
# convert version constant to registry value
from ram_concept.api_version import _version_string_to_registry_version
required_registry_version_constant = _version_string_to_registry_version(required_api_version)

if version_value < required_registry_version_constant:
    message1 = "RAM Concept version {0} or later is required to support the installed API".format(required_api_version)
    message2 = "Upgrade the RAM Concept installation on this machine to {0} or later.".format(required_api_version)
    message3 = "If you have installed RAM Concept {0} or later, you need to run it once for it to be available to the API.".format(required_api_version)
    print_red(message1)
    print_red(message2)
    print_red(message3)
    exit()

# as final test, run a concept server
try:
    from ram_concept.concept import Concept
    concept = Concept.start_concept(headless=True)
    concept.shut_down()
except BaseException as e:
    print_red("Unable to start RAM Concept.")
    print_red("The exception message below may provide some information:")
    print_red(str(e))
    exit()

print_green("Installation verified. You are ready to run Python scripts that use the RAM Concept API.")