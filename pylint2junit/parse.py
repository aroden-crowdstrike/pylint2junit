"""
Convert pylint report txt format to junit_types
"""
import re

from pylint2junit.junit_types import ModuleErrors, PyLintError

_MODULE_RE = re.compile(r'^\*{13} Module ([\w.]+)')

_REPORT_RE = re.compile(r'^-{67}')


def parse_input_lines(pylint_lines):
    """
    Parses input lines to objects that

    :param pylint_lines: lines to be parsed
    :type pylint_lines: list[str]

    :return: list of ModuleErrors objects
    :rtype: list[ModuleErrors]
    """
    cur_module = None
    cur_line_list = []
    for line in pylint_lines:
        # ignore empty lines
        if not (line and line.strip()):
            continue
        # once report section is hit; bail
        if _REPORT_RE.search(line):
            break
        # look fo a new module
        module = _MODULE_RE.search(line)
        if module:
            # yield current
            if cur_module:
                if cur_line_list:
                    cur_module.pylint_error_list.append(
                        _lines_to_pylint(cur_line_list)
                    )
                    cur_line_list = list()
                yield cur_module
            # new module
            cur_module = ModuleErrors(
                module_name=module.group(1),
                pylint_error_list=list(),
            )
        elif cur_module:
            # look for continue of last error
            if line.startswith(' '):
                cur_line_list.append(line)
            else:
                # record error start for new one
                if cur_line_list:
                    cur_module.pylint_error_list.append(
                        _lines_to_pylint(cur_line_list)
                    )
                cur_line_list = list()
                cur_line_list.append(line)
        else:
            raise NotImplementedError()
    if cur_module and cur_line_list:
        cur_module.pylint_error_list.append(
            _lines_to_pylint(cur_line_list)
        )
        yield cur_module


_PARSABLE_RE = re.compile(
    r'^(?P<path>[\w/.]+)'
    r':(?P<line>\d+)'
    r': \[(?P<msg_id>[^(]+)(?P<symbol>[^\]]*)\]'
    r' (?P<message>.*)'
)

_TEXT_RE = re.compile(
    r'^(?P<path>[\w/.]+)'
    r':(?P<line>\d+)'
    r':(?P<column>\d+)'
    r': (?P<msg_id>[^:]*)'
    r': (?P<message>[^(]*)'
    r'\((?P<symbol>[^)]*)\)'
)


def _lines_to_pylint(lines):
    match = _PARSABLE_RE.search(lines[0])
    if not match:
        match = _TEXT_RE.search(lines[0])
    if not match:
        raise NotImplementedError("Undetected format")
    path = match.group('path')
    line = match.group('line')
    msg_id = match.group('msg_id')
    message = "\n".join(
        [match.group('message')] + lines[1:],
    )
    symbol = match.group('symbol')
    return PyLintError(
        msg_id=msg_id,
        path=path,
        line=line,
        message=message,
        symbol=symbol,
    )
