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

from os.path import normcase as nc
from unittest import TestCase

from test_utils import Mock, patch

from pybuilder.core import Project
from pybuilder.errors import BuildFailedException
from pybuilder.plugins.python.sonarqube_plugin import (
    SonarCommandBuilder,
    build_sonar_scanner,
    run_sonar_analysis,
)
from pybuilder.reactor import Reactor


class RunSonarAnalysisTest(TestCase):
    def setUp(self):
        self.project = Project("any-project")
        self.project.version = "0.0.1"
        self.project.set_property("sonarqube_project_key", "project_key")
        self.project.set_property("sonarqube_project_name", "project_name")
        self.project.set_property("dir_source_main_python", "src/main/python")
        self.project.set_property("dir_target", "target")
        self.project.set_property("dir_reports", "target/reports")
        self.reactor = Mock(Reactor)
        pyb_env = Mock()
        self.reactor.python_env_registry = {"pybuilder": pyb_env}

    def test_should_build_sonar_scanner_for_project(self):
        self.assertEqual(
            build_sonar_scanner(self.project, self.reactor).as_string,
            "sonar-scanner -Dsonar.projectKey=project_key "
            "-Dsonar.projectName=project_name "
            "-Dsonar.projectVersion=0.0.1 "
            "-Dsonar.sources=src/main/python "
            "-Dsonar.python.coverage.reportPath=%s"
            % nc("target/reports/coverage*.xml"),
        )

    @patch("pybuilder.plugins.python.sonarqube_plugin.SonarCommandBuilder.run")
    def test_should_break_build_when_sonar_scanner_fails(self, run_sonar_command):
        run_sonar_command.return_value = Mock(exit_code=1)

        self.assertRaises(
            BuildFailedException, run_sonar_analysis, self.project, Mock(), self.reactor
        )

    @patch("pybuilder.plugins.python.sonarqube_plugin.SonarCommandBuilder.run")
    def test_should_not_break_build_when_sonar_scanner_succeeds(
        self, run_sonar_command
    ):
        run_sonar_command.return_value = Mock(exit_code=0)

        run_sonar_analysis(self.project, Mock(), self.reactor)


class SonarCommandBuilderTests(TestCase):
    def setUp(self):
        self.project = Project("any-project")
        self.reactor = Mock()
        pyb_env = Mock()
        self.reactor.python_env_registry = {"pybuilder": pyb_env}
        self.reactor.pybuilder_venv = pyb_env

        self.project.set_property("any-property-name", "any-property-value")
        self.sonar_builder = SonarCommandBuilder("sonar", self.project, self.reactor)

    def test_should_set_sonar_key_to_specific_value(self):
        self.sonar_builder.set_sonar_key("anySonarKey").to("anyValue")

        self.assertEqual(self.sonar_builder.as_string, "sonar -DanySonarKey=anyValue")

    def test_should_set_sonar_key_to_two_specific_values(self):
        self.sonar_builder.set_sonar_key("anySonarKey").to("anyValue").set_sonar_key(
            "other"
        ).to("otherValue")

        self.assertEqual(
            self.sonar_builder.as_string,
            "sonar -DanySonarKey=anyValue -Dother=otherValue",
        )

    def test_should_set_sonar_key_to_property_value(self):
        self.sonar_builder.set_sonar_key("anySonarKey").to_property_value(
            "any-property-name"
        )

        self.assertEqual(
            self.sonar_builder.as_string, "sonar -DanySonarKey=any-property-value"
        )
