from __future__ import print_function
from setuptools import setup, find_packages
import os
import sys
import shutil
import glob

pkg_version = os.environ.get('PROJECT_VERSION')

setup(
    name='mediaflow',
    version=pkg_version,
    author='wingo.zwt',
    author_email='wingo.zwt@alibaba-inc.com',
    description='media streaming engine.',
    license='BSD',
    keywords='mediaflow',
    include_package_data=True,
    download_url='http://eas-public.oss-cn-hangzhou-zmf.aliyuncs.com/pkg/',
    packages=['mediaflow'],
    install_requires=[
        'numpy>=1.16', 'jinja2', 'requests', 'python-magic', 'graphviz==0.16'
    ],
    package_data={
        'mediaflow': ['*.so', '.lib/*', 'ops/*.py', 'jar/*.jar', 'include/*.h', 'include/*/*.h', 'include/*/*/*.h'],
    },
    entry_points={
        'console_scripts': ['local-run=mediaflow.local_run:main'],
    }
)
