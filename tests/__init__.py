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
.. module:: diffdibb.tests
    :platform: Unix
    :synopsis:

.. moduleauthor:: Pedro Salgado <steenzout@ymail.com>
"""

import os
import logging
import unittest

import diffdibb.config
import diffdibb.logging


LOGGING_CONFIG_FILE = '%s/tests/logging.conf' % os.curdir
PACKAGE_CONFIG_FILE = '%s/tests/diffdibb.cfg' % os.curdir


class Basic(object):
    """
    Basic functionality to enhance test cases.
    """

    def setup_configuration(self):
        """
        Setup test configuration.
        It will also load (once) the test configuration.
        """
        logging.getLogger('%s.%s' % (__name__, 'Basic')).info('setup_configuration()')

        diffdibb.config.reset()
        diffdibb.config.load_configuration(PACKAGE_CONFIG_FILE)

        self.configuration = diffdibb.config.get()

    def setup_logger(self):
        """
        Setup test logger.
        It will also load (once) the test logging configuration.
        """
        logging.getLogger('%s.%s' % (__name__, 'Basic')).info('setup_logger()')

        diffdibb.logging.load_configuration(LOGGING_CONFIG_FILE)

        self.logger = logging.getLogger('%s.%s' % (__name__, self.__class__.__name__))


class BaseTestCase(unittest.TestCase, Basic):
    """
    Base test case.
    """

    __slots__ = ('configuration', 'logger')

    def __init__(self, methodName):
        """
        Initializes a BaseTestCase instance.

        :param methodName: the test method to be executed.
        :type methodName: str
        """
        super(BaseTestCase, self).__init__(methodName)

        self.setup_logger()
        self.setup_configuration()

    def setUp(self):
        """
        Setup test resources.
        """
        self.logger.info('setUp()')

    def tearDown(self):
        """
        Tear down test resources.
        """
        self.logger.info('tearDown()')
