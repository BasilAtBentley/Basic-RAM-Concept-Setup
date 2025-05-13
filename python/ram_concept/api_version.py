#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------

# DEVELOPMENT_API_VERSION is expected to only be used in development environments
DEVELOPMENT_API_VERSION = "99.99.0"

def api_version()->str:
    """Returns the API Version string (e.g. "8.2.0").
    API versions always match the concept.exe version the API was released with."""

    try:
        # this will raise an exception if version_constant.py cannot be found
        from .version_constant import API_VERSION
        return API_VERSION
    except:
        return DEVELOPMENT_API_VERSION


def _matching_registry_exe_version()->int:
    """Returns the concept.exe version that matches the API version.
    e.g. 820 is returned for API version "8.2.0" """
    return _version_string_to_registry_version(api_version())


def _version_string_to_registry_version(version_string: str)->int:
    """Converts the 3-number version string ("8.2.0") to matching registry value (820). """
    three_version_numbers = version_string.split(".")
    assert len(three_version_numbers) == 3

    major = int(three_version_numbers[0])
    minor = int(three_version_numbers[1])
    micro = int(three_version_numbers[2])

    exe_version = (major * 100) + (minor * 10) + (micro * 1)
    return exe_version
