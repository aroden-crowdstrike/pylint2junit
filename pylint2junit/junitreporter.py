"""
Pylint junit style reporter
"""
from __future__ import absolute_import, print_function

import collections
from datetime import datetime
import sys

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter

from pylint2junit import junit_types
from pylint2junit.tojunit import pylint_to_junit

EMPTY_RESULT = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite errors="0" failures="0" name="pylint" skipped="0" tests="0"
      time="0.000" timestamp="{timestamp}">
  </testsuite>
</testsuites>
"""


class _KeyDefaultDict(collections.defaultdict):
    def __init__(self, missing_function):
        collections.defaultdict.__init__(self)
        self._mia_fun = missing_function

    def __missing__(self, key):
        self[key] = value = self._mia_fun(key)
        return value


class JunitReporter(BaseReporter):
    """
    Report messages and layouts in junit

    https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd
    https://confluence.atlassian.com/bamboo/junit-parsing-in-bamboo
    -289277357.html
    """
    __implements__ = IReporter
    name = 'junit'
    extension = 'junit'

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)

        def _default(module_name):
            return junit_types.ModuleErrors(
                module_name=module_name,
                pylint_error_list=list(),
            )

        self._messages = _KeyDefaultDict(_default)

    def handle_message(self, msg):
        """
        For every message append to module's list
        """
        self._messages[msg.module].pylint_error_list.append(
            junit_types.PyLintError(
                msg_id=msg.msg_id,
                path=msg.path,
                line=msg.line,
                message=msg.msg,
                symbol=msg.symbol,
            )
        )

    def display_messages(self, _layout):
        """
        Output results to desired target
        """
        if self._messages:
            print(pylint_to_junit(self._messages.values()), file=self.out)
        else:
            empty_results = EMPTY_RESULT.format(
                timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            )
            print(empty_results, file=self.out)

    def display_reports(self, _layout):
        """
        Report not supported
        """
        pass

    def _display(self, _layout):
        """
        Just in case override; shouldn't be called because of display_reports
        """
        pass
