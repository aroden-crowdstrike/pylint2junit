"""
Types to abstract input format
"""
import collections

ModuleErrors = collections.namedtuple(
    '_Module_Errors',
    [
        'module_name',
        'pylint_error_list',
    ]
)
PyLintError = collections.namedtuple(
    '_PyLintError',
    [
        'msg_id',
        'path',
        'line',
        'message',
        'symbol',
    ]
)
