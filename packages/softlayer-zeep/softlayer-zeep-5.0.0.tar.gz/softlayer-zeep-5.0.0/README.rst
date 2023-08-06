Zeep: Python SOAP client
========================

A fast and modern Python SOAP client

Highlights:
 * Compatible with Python 3.8, 3.9, 3.10 and PyPy3
 * Build on top of lxml and requests
 * Support for Soap 1.1, Soap 1.2 and HTTP bindings
 * Support for WS-Addressing headers
 * Support for WSSE (UserNameToken / x.509 signing)
 * Support for asyncio using the httpx module
 * Experimental support for XOP messages


Please see for more information the documentation at
https://readthedocs.org/projects/python-zeep

This project is a fork of https://github.com/mvantellingen/python-zeep and exists to handle quirks in the SoftLayer API that might not be suitable to add upstream.

.. start-no-pypi

Status
------

.. image:: https://readthedocs.org/projects/python-zeep/badge/?version=latest
    :target: https://readthedocs.org/projects/python-zeep/

.. image:: https://github.com/softlayer/softlayer-zeep/workflows/Python%20Tests/badge.svg
    :target: https://github.com/softlayer/softlayer-zeep/actions?query=workflow%3A%22Python+Tests%22

.. image:: http://codecov.io/github/softlayer/softlayer-zeep/coverage.svg?branch=master
    :target: http://codecov.io/github/softlayer/softlayer-zeep?branch=master

.. image:: https://img.shields.io/pypi/v/softlayer-zeep.svg
    :target: https://pypi.python.org/pypi/softlayer-zeep/

.. end-no-pypi

Installation
------------

.. code-block:: bash

    pip install softlayer-zeep


Zeep uses the lxml library for parsing xml. See https://lxml.de/installation.html for the installation requirements.

Usage
-----
.. code-block:: python

    from zeep import Client

    client = Client('tests/wsdl_files/example.rst')
    client.service.ping()


To quickly inspect a WSDL file use::

    python -m zeep <url-to-wsdl>


Please see the documentation at http://docs.python-zeep.org for more
information.


Support
=======

Open an issue here: https://github.com/softlayer/softlayer-zeep/issues

If you want to report a bug then please first read
http://docs.python-zeep.org/en/master/reporting_bugs.html

Please only report bugs and not support requests to the GitHub issue tracker.
