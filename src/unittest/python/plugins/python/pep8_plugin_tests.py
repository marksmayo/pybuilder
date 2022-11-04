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

from unittest import TestCase

from test_utils import Mock

from pybuilder.core import Logger, Project
from pybuilder.plugins.python.pep8_plugin import (
    check_pep8_available,
    init_pep8_properties,
)


class CheckPep8AvailableTests(TestCase):
    def test_should_check_that_pylint_can_be_executed(self):
        mock_project = Mock(Project)
        mock_logger = Mock(Logger)

        reactor = Mock()
        pyb_env = Mock()
        reactor.python_env_registry = {"pybuilder": pyb_env}
        reactor.pybuilder_venv = pyb_env

        check_pep8_available(mock_project, mock_logger, reactor)

        expected_command_line = [
            "pep8",
        ]
        pyb_env.verify_can_execute.assert_called_with(
            expected_command_line, "pep8", "plugin python.pep8"
        )

    def test_should_set_dependency(self):
        mock_project = Mock(Project)
        init_pep8_properties(mock_project)
        mock_project.plugin_depends_on.assert_called_with("pep8")
