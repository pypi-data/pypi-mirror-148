"""
tests/deeptest/deepertest/test___impl.py (pytest-prefer-nested-dup-tests)
"""

################################################################################
#region Imports

#===============================================================================
#region stdlib

from typing import (
    Any,
)

#endregion stdlib
#===============================================================================

#endregion Imports
################################################################################

################################################################################
#region Types

PytestFixture = Any

#endregion Types
################################################################################

################################################################################
#region Tests


#===============================================================================
def test___main(testdir: PytestFixture) -> None:
    """
    test___main: simple test to confirm this subpackage of tests loads

    Args:
        testdir (PytestFixture):
    """

    testdir = testdir  # ignore unused arg in sig
    assert True

#endregion Tests
################################################################################
