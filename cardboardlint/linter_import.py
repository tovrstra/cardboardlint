# Cardboardlint is a cheap lint solution for pull requests.
# Copyright (C) 2011-2017 The Cardboardlint Development Team
#
# This file is part of Cardboardlint.
#
# Cardboardlint is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# Cardboardlint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Linter for import conventions.

This script counts the number of bad imports. The following is not allowed in a package:

* Importing from its own package as follows:

  .. code-block:: python

        from package import foo
"""

import codecs
from typing import List

from cardboardlint.common import Message, Linter


__all__ = ['linter_import']


DEFAULT_CONFIG = {
    # Filename filter rules
    'filefilter': ['- */test_*.py', '+ *.py', '+ *.pyx'],
    # Names of python packages in the project (no longer searched automatically).
    'packages': [],
}


def run_import(config: dict, filenames: List[str], _numproc: int = 1) -> List[Message]:
    """Linter for checking import statements.

    Parameters
    ----------
    config
        Dictionary that contains the configuration for the linter.
    filenames
        A list of filenames to check
    numproc
        The number of processors to use.

    Returns
    -------
    _messages
        The list of messages generated by the external linter.

    """
    # Loop all python and cython files
    messages = []
    if len(config['packages']) > 0:
        for filename in filenames:
            try:
                _check_file(filename, config, messages)
            except UnicodeDecodeError as err:
                messages.append(Message(filename, None, None, str(err)))
    return messages


def _check_file(filename: str, config: dict, messages: List[str]):
    """Look for bad imports in the given file.

    Parameters
    ----------
    filename
        File to be checked
    config
        Dictionary with configuration of the linters.
    messages
        A list of messages to append to. (output arg)

    """
    with codecs.open(filename, encoding='utf-8') as f:
        for lineno, line in enumerate(f):
            for package in config['packages']:
                # skip version import
                if line == u'from {0} import __version__\n'.format(package):
                    continue
                if u'from {0} import'.format(package) in line:
                    text = 'Wrong import from {0}'.format(package)
                    messages.append(Message(filename, lineno+1, None, text))


# pylint: disable=invalid-name
linter_import = Linter('import', run_import, DEFAULT_CONFIG, language='python')
