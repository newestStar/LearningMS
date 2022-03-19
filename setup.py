# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in lms/__init__.py
from lms import __version__ as version

setup(
	name='lms',
	version=version,
	description='LMS App',
	author='Frappe',
	author_email='school@frappe.io',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
