"""
pytest-prefer-nested-dup-tests

by Marximus Maximus (https://www.marximus.com)

A Pytest plugin to drop duplicated tests during collection, but will prefer
keeping nested packages.

By default, when de-duplicating tests, all sub-packages become top level packages.
This plugin keeps the subpackage structure intact.
"""  # noqa: D400

################################################################################
#region import

#===============================================================================
#region ours

from .__impl import *  # noqa: F401, F403

#endregion ours
#===============================================================================

#endregion import
################################################################################
