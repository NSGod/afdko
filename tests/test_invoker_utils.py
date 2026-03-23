"""
Utilities for testing both invoker and wrapper paths.

This module provides helpers to test commands via:
1. Unified invoker: afdko <command> [args]
2. Individual wrappers: <command> [args]

This ensures both paths work correctly and maintain backwards compatibility.
"""

import subprocess
import os


def run_via_invoker(cmd, *args):
    """
    Run command via unified invoker: afdko <cmd> [args]

    Args:
        cmd: Command name (e.g., 'tx', 'makeotf')
        *args: Command arguments

    Returns:
        int: Return code from subprocess.call()
    """
    return subprocess.call(['afdko', cmd] + list(args))


def run_via_wrapper(cmd, *args):
    """
    Run command via individual wrapper: <cmd> [args]

    Args:
        cmd: Command name (e.g., 'tx', 'makeotf')
        *args: Command arguments

    Returns:
        int: Return code from subprocess.call()
    """
    return subprocess.call([cmd] + list(args))


def run_both_paths(cmd, *args, check='returncode'):
    """
    Run command via both paths and verify they behave the same.

    Args:
        cmd: Command name (e.g., 'tx', 'makeotf')
        *args: Command arguments
        check: What to verify ('returncode', 'stdout', 'both')

    Returns:
        tuple: (invoker_result, wrapper_result)
            - If check='returncode': (int, int) return codes
            - If check='stdout' or 'both': (CompletedProcess, CompletedProcess)

    Examples:
        >>> # Check return codes match
        >>> inv_rc, wrap_rc = run_both_paths('tx', '-h')
        >>> assert inv_rc == wrap_rc == 0

        >>> # Check output matches
        >>> inv_proc, wrap_proc = run_both_paths('tx', '-v', check='stdout')
        >>> assert inv_proc.stdout == wrap_proc.stdout
    """
    if check == 'returncode':
        inv_result = run_via_invoker(cmd, *args)
        wrap_result = run_via_wrapper(cmd, *args)
        return inv_result, wrap_result
    elif check in ('stdout', 'both'):
        inv_proc = subprocess.run(['afdko', cmd] + list(args),
                                  capture_output=True, text=True)
        wrap_proc = subprocess.run([cmd] + list(args),
                                   capture_output=True, text=True)
        return inv_proc, wrap_proc
    else:
        raise ValueError(f"Unknown check type: {check}")


def make_cmd(tool, use_invoker=None):
    """
    Helper to construct command for subprocess calls.

    Respects AFDKO_TEST_USE_INVOKER environment variable.

    Args:
        tool: Command name (e.g., 'tx', 'makeotf')
        use_invoker: Override environment variable (True/False/None)

    Returns:
        list: Command parts ready for subprocess

    Examples:
        >>> make_cmd('tx')  # With AFDKO_TEST_USE_INVOKER=1
        ['afdko', 'tx']

        >>> make_cmd('tx')  # With AFDKO_TEST_USE_INVOKER=0
        ['tx']

        >>> make_cmd('tx', use_invoker=True)  # Override
        ['afdko', 'tx']
    """
    if use_invoker is None:
        use_invoker = os.getenv('AFDKO_TEST_USE_INVOKER', 'True').lower() in ('true', '1', 't', 'yes')

    return ['afdko', tool] if use_invoker else [tool]


# Pytest fixture support for parametrizing tests across both paths
def pytest_generate_tests(metafunc):
    """
    Automatically parametrize tests that use 'run_cmd' fixture
    to test both invoker and wrapper paths.

    Usage in tests:
        def test_something(run_cmd):
            assert run_cmd('tx', '-h') == 0

    This will run the test twice:
    - Once with run_cmd=run_via_invoker
    - Once with run_cmd=run_via_wrapper
    """
    if 'run_cmd' in metafunc.fixturenames:
        metafunc.parametrize('run_cmd', [
            run_via_invoker,
            run_via_wrapper,
        ], ids=['invoker', 'wrapper'])
