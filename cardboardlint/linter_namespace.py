"""Linter for namespace collisions.

This script imports every module in HORTON and checks for overlapping name spaces
"""
import os
import sys
import importlib
from cardboardlint.common import Message, get_filenames


def linter_namespace(config, files_lines):
    """Linter for checking namespace statements.

    Parameters
    ----------
    config : dict
        Dictionary that contains the configuration for the linter
    files_lines : dict
        Dictionary of filename to the set of line numbers (that have been modified).
        See `run_diff` method in `carboardlint`
    """
    messages = []

    # Make sure we test the source tree and not some locally installed copy of HORTON.
    sys.path.insert(0, '.')

    # Find all module names and load namespaces
    namespace = {}
    for filename in get_filenames(config['directories'], config['include'], config['exclude'],
                                  files_lines=files_lines):
        # remove extension and replace / by .
        modulename = os.path.splitext(filename)[0].replace('/', '.')

        # Check all public names of the module.
        module = importlib.import_module(modulename)
        names = dir(module)
        if '__all__' in names:
            for name in names:
                if name in module.__all__:
                    namespace.setdefault(name, []).append(modulename)
                    if name in config['exclude']:
                        messages.append(Message(filename, None, None,
                                                'Invalid name in namespace: {0}'.format(name)))
        else:
            messages.append(Message(filename, None, None, 'Missing __all__'))

    # Detect collisions
    for name, modules in namespace.items():
        if len(modules) > 1:
            text = "Name '{0}' found in modules {1}".format(name, ' '.join(modules))
            messages.append(Message(None, None, None, text))
    return messages
