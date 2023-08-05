# coding: utf-8
#
# This code is part of pyrekordbox.
#
# Copyright (c) 2022, Dylan Jones

"""This module contains common constants and methods used in other modules.

Contains all the path and settings handling of the Rekordbox installation(s) on
the users machine.
"""

import os
import sys
import json
import logging
import xml.etree.cElementTree as xml

logger = logging.getLogger(__name__)


def _read_config_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".cfg":
        from configparser import ConfigParser

        parser = ConfigParser()
        parser.read(path)
        return parser
    elif ext == ".toml":
        import toml

        return toml.load(path)
    elif ext in (".yaml", ".yml"):
        import yaml

        with open(path, "r") as stream:
            return yaml.safe_load(stream)
    return dict()


def read_pyrekordbox_configuration():
    """Reads the pyrekordbox configuration.

    So far only the `pioneer-install-dir` and `pioneer-app-dir` fileds in the
    `rekordbox` section are supported. Supported configuration files are
    pyproject.toml, setup.cfg, rekordbox.toml, rekordbox.cfg and rekordbox.yml.
    The files are searched for in that order.

    Returns
    -------
    pyrekordbox_config : dict
        The pyrekordbox configuration data, if found.
    """
    files = ["pyproject.toml", "setup.cfg"]
    for ext in [".toml", ".cfg", ".yaml", ".yml"]:
        files.append("rekordbox" + ext)

    for file in files:
        try:
            data = _read_config_file(file)
            config = dict(data["rekordbox"])
        except (ImportError, FileNotFoundError, KeyError):
            pass
        else:
            if config:
                return config
    return dict()


def get_pioneer_app_dir(path=""):
    """Returns the path of the Pioneer application data directory.

    On Windows, the Pioneer application data is stored in `/Users/user/AppData/Roaming`
    On macOS the application data is somewhere in `~/Libary/Application Support`.

    Parameters
    ----------
    path : str, optional
        If a path is given it will only be checked for validity. Otherwise,
        the default Pioneer directory will be constructed and checked.

    Returns
    -------
    pioneer_path : str
        The path to the Pioneer application data.
    """
    if not path:
        if sys.platform == "win32":
            # Windows: located in /Users/user/AppData/Roaming/
            app_data = os.environ["AppData"]
        elif sys.platform == "darwin":
            # MacOS: located in ~/Library/Application Support/
            home = os.path.expanduser("~")
            app_data = os.path.join(home, "Library", "Application Support")
        else:
            # Linux: not supported
            logger.warning(f"OS {sys.platform} not supported!")
            app_data = ""

        # Pioneer app data
        path = os.path.join(app_data, "Pioneer")

    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"The Pioneer app-dir {path} does not exist!")

    return path


def get_pioneer_install_dir(path=""):
    """Returns the path of the Pioneer program installation directory.

    On Windows, the Pioneer program data is stored in `/ProgramFiles/Pioneer`
    On macOS the program data is somewhere in `/Applications/`.

    Parameters
    ----------
    path : str, optional
        If a path is given it will only be checked for validity. Otherwise,
        the default Pioneer directory will be constructed and checked.

    Returns
    -------
    pioneer_path : str
        The path to the Pioneer program installation data.
    """
    if not path:
        if sys.platform == "win32":
            # Windows: located in /ProgramFiles/Pioneer
            program_files = os.environ["ProgramFiles"].replace("(x86)", "").strip()
            path = os.path.join(program_files, "Pioneer")
        elif sys.platform == "darwin":
            # MacOS: located in /Applications/
            path = os.path.abspath("/Applications")
        else:
            # Linux: not supported
            logger.warning(f"OS {sys.platform} not supported!")

    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"The Pioneer install-dir {path} does not exist!")

    return path


def _convert_type(s):
    # Try to parse as int, float, list of int, list of float
    types_ = int, float
    for type_ in types_:
        try:
            return type_(s)
        except ValueError:
            pass
        try:
            return [type_(x) for x in s.split(",")]
        except ValueError:
            pass

    return s


def read_rekordbox_settings(rekordbox_app_dir):
    """Finds and parses the 'rekordbox3.settings' file in the Rekordbox 5 or 6 app-dir.

    The settings file usually is called 'rekordbox3.settings' and is
    located in the application data directory of the corresponding Rekordbox
    (major) version.

    Parameters
    ----------
    rekordbox_app_dir : str
        The path of the application-data directory of Rekordbox 5 or 6.

    Returns
    -------
    settings : dict
        The parsed Rekordbox settings data.
    """
    # Get path of the settings file
    file_name = "rekordbox3.settings"
    path = os.path.join(rekordbox_app_dir, file_name)
    # if not os.path.exists(path):
    #    raise FileNotFoundError(f"No '{file_name}' file in '{rekordbox_app_dir}'.")

    # Parse the settings file
    settings = dict()
    tree = xml.parse(path)
    for element in tree.findall("VALUE"):
        name = element.attrib["name"]
        try:
            val = _convert_type(element.attrib["val"])
        except KeyError:
            device_setup = element.find("DEVICESETUP")
            val = {k: _convert_type(v) for k, v in device_setup.attrib.items()}
        settings[name] = val
    return settings


def read_rekordbox6_options(pioneer_app_dir):
    """Finds and parses the Rekordbox 6 `options.json` file with additional settings.

    The options file contains additional settings used by Rekordbox 6, for example the
    path of the new `master.db` database. It also contains some data nedded to open
    the database, which is encrypted using SQLCipher.

    Parameters
    ----------
    pioneer_app_dir : str, optional
        The path of the Pioneer application data.

    Returns
    -------
    options : dict
        The parsed rekordbox 6 options data.
    """
    # Get path of the options file
    opt_path = os.path.join(
        pioneer_app_dir, "rekordboxAgent", "storage", "options.json"
    )

    # Read and parse the options file
    with open(opt_path, "r") as fh:
        data = json.load(fh)
    options = dict()
    for key, value in data["options"]:
        options[key] = value

    return options


def read_rekordbox6_asar(rb6_install_dir):
    """Finds and parses the Rekordbox 6 `app.asar` archive file.

    An ASAR file is an archive used to package source code for an application
    using Electron. Rekordbox 6 stores some useful information for opening the
    new `master.db` database in this file.

    Parameters
    ----------
    rb6_install_dir : str
        The path of the Rekordbox 6 installation directory.

    Returns
    -------
    asar_data : str
        The data of the Rekordbox 6 `app.asar` archive file as ANSI encoded string.
    """
    # Find location of app asar file
    if sys.platform == "win32":
        location = os.path.join(
            rb6_install_dir, "rekordboxAgent-win32-x64", "resources"
        )
    elif sys.platform == "darwin":
        root = os.path.join(rb6_install_dir, "rekordbox.app", "Contents", "MacOS")
        location = os.path.join(root, "rekordboxAgent.app", "Contents", "Resources")
    else:
        raise logger.warning(f"OS {sys.platform} not supported!")

    # Read asar file
    path = os.path.abspath(os.path.join(location, "app.asar"))
    with open(path, "rb") as fh:
        data = fh.read().decode("ANSI")

    return data
