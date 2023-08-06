"""
pytest-prefer-nested-dup-tests/__impl.py
see pytest-prefer-nested-dup-tests.__init__.py
"""

################################################################################
#region Imports

#===============================================================================
#region stdlib

from typing import (
    cast,
    Dict,
    List,
    Optional,
)

#endregion stdlib
#===============================================================================

#===============================================================================
#region third party

import _pytest.config
import _pytest.fixtures
import pytest

#endregion third party
#===============================================================================

#endregion Imports
################################################################################

################################################################################
#region Public Classes


#===============================================================================
class ExtendedItem(pytest.Item):
    """
    ExtendedItem adds prefer_nested_dup_tests__parent_depth to pytest.Item.
    """

    prefer_nested_dup_tests__parent_depth: int

#endregion Public Classes
################################################################################

################################################################################
#region Public Hooks


#===============================================================================
def pytest_configure(config: _pytest.config.Config) -> None:
    """
    pytest_configure hook to forcibly enable keepduplicates option.

    _extended_summary_

    Args:
        config (_pytest.config.Config): current pytest config to modify
    """

    config.option.keepduplicates = True


#===============================================================================
def pytest_collection_modifyitems(
    session: pytest.Session,
    config: _pytest.config.Config,
    items: List[ExtendedItem],
) -> None:
    """
    pytest_collection_modifyitems hook to drop non-package versions of duplicate
    tests.

    Args:
        session (pytest.Session): current pytest Session
        config (_pytest.config.Config): current pytest Config
        items (List[ExtendedItem]): list of discovered tests
    """

    session = session  # ignore unused var warning

    seen_best_nodes: Dict[str, ExtendedItem] = {}

    for item in items:
        item.prefer_nested_dup_tests__parent_depth = 0
        parent: Optional[ExtendedItem] = cast(Optional[ExtendedItem], item.parent)
        while parent is not None:
            item.prefer_nested_dup_tests__parent_depth = (
                item.prefer_nested_dup_tests__parent_depth + 1
            )
            parent = cast(Optional[ExtendedItem], parent.parent)
        if item.nodeid not in seen_best_nodes.keys():
            seen_best_nodes[item.nodeid] = item
        else:
            if (
                item.prefer_nested_dup_tests__parent_depth
                > seen_best_nodes[item.nodeid].prefer_nested_dup_tests__parent_depth
            ):
                seen_best_nodes[item.nodeid] = item

    new_items = list(seen_best_nodes.values())

    items[:] = new_items

    # fix how many items we report in terminal output b/c we do not "deselect"
    # our removed duplicates (intentionally)
    terminal_plugin = config.pluginmanager.get_plugin("terminalreporter")
    terminal_plugin._numcollected = len(items)
    terminal_plugin.report_collect()

#endregion Public Hooks
################################################################################
