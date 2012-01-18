import os
from setuptools import setup

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'
long_desc = open(root_dir + '/README.md').read()

setup(
    name='django-bootstrap-toolkit',
    version='1.0.1',
    url='https://github.com/dyve/django-bootstrap-toolkit',
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    license='Apache License 2.0',
    install_requires=['Django'],
    packages=['bootstrap_toolkit', 'bootstrap_toolkit.templatetags'],
    package_data={'bootstrap_toolkit': ['templates/bootstrap/*.html']},
    description='Bootstrap support for Django projects',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment",
        "Framework :: Django",
        ],
    long_description=long_desc,
)
