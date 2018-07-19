"""
Given pylint2junit.junit_types provide XML as string
"""

from functools import reduce
from xml.etree import ElementTree as ET

def pylint_to_junit(modules):
    """
    Given ouptut of pylint in a file writes out a new XML file in junit format
    for parsing by a CI server.

    https://github.com/windyroad/JUnit-Schema/blob/master/JUnit.xsd

    https://confluence.atlassian.com/bamboo/junit-parsing-in-bamboo-289277357.html

    :param modules: list of modules to output pylint for
    :type modules: List[junit_types.ModuleErrors]

    :return: string of xml
    :rtype: str
    """
    modules = list(modules)

    # boiler plate elements
    failure_cnt = reduce(
        lambda cnt, m: cnt + len(m.pylint_error_list),
        modules,
        0,
    )
    suite = ET.Element(
        "testsuite",
        name="pylint",
        errors="0",
        tests=str(len(modules)),
        time="0.0",
        failures=str(failure_cnt)
    )
    props = ET.SubElement(
        suite,
        'properties',
    )
    ET.SubElement(
        props,
        'property',
        name='converted_by',
        value='pylint2junit',
    )

    # each module has a testcase with many failures
    for module_error in modules:
        _module_errors_to_junit_test_case(module_error, suite)

    # write completed xml output
    return u'<?xml version="1.0" encoding="UTF-8" ?>{}'.format(ET.tostring(
        suite,
        encoding="utf-8",
        method="xml",
        #pretty_print=True,
    ).decode('utf-8'))

def _module_errors_to_junit_test_case(module_error, suit_xml_section):
    """
    Given ModuleError writes a test_case section section to a suit_xml section

    :param module_error:
    :type module_error: ModuleErrors

    :param suit_xml_section: xml context element
    :type suit_xml_section: ET.Element
    """
    test_case = ET.SubElement(
        suit_xml_section,
        "testcase",
        name="{}".format(module_error.module_name),
        time="0.0",
    )
    for error in module_error.pylint_error_list:
        elm = ET.SubElement(
            test_case,
            "failure",
            type="{code}: {msg}".format(
                code=error.msg_id,
                msg=error.symbol,
            ),
            message="{file}:{line}".format(
                file=error.path,
                line=error.line,
            ),
        )
        # new line helps some CI's be more pretty
        elm.text = "{}\n".format(
            error.message.strip() if error.message else ''
        )
