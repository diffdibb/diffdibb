# -*- coding: utf-8 -*-
#
#   diffdibb : tools to audit databases.
#
# Copyright (C) 2015, diffdibb
# https://github.com/diffdibb
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
.. module:: diffdibb.config
    :platform: Unix
    :synopsis: Configuration utilities.

.. moduleauthor:: Pedro Salgado <steenzout@ymail.com>
"""

from __future__ import absolute_import

import os.path

try:
    from ConfigParser import SafeConfigParser as ConfigParser
except ImportError:
    from configparser import ConfigParser

import logging


DEFAULT_CONFIG_FILE = '/etc/diffdibb/diffdibb.cfg'


class Cache(object):
    SETTINGS = None


def load_configuration(config_file=DEFAULT_CONFIG_FILE):
    """
    Loads configuration.

    :param config_file: the configuration file(s).
    :type config_file: str or list of str
    """
    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        msg = '%s configuration file does not exist!' % config_file
        logging.getLogger(__name__).error(msg)
        raise ValueError(msg)

    parser = ConfigParser()
    try:
        parser.read(config_file)
        Cache.SETTINGS = {}
        for section in parser.sections():
            Cache.SETTINGS[section] = dict(parser.items(section))
        logging.getLogger(__name__).info('%s configuration file was loaded.', config_file)
        return Cache.SETTINGS
    except StandardError as error:
        SETTINGS = None
        logging.getLogger(__name__).error('Failed to load configuration from %s!', config_file)
        logging.getLogger(__name__).debug(str(error), exc_info=True)
        raise error


def get():
    """
    Returns the configuration.

    :return: the configuration.
    :rtype: object (configParser.ConfigParser)
    """
    if Cache.SETTINGS is None:
        return load_configuration()
    return Cache.SETTINGS


def reset():
    """
    Reset the configuration.
    """
    Cache.SETTINGS = None
