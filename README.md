pylint2junit
============
Provides junit xml from either `pylint --output-format=pylint2junit.JunitReporter`
or a shell script to convert pylint text/parsable output to an xml file.


Install
-------

    pip install pylint2junit

Usage
-----

Output formatter

    pylint --output-format=pylint2junit.JunitReporter example

Conversion script

    pylint --output-format=parseable example > pylint_results.txt
    pylint2junit --input=pylint_results.txt --output=pylint_results.txt


Building
--------

Validate no pylint problem

     pylint pylint2junit tests

Build

    python setup.py bdsit_wheel
