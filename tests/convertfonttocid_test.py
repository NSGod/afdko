import os
import pytest
from shutil import copy2, rmtree
import tempfile

from afdko.convertfonttocid import mergeFontToCFF

from differ import main as differ
from test_utils import (get_input_path, get_expected_path, get_temp_file_path,
                        generate_ttx_dump)

MODULE = 'convertfonttocid'

DATA_DIR = os.path.join(os.path.dirname(__file__), MODULE + '_data')
TEMP_DIR = None  # Initialized in setup_module()


def setup_module():
    """
    Create the temporary output directory in system temp
    """
    global TEMP_DIR
    TEMP_DIR = tempfile.mkdtemp(prefix='afdko_convertfonttocid_test_')


def teardown_module():
    """
    teardown the temporary output directory
    """
    if TEMP_DIR and os.path.exists(TEMP_DIR):
        rmtree(TEMP_DIR)


# -----
# Tests
# -----

@pytest.mark.parametrize('subroutinize', [True, False])
@pytest.mark.parametrize('font_filename', ['1_fdict.ps', '3_fdict.ps'])
def test_mergeFontToCFF_bug570(font_filename, subroutinize):
    # Use TEMP_DIR to keep test files isolated
    actual_path = get_temp_file_path(directory=TEMP_DIR)
    subr_str = 'subr' if subroutinize else 'no_subr'
    font_base = os.path.splitext(font_filename)[0]
    ttx_filename = f'{font_base}-{subr_str}.ttx'
    source_path = get_input_path(font_filename)
    output_path = get_input_path('core.otf')
    copy2(output_path, actual_path)

    mergeFontToCFF(source_path, actual_path, subroutinize)

    actual_ttx = generate_ttx_dump(actual_path, ['CFF '])
    expected_ttx = get_expected_path(ttx_filename)
    assert differ([expected_ttx, actual_ttx, '-l', '2'])
