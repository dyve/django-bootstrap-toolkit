from setuptools import setup

setup(
    name='django-bootstrap-toolkit',
    version='1.0.7',
    url='https://github.com/dyve/django-bootstrap-toolkit',
    author='Dylan Verheul',
    author_email='dylan@dyve.net',
    license='Apache License 2.0',
#   install_requires=['Django'],
    packages=['bootstrap_toolkit', 'bootstrap_toolkit.templatetags'],
    include_package_data=True,
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
)
