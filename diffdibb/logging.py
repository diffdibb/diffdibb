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
.. module:: diffdibb.logging
    :platform: Unix
    :synopsis: Logging utilities.

.. moduleauthor:: Pedro Salgado <steenzout@ymail.com>
"""

from __future__ import absolute_import


import logging
import logging.config as config

import os


DEFAULT_CONFIG_FILE = '/etc/diffdibb/logging.conf'


def load_configuration(config_file=DEFAULT_CONFIG_FILE):
    """
    Loads logging configuration from the given configuration file.

    :param config_file: the configuration file (default=/etc/source/logging.conf)
    :type config_file: str
    """
    if not os.path.exists(config_file) or not os.path.isfile(config_file):
        msg = '%s configuration file does not exist!', config_file
        logging.getLogger(__name__).error(msg)
        raise ValueError(msg)

    try:
        config.fileConfig(config_file, disable_existing_loggers=False)
        logging.getLogger(__name__).info('%s configuration file was loaded.', config_file)
    except StandardError as error:
        logging.getLogger(__name__).error('Failed to load configuration from %s!', config_file)
        logging.getLogger(__name__).debug(str(error), exc_info=True)
        raise error
