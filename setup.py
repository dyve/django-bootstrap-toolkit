from setuptools import setup

setup(
    name='django-bootstrap-toolkit',
    version='2.6.23',
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
