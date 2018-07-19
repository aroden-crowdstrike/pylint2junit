"""
JunitReporter to be used as formatter

    pylint --output-format=pylint2junit.JunitReporter examplecode

Runnable script that can read pylint report output and produce
junit xml file.

    python -m pylint2junit \
        --input=pylint_results.txt \
        --output=pylint_results.txt
"""
from .junitreporter import JunitReporter
