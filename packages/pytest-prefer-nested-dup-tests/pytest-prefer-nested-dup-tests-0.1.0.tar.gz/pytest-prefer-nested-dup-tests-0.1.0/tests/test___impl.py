"""
tests/test___impl.py (pytest-prefer-nested-dup-tests)
"""

################################################################################
#region Imports

#===============================================================================
#region stdlib

import sys
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


def test___main(testdir: PytestFixture) -> None:
    """
    test___main: simple test to confirm this subpackage of tests loads

    Args:
        testdir (PytestFixture):
    """

    testdir = testdir  # ignore unused arg in sig
    assert True


def test_drop_duplicated_dir(testdir: PytestFixture) -> None:
    """
    test_drop_duplicated_dir tests if same toplevel dir is found twice

    Args:
        testdir (PytestFixture):
    """

    testdir.makepyfile(
        """
        def test_foo():
            pass
        """,
    )
    result = testdir.runpytest(".", ".", "-p", "no:sugar")
    result.stdout.fnmatch_lines(
        [
            "* 1 passed in *",
        ],
    )
    assert result.ret == 0


def test_drop_duplicated_pkg(testdir: PytestFixture) -> None:
    """
    test_drop_duplicated_pkg tests if same toplevel package is found twice


    Args:
        testdir (PytestFixture):
    """

    testdir.makepyfile(
        **{
            "pkg/__init__.py": "",
            "pkg/test_foo.py": """
                def test_foo():
                    pass
            """,
        },
    )
    result = testdir.runpytest("pkg", "pkg", "-p", "no:sugar")
    result.stdout.fnmatch_lines(
        [
            "* 1 passed in *",
        ],
    )
    assert result.ret == 0


def test_drop_duplicated_files(testdir: PytestFixture) -> None:
    """
    test_drop_duplicated_files tests if same toplevel file is found twice

    Args:
        testdir (PytestFixture):
    """

    testdir.makepyfile(
        **{
            "tests/test_bar.py": """
                def test_bar():
                    pass
            """,
            "tests/test_foo.py": """
                def test_foo():
                    pass
            """,
        },
    )
    result = testdir.runpytest("tests/test_foo.py", "tests", "-v", "-p", "no:sugar")
    result.stdout.fnmatch_lines(
        [
            "tests/test_foo.py::test_foo *",
            "tests/test_bar.py::test_bar *",
            "* 2 passed *",
        ],
    )
    assert result.ret == 0


def test_nested_package(testdir: PytestFixture) -> None:
    """
    test_nested_package tests finding nested packages and reporting them as nested

    Args:
        testdir (PytestFixture): _description_
    """

    # we need to hide our own "tests" module in order for this to work when
    #   testing ourself.
    sys_modules_tests_old = sys.modules.get("tests")
    del sys.modules["tests"]

    # do the real test in a try so that we can fix up sys.modules later
    try:
        testdir.makepyfile(
            **{
                "tests/__init__.py": "",
                "tests/foo/__init__.py": "",
                "tests/foo/test_foo.py": """
                            def test_foo():
                                pass
                        """,
                "tests/bar/__init__.py": "",
                "tests/bar/test_bar.py": """
                            def test_bar():
                                pass
                        """,
            },
        )

        result = testdir.runpytest(".", "-v", "--collect-only", "-p", "no:sugar")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "<Package tests>",
                "  <Package bar>",
                "    <Module test_bar.py>",
                "      <Function test_bar>",
                "  <Package foo>",
                "    <Module test_foo.py>",
                "      <Function test_foo>",
            ],
        )
        assert result.ret == 0

        result = testdir.runpytest(".", "-v", "-p", "no:sugar")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "tests/bar/test_bar.py::test_bar *",
                "tests/foo/test_foo.py::test_foo *",
                "* 2 passed in *",
            ],
        )
        assert result.ret == 0

        result = testdir.runpytest("tests/foo", ".", "--collect-only", "-p", "no:sugar")
        result.stdout.fnmatch_lines(
            [
                "collected 2 items",
                "<Package tests>",
                "  <Package foo>",
                "    <Module test_foo.py>",
                "      <Function test_foo>",
                "  <Package bar>",
                "    <Module test_bar.py>",
                "      <Function test_bar>",
            ],
        )
        assert result.ret == 0
    finally:
        # fix up sys.modules to include our "tests" module again (not the one
        #   from the temp dir)
        if sys_modules_tests_old:  # pragma: no branch
            sys.modules["tests"] = sys_modules_tests_old


def test___toplevel_coverage(testdir: PytestFixture) -> None:
    """
    test___toplevel_coverage is only to allow coverage.py to see the top level and
       outermost scope of our code

    Args:
        testdir (PytestFixture):
    """

    # this test solely exists to allow coverage.py to see the top level and
    #   outermost scope of our code
    # this is necessary b/c our code gets imported before coverage.py hooks in
    # we simply "hide" our module from python, import it, and then put it back
    # we put it back, just in case something had modified it in memory before
    #   this test runs

    testdir = testdir  # ignore unused arg in sig

    # keep a reference to it
    old_module = sys.modules["pytest_prefer_nested_dup_tests"]
    # hide it from python
    del sys.modules["pytest_prefer_nested_dup_tests"]
    # import it as if new
    import pytest_prefer_nested_dup_tests  # noqa: 401
    # put it back
    sys.modules["pytest_prefer_nested_dup_tests"] = old_module

    # same as above, but for the __impl file
    old_module = sys.modules["pytest_prefer_nested_dup_tests.__impl"]
    del sys.modules["pytest_prefer_nested_dup_tests.__impl"]
    import pytest_prefer_nested_dup_tests.__impl  # noqa: 401
    sys.modules["pytest_prefer_nested_dup_tests.__impl"] = old_module

#endregion Tests
################################################################################
