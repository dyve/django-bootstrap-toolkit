import re
from setuptools import setup

# Read version from file
VERSION_FILE = 'bootstrap_toolkit/_version.py'
version_text = open(VERSION_FILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, version_text, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

# Setup
setup(
    name='django-bootstrap-toolkit',
    version=version,
    url='https://github.com/dyve/django-bootstrap-toolkit',
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    license='Apache License 2.0',
    packages=['bootstrap_toolkit', 'bootstrap_toolkit.templatetags'],
    include_package_data=True,
    description='Bootstrap support for Django projects',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
    ],
)
