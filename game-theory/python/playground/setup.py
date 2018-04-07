# Copyright 2018 ELIFE. All rights reserved.
# Use of this source code is governed by a MIT
# license that can be found in the LICENSE file.

from setuptools import setup

with open("README.rst") as handle:
    README = handle.read()

with open("LICENSE") as handle:
    LICENSE = handle.read()

setup(
    name='playground',
    version='0.0.0',
    description='Playing Games on a Graph',
    long_description=README,
    maintainer='Douglas G. Moore',
    maintainer_email='doug@dglmoore.com',
    url='https://github.com/elife-asu/meet-julia',
    license=LICENSE,
    requires=[],
    packages=[],
    package_data={},
    test_suite='test',
    platforms=['Windows', 'OS X', 'Linux']
)
