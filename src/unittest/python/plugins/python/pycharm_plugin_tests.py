#   -*- coding: utf-8 -*-
#
#   This file is part of PyBuilder
#
#   Copyright 2011-2020 PyBuilder Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

try:
    TYPE_FILE = file
except NameError:
    from io import FileIO as TYPE_FILE

import unittest
from os import sep

from test_utils import MagicMock, Mock, patch

from pybuilder.core import Project
from pybuilder.plugins.python.pycharm_plugin import (
    _ensure_directory_present,
    pycharm_generate,
)
from pybuilder.utils import jp, np


class PycharmPluginTests(unittest.TestCase):
    @patch("pybuilder.plugins.python.pycharm_plugin.os")
    def test_should_create_pycharm_directory_if_not_present(self, os):
        os.path.exists.return_value = False

        _ensure_directory_present("foo")

        os.makedirs.assert_called_with("foo")

    @patch("pybuilder.plugins.python.pycharm_plugin.os")
    def test_should_not_create_pycharm_directory_if_present(self, os):
        os.path.exists.return_value = True

        _ensure_directory_present("foo")

        self.assertFalse(os.makedirs.called)

    @patch("pybuilder.plugins.python.pycharm_plugin.open", create=True)
    @patch("pybuilder.plugins.python.pycharm_plugin.os")
    def test_should_write_pycharm_file(self, os, mock_open):
        project = Project("basedir", name="pybuilder")
        project.set_property("dir_source_main_python", "src/main/python")
        project.set_property("dir_source_unittest_python", "src/unittest/python")
        project.set_property(
            "dir_source_integrationtest_python", "src/integrationtest/python"
        )
        project.set_property("dir_target", "build")
        mock_open.return_value = MagicMock(spec=TYPE_FILE)
        os.path.join.side_effect = lambda first, second: first + sep + second

        pycharm_generate(project, Mock())

        mock_open.assert_called_with(
            np(jp(project.basedir, ".idea/pybuilder.iml")), "w"
        )
        metadata_file = mock_open.return_value.__enter__.return_value
        metadata_file.write.assert_called_with(
            """<?xml version="1.0" encoding="UTF-8"?>
<!-- This file has been generated by the PyBuilder PyCharm Plugin -->

<module type="PYTHON_MODULE" version="4">
  <component name="NewModuleRootManager">
    <content url="file://$MODULE_DIR$">
      <sourceFolder url="file://$MODULE_DIR$/src/main/python" isTestSource="false" />
      <sourceFolder url="file://$MODULE_DIR$/src/unittest/python" isTestSource="true" />
      <sourceFolder url="file://$MODULE_DIR$/src/integrationtest/python" isTestSource="true" />
      <excludeFolder url="file://$MODULE_DIR$/.pybuilder" />
      <excludeFolder url="file://$MODULE_DIR$/build" />
    </content>
    <orderEntry type="inheritedJdk" />
    <orderEntry type="sourceFolder" forTests="false" />
  </component>
  <component name="PyDocumentationSettings">
    <option name="myDocStringFormat" value="Plain" />
  </component>
  <component name="TestRunnerService">
    <option name="projectConfiguration" value="Unittests" />
    <option name="PROJECT_TEST_RUNNER" value="Unittests" />
  </component>
</module>"""
        )
