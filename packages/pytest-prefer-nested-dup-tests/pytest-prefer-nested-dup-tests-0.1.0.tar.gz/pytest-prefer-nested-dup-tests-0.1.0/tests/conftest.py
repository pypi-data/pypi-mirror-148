"""
tests/conftest.py (pytest-prefer-nested-dup-tests)
"""

################################################################################
#region Imports

#===============================================================================
#region stdlib

from typing import (
    Sequence,
    Union,
)

#endregion stdlib
#===============================================================================

#endregion Imports
################################################################################

pytest_plugins: Union[str, Sequence[str]] = ["pytester"]
