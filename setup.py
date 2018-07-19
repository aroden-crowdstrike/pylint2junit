from setuptools import find_packages, setup

setup(
    name='pylint2junit',
    description='Converts pylint output to junit style test results',
    long_description=open('README.md').read(),
    author='andrew.roden@crowdstrike.com',
    author_email='andrew.roden@crowdstrike.com',
    url='',
    # excludes requires both a parent and children filter
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True, # if GIT committed; include
    setup_requires=[
        'setuptools_scm',
        'wheel',
    ],
    license="BSD",
    keywords='pylint',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'pylint2junit = pylint2junit.__main__:main',
        ]
    },
    install_requires=[
    ],
    tests_require=[
        'pylint',
    ],
    use_scm_version=True,
)
