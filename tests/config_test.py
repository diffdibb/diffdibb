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

import unittest

import mock
import pytest

import diffdibb.config
from diffdibb.config import DEFAULT_CONFIG_FILE, Cache


class LoadConfigurationTestCase(unittest.TestCase):
    """
    Tests for the diffdibb.config.load_configuration() function.
    """

    def setUp(self):
        diffdibb.config.reset()

        # mock of logging.RootLogger
        self.patch_get_logger = mock.patch('diffdibb.config.logging.getLogger', autospec=True)
        self.mock_get_logger = self.patch_get_logger.start()

        self.patch_root_logger = mock.patch('diffdibb.config.logging.RootLogger', autospec=True)
        self.mock_root_logger = self.patch_root_logger.start()
        self.mock_get_logger.return_value = self.mock_root_logger

        self.patch_path_exists = mock.patch('os.path', autospec=True)
        self.mock_path = self.patch_path_exists.start()

        self.patch_config_read = mock.patch('diffdibb.config.ConfigParser.read')
        self.mock_read = self.patch_config_read.start()

    def tearDown(self):
        self.patch_get_logger.stop()
        self.patch_root_logger.stop()
        self.patch_path_exists.stop()
        self.patch_config_read.stop()

    def test(self):
        """
        Test diffdibb.config.load_configuration() when configuration file exists.
        """
        self.mock_path.exists.return_value = True
        self.mock_path.isfile.return_value = True
        self.mock_read.return_value = None

        diffdibb.config.load_configuration()

        self.mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        self.mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)
        self.mock_read.assert_called_with(DEFAULT_CONFIG_FILE)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.info.assert_called_once_with(
            '%s configuration file was loaded.', DEFAULT_CONFIG_FILE)

    def test_nofile(self):
        """
        Test diffdibb.config.load_configuration() when the configuration file doesn't exist.
        """
        self.mock_path.exists.return_value = True
        self.mock_path.isfile.return_value = False
        self.mock_read.return_value = None

        with pytest.raises(ValueError):
            diffdibb.config.load_configuration()

        self.mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        self.mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)

        self.assertFalse(self.mock_read.readConfig.called)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.error.assert_called_once_with(
            '%s configuration file does not exist!' % DEFAULT_CONFIG_FILE)

    def test_errors(self):
        """
        Test diffdibb.config.load_configuration() when errors are raised.
        """
        self.mock_path.exists.return_value = True
        self.mock_path.isfile.return_value = True
        self.mock_read.side_effect = ValueError(123)

        with pytest.raises(ValueError):
            diffdibb.config.load_configuration()

        self.mock_path.exists.assert_called_once_with(DEFAULT_CONFIG_FILE)
        self.mock_path.isfile.assert_called_once_with(DEFAULT_CONFIG_FILE)

        self.assertFalse(self.mock_read.readConfig.called)

        self.assertTrue(self.mock_get_logger.called)
        self.mock_root_logger.error.assert_called_once_with(
            'Failed to load configuration from %s!', DEFAULT_CONFIG_FILE)
        self.mock_root_logger.debug.assert_called_once_with(
            str(ValueError(123)), exc_info=True)


class GetTestCase(unittest.TestCase):
    """
    Tests for the diffdibb.config.get() function.
    """

    def setUp(self):
        diffdibb.config.reset()

    @mock.patch('diffdibb.config.load_configuration', autospec=True)
    def test(self, mock_load):
        """
        Tests diffdibb.config.get() when no settings have been loaded.
        """
        default = {'key1': 'value1'}
        mock_load.return_value = default

        self.assertEquals(default, diffdibb.config.get())
        mock_load.assert_called_once_with()

    @mock.patch('diffdibb.config.load_configuration', autospec=True)
    def test_with_preloaded_settings(self, mock_load):
        """
        Tests diffdibb.source.config.get() when settings have been loaded.
        """
        default = {'key2': 'value2'}
        Cache.SETTINGS = default

        self.assertEquals(default, diffdibb.config.get())
        self.assertFalse(mock_load.called)


class ResetTestCase(unittest.TestCase):
    """
    Tests for the diffdibb.config.reset() function.
    """

    def setUp(self):
        diffdibb.config.reset()

    def test(self):
        """
        Tests diffdibb.config.reset().
        """
        default = {'key2': 'value2'}
        Cache.SETTINGS = default

        self.assertEquals(default, diffdibb.config.get())
        self.assertTrue(diffdibb.config.reset() is None)
        self.assertTrue(Cache.SETTINGS is None)
