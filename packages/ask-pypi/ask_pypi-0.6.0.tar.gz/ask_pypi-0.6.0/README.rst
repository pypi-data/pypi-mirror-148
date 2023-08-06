ASK PYPI
========

Ask PyPI about whether a Python Package has alread been released/registered under a given name.

.. start-badges

| |build| |release_version| |wheel| |supported_versions| |commits_since_specific_tag_on_master| |commits_since_latest_github_release|


|
| **Source Code:** https://github.com/boromir674/ask-pypi
| **Pypi Package:** https://pypi.org/project/ask_pypi/
|


.. Test Workflow Status on Github Actions for specific branch <branch>

.. |build| image:: https://img.shields.io/github/workflow/status/boromir674/ask-pypi/Test%20Python%20Package/master?label=build&logo=github-actions&logoColor=%233392FF
    :alt: GitHub Workflow Status (branch)
    :target: https://github.com/boromir674/ask-pypi/actions/workflows/test.yaml?query=branch%3Amaster

.. above url to workflow runs, filtered by the specified branch

.. |release_version| image:: https://img.shields.io/pypi/v/ask_pypi
    :alt: Production Version
    :target: https://pypi.org/project/ask_pypi/

.. |wheel| image:: https://img.shields.io/pypi/wheel/ask-pypi?color=green&label=wheel
    :alt: PyPI - Wheel
    :target: https://pypi.org/project/ask_pypi

.. |supported_versions| image:: https://img.shields.io/pypi/pyversions/ask-pypi?color=blue&label=python&logo=python&logoColor=%23ccccff
    :alt: Supported Python versions
    :target: https://pypi.org/project/ask_pypi

.. |commits_since_specific_tag_on_master| image:: https://img.shields.io/github/commits-since/boromir674/ask-pypi/v0.6.0/master?color=blue&logo=github
    :alt: GitHub commits since tagged version (branch)
    :target: https://github.com/boromir674/ask-pypi/compare/v0.6.0..master

.. |commits_since_latest_github_release| image:: https://img.shields.io/github/commits-since/boromir674/ask-pypi/latest?color=blue&logo=semver&sort=semver
    :alt: GitHub commits since latest release (by SemVer)


Features
========


1. **ask_pypi** `python package`

   a. **is-pypi-package** cli to check PyPI about a given package

2. **Test Suite** using `Pytest`
3. **Parallel Execution** of Unit Tests, on multiple cpu's
4. **Automation**, using `tox`

   a. **Code Coverage** measuring
   b. **Build Command**, using the `build` python package
   c. **Pypi Deploy Command**, supporting upload to both `pypi.org` and `test.pypi.org` servers
   d. **Type Check Command**, using `mypy`
5. **CI Pipeline**, running on `Github Actions`

   a. **Job Matrix**, spanning different `platform`'s and `python version`'s

      1. Platfroms: `ubuntu-latest`, `macos-latest`
      2. Python Iterpreters: `3.6`, `3.7`, `3.8`, `3.9`, `3.10`
   b. **Parallel Job** execution, generated from the `matrix`, that runs the `Test Suite`



Quickstart
==========

Using `pip` is the approved way for installing `ask_pypi`.

.. code-block:: sh

    python3 -m pip install --user ask_pypi


Usage
-----

Open a console (ie terminal) and run:

.. code-block:: sh

    is-pypi-package so-magic

    echo $?

Observer that the exit code is 0, since there IS a package named `so-magic` on pypi.org.

.. code-block:: sh

    is-pypi-package ubaspidfbpasuidbf

    echo $?

Observer that the exit code is 1, since there is NOT a package named `ubaspidfbpasuidbf` on pypi.org.


License
=======

* Free software: Affero GNU General Public License v3.0
