========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/softframe/badge/?style=flat
    :target: https://readthedocs.org/projects/softframe
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/softframe.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/softframe

.. |commits-since| image:: https://img.shields.io/github/commits-since/pcastanha/softframe/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/pcastanha/softframe/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/softframe.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/softframe

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/softframe.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/softframe

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/softframe.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/softframe


.. end-badges

Framework for data science activities

* Free software: BSD license

Installation
============

::

    pip install softframe

Documentation
=============

https://softframe.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
