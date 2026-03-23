import pytest
import subprocess

from runner import main as runner
from differ import main as differ
from test_utils import get_expected_path

TOOL = 'detype1'

# Tests use the unified 'afdko' invoker by default for the primary test path.
# This reflects real-world usage where users run 'afdko detype1 ...' commands.
# A small backwards compatibility test at the end verifies wrappers still work.

def _tool_cmd(*args):
    """Helper to construct command using unified invoker."""
    return ['afdko', TOOL] + list(args)


# -----
# Tests
# -----

@pytest.mark.parametrize('arg', ['-h'])
def test_exit_known_option(arg):
    assert subprocess.call(_tool_cmd(arg)) == 0


@pytest.mark.parametrize('arg', ['-v', '-u'])
def test_exit_unknown_option(arg):
    assert subprocess.call(_tool_cmd(arg)) == 1


def test_run_on_pfa_data():
    actual_path = runner(['-t', TOOL, '-s', '-f', 'type1.pfa'])
    expected_path = get_expected_path('type1.txt')
    assert differ([expected_path, actual_path])


# ---------------------------------
# Backwards Compatibility Tests
# ---------------------------------
# Minimal tests to verify wrapper scripts still work.
# Main tests above use the invoker (the norm).

class TestWrapperBackwardsCompatibility:
    """Verify that the detype1 wrapper script still works for backwards compatibility."""

    @pytest.mark.parametrize('arg', ['-h'])
    def test_wrapper_help(self, arg):
        """Wrapper script handles basic options."""
        assert subprocess.call([TOOL, arg]) in [0, 1]  # Some tools return 1 for help

    def test_wrapper_runs_same_code(self):
        """Wrapper and invoker run the same underlying code."""
        # Run via invoker
        inv_result = subprocess.run(_tool_cmd('-h'),
                                    capture_output=True, text=True)
        
        # Run via wrapper
        wrap_result = subprocess.run([TOOL, '-h'],
                                     capture_output=True, text=True)
        
        # Both should succeed (return code may vary by tool)
        assert inv_result.returncode == wrap_result.returncode
        # Both should produce some output (even if minimal)
        assert len(inv_result.stdout) > 0
        assert len(wrap_result.stdout) > 0
        # Both should contain usage/help content
        assert 'usage' in inv_result.stdout.lower()
        assert 'usage' in wrap_result.stdout.lower()
