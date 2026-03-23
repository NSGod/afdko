"""
Deprecation wrappers for standalone command scripts.

These wrappers emit warnings before delegating to the actual
implementation. Commands are classified as "early" or "standard"
deprecation based on usage patterns.

Environment Variable:
    AFDKO_WRAPPER_MODE: Controls deprecation behavior
        - 'off' or unset: No warnings (current default)
        - 'warn': Show deprecation warnings (future default)
        - 'error': Treat deprecated wrappers as errors

    PYTHONWARNINGS=ignore: Also suppresses warnings (Python standard)

Timeline:
    Phase 1 (Current): Default='off', users opt-in with
                       AFDKO_WRAPPER_MODE=warn
    Phase 2 (Future):  Default='warn', users can silence with
                       AFDKO_WRAPPER_MODE=off
    Phase 3 (Near removal): Optionally default='error' for final
                            migration push
"""

import os
import sys
import warnings
from typing import Callable, NoReturn


# ============================================================================
# Configuration - Update these dates when releasing
# ============================================================================

# Current AFDKO version being released
CURRENT_VERSION = "4.1.0"
RELEASE_DATE = "2026-03-15"

# Date-based deprecation targets (hybrid approach)
# Early commands: 6 months after release
EARLY_REMOVAL_DATE = "2026-09-15"
EARLY_REMOVAL_TEXT = "an upcoming release after September 2026"

# Standard commands: 12 months after release, next major version
STANDARD_REMOVAL_DATE = "2027-03-15"
STANDARD_REMOVAL_VERSION = "5.0"
STANDARD_REMOVAL_TEXT = "the next major version after March 2027"

# Default wrapper mode (change this for different phases of rollout)
# Phase 1: 'off' - Users must opt-in to see warnings
# Phase 2: 'warn' - Show warnings by default (near removal dates)
# Phase 3: 'error' - Treat as errors for final migration (optional)
DEFAULT_WRAPPER_MODE = 'off'


# ============================================================================
# Command Classification
# ============================================================================

# Commands marked for early deprecation (6 months)
# Based on: /Users/skefiterum/src/docrepo/slides/afdko_command_planning.md
EARLY_COMMANDS = {
    # C++ commands
    'addfeatures',
    'detype1',
    'sfntdiff',
    'type1',
    # Python build commands
    'comparefamily',
    'otc2otf',
    'otf2otc',
    'ttfcomponentizer',
    'ttfdecomponentizer',
    # Python proofing commands
    'charplot',
    'digiplot',
    'fontplot',
    'fontplot2',
    'fontsetplot',
    'hintplot',
}

# All other commands use standard deprecation (12 months, next major version)
# These are the commonly used, high-impact commands


# ============================================================================
# Environment Variable Checks
# ============================================================================

def _get_wrapper_mode() -> str:
    """
    Get the current wrapper deprecation mode.

    Returns:
        'off', 'warn', or 'error'
    """
    # Python standard: PYTHONWARNINGS=ignore forces 'off'
    if os.environ.get('PYTHONWARNINGS') == 'ignore':
        return 'off'

    # Get AFDKO_WRAPPER_MODE, normalize to lowercase
    mode = os.environ.get('AFDKO_WRAPPER_MODE', '').lower().strip()

    # Handle common variations
    if mode in ('off', 'silent', 'disabled', 'no', 'false', '0'):
        return 'off'
    elif mode in ('warn', 'warning', 'warnings', 'yes', 'true', '1'):
        return 'warn'
    elif mode in ('error', 'strict', 'fail', '2'):
        return 'error'
    elif mode == '':
        # No environment variable set, use default
        return DEFAULT_WRAPPER_MODE
    else:
        # Invalid value, warn and use default
        print(
            f"Warning: Invalid AFDKO_WRAPPER_MODE='{mode}'. "
            f"Valid values: off, warn, error. "
            f"Using default: '{DEFAULT_WRAPPER_MODE}'",
            file=sys.stderr
        )
        return DEFAULT_WRAPPER_MODE


# ============================================================================
# Warning Messages
# ============================================================================

def _format_early_warning(command_name: str) -> str:
    """Format deprecation warning for early-removal commands."""
    return (
        f"DeprecationWarning: The '{command_name}' command wrapper is "
        f"deprecated and will be removed in {EARLY_REMOVAL_TEXT}.\n"
        f'The command should now be run as "afdko {command_name} '
        f'[options]".\n\n'
        f"To suppress this warning, set AFDKO_WRAPPER_MODE=off or "
        f"PYTHONWARNINGS=ignore.\n"
    )


def _format_standard_warning(command_name: str) -> str:
    """Format deprecation warning for standard-removal commands."""
    return (
        f"DeprecationWarning: The '{command_name}' command wrapper is "
        f"deprecated and will be removed in {STANDARD_REMOVAL_TEXT}.\n"
        f'The command should now be run as "afdko {command_name} '
        f'[options]".\n\n'
        f"To suppress this warning, set AFDKO_WRAPPER_MODE=off or "
        f"PYTHONWARNINGS=ignore.\n"
    )


def _emit_deprecation_warning(command_name: str) -> None:
    """
    Emit deprecation warning for a command wrapper.

    Args:
        command_name: Name of the deprecated command
    """
    # Check current mode
    mode = _get_wrapper_mode()

    # If mode is 'off', don't emit warnings
    if mode == 'off':
        return

    # Mode is 'warn' - emit the warning
    # (mode 'error' is handled separately in deprecated_command)

    # Determine if this is an early or standard deprecation
    is_early = command_name in EARLY_COMMANDS

    # Format the appropriate message
    if is_early:
        message = _format_early_warning(command_name)
    else:
        message = _format_standard_warning(command_name)

    # Print to stderr (always visible unless redirected)
    print(message, file=sys.stderr)

    # Also emit FutureWarning for Python contexts
    # (Use short message for Python warnings)
    removal = EARLY_REMOVAL_TEXT if is_early else STANDARD_REMOVAL_TEXT
    short_msg = (
        f"'{command_name}' wrapper is deprecated; "
        f"use 'afdko {command_name}' instead. "
        f"Removal: {removal}"
    )
    warnings.warn(short_msg, FutureWarning, stacklevel=3)


def _check_error_mode(command_name: str) -> None:
    """
    Check if wrapper should error instead of warning.

    Raises:
        SystemExit: If AFDKO_WRAPPER_MODE=error
    """
    mode = _get_wrapper_mode()

    if mode == 'error':
        is_early = command_name in EARLY_COMMANDS
        removal_text = (EARLY_REMOVAL_TEXT if is_early
                        else STANDARD_REMOVAL_TEXT)

        print(
            f"Error: The '{command_name}' wrapper is deprecated and will "
            f"be removed in {removal_text}.\n"
            f'The command should now be run as "afdko {command_name} '
            f'[options]".\n\n'
            f"To temporarily allow deprecated wrappers, set "
            f"AFDKO_WRAPPER_MODE=off or AFDKO_WRAPPER_MODE=warn.\n",
            file=sys.stderr
        )
        sys.exit(1)


# ============================================================================
# Wrapper Functions
# ============================================================================

def deprecated_command(command_name: str, target_func: Callable) -> Callable:
    """
    Create a deprecation wrapper for a command.

    Args:
        command_name: Name of the command (e.g., 'tx', 'makeotf')
        target_func: Actual implementation function

    Returns:
        Wrapped function that emits warnings before calling target
    """
    def wrapper(*args, **kwargs) -> NoReturn:
        # Check if we should error instead of warning
        _check_error_mode(command_name)

        # Emit deprecation warning
        _emit_deprecation_warning(command_name)

        # Call actual implementation
        return target_func(*args, **kwargs)

    wrapper.__name__ = target_func.__name__
    wrapper.__doc__ = (
        f"DEPRECATED: Use 'afdko {command_name}' instead.\n\n"
        f"{target_func.__doc__ or ''}"
    )
    return wrapper


# ============================================================================
# Individual Command Wrappers
# ============================================================================
# These are the entry points referenced in pyproject.toml

# C++ Commands
def tx_wrapper() -> NoReturn:
    """Deprecated wrapper for tx command."""
    from afdko._internal import tx
    return deprecated_command('tx', tx)()


def sfntedit_wrapper() -> NoReturn:
    """Deprecated wrapper for sfntedit command."""
    from afdko._internal import sfntedit
    return deprecated_command('sfntedit', sfntedit)()


def spot_wrapper() -> NoReturn:
    """Deprecated wrapper for spot command."""
    from afdko._internal import spot
    return deprecated_command('spot', spot)()


def addfeatures_wrapper() -> NoReturn:
    """Deprecated wrapper for addfeatures command (EARLY)."""
    from afdko._internal import addfeatures
    return deprecated_command('addfeatures', addfeatures)()


def detype1_wrapper() -> NoReturn:
    """Deprecated wrapper for detype1 command (EARLY)."""
    from afdko._internal import detype1
    return deprecated_command('detype1', detype1)()


def type1_wrapper() -> NoReturn:
    """Deprecated wrapper for type1 command (EARLY)."""
    from afdko._internal import type1
    return deprecated_command('type1', type1)()


def sfntdiff_wrapper() -> NoReturn:
    """Deprecated wrapper for sfntdiff command (EARLY)."""
    from afdko._internal import sfntdiff
    return deprecated_command('sfntdiff', sfntdiff)()


def mergefonts_wrapper() -> NoReturn:
    """Deprecated wrapper for mergefonts command."""
    from afdko._internal import mergefonts
    return deprecated_command('mergefonts', mergefonts)()


def rotatefont_wrapper() -> NoReturn:
    """Deprecated wrapper for rotatefont command."""
    from afdko._internal import rotatefont
    return deprecated_command('rotatefont', rotatefont)()


# Python Commands - Build & Processing
def makeotf_wrapper() -> NoReturn:
    """Deprecated wrapper for makeotf command."""
    from afdko.makeotf import main
    return deprecated_command('makeotf', main)()


def buildcff2vf_wrapper() -> NoReturn:
    """Deprecated wrapper for buildcff2vf command."""
    from afdko.buildcff2vf import main
    return deprecated_command('buildcff2vf', main)()


def buildmasterotfs_wrapper() -> NoReturn:
    """Deprecated wrapper for buildmasterotfs command."""
    from afdko.buildmasterotfs import main
    return deprecated_command('buildmasterotfs', main)()


def makeinstancesufo_wrapper() -> NoReturn:
    """Deprecated wrapper for makeinstancesufo command."""
    from afdko.makeinstancesufo import main
    return deprecated_command('makeinstancesufo', main)()


def checkoutlinesufo_wrapper() -> NoReturn:
    """Deprecated wrapper for checkoutlinesufo command."""
    from afdko.checkoutlinesufo import main
    return deprecated_command('checkoutlinesufo', main)()


def comparefamily_wrapper() -> NoReturn:
    """Deprecated wrapper for comparefamily command (EARLY)."""
    from afdko.comparefamily import main
    return deprecated_command('comparefamily', main)()


def otc2otf_wrapper() -> NoReturn:
    """Deprecated wrapper for otc2otf command (EARLY)."""
    from afdko.otc2otf import main
    return deprecated_command('otc2otf', main)()


def otf2otc_wrapper() -> NoReturn:
    """Deprecated wrapper for otf2otc command (EARLY)."""
    from afdko.otf2otc import main
    return deprecated_command('otf2otc', main)()


def otf2ttf_wrapper() -> NoReturn:
    """Deprecated wrapper for otf2ttf command."""
    from afdko.otf2ttf import main
    return deprecated_command('otf2ttf', main)()


def ttfcomponentizer_wrapper() -> NoReturn:
    """Deprecated wrapper for ttfcomponentizer command (EARLY)."""
    from afdko.ttfcomponentizer import main
    return deprecated_command('ttfcomponentizer', main)()


def ttfdecomponentizer_wrapper() -> NoReturn:
    """Deprecated wrapper for ttfdecomponentizer command (EARLY)."""
    from afdko.ttfdecomponentizer import main
    return deprecated_command('ttfdecomponentizer', main)()


def ttxn_wrapper() -> NoReturn:
    """Deprecated wrapper for ttxn command."""
    from afdko.ttxn import main
    return deprecated_command('ttxn', main)()


# Python Commands - Proofing (all EARLY)
def charplot_wrapper() -> NoReturn:
    """Deprecated wrapper for charplot command (EARLY)."""
    from afdko.proofpdf import charplot
    return deprecated_command('charplot', charplot)()


def digiplot_wrapper() -> NoReturn:
    """Deprecated wrapper for digiplot command (EARLY)."""
    from afdko.proofpdf import digiplot
    return deprecated_command('digiplot', digiplot)()


def fontplot_wrapper() -> NoReturn:
    """Deprecated wrapper for fontplot command (EARLY)."""
    from afdko.proofpdf import fontplot
    return deprecated_command('fontplot', fontplot)()


def fontplot2_wrapper() -> NoReturn:
    """Deprecated wrapper for fontplot2 command (EARLY)."""
    from afdko.proofpdf import fontplot2
    return deprecated_command('fontplot2', fontplot2)()


def fontsetplot_wrapper() -> NoReturn:
    """Deprecated wrapper for fontsetplot command (EARLY)."""
    from afdko.proofpdf import fontsetplot
    return deprecated_command('fontsetplot', fontsetplot)()


def hintplot_wrapper() -> NoReturn:
    """Deprecated wrapper for hintplot command (EARLY)."""
    from afdko.proofpdf import hintplot
    return deprecated_command('hintplot', hintplot)()


def waterfallplot_wrapper() -> NoReturn:
    """Deprecated wrapper for waterfallplot command."""
    from afdko.proofpdf import waterfallplot
    return deprecated_command('waterfallplot', waterfallplot)()


# Python Commands - Hinting
def otfautohint_wrapper() -> NoReturn:
    """Deprecated wrapper for otfautohint command."""
    from afdko.otfautohint.__main__ import main
    return deprecated_command('otfautohint', main)()


def otfstemhist_wrapper() -> NoReturn:
    """Deprecated wrapper for otfstemhist command."""
    from afdko.otfautohint.__main__ import stemhist
    return deprecated_command('otfstemhist', stemhist)()


# ============================================================================
# Special Transition Wrappers (Always Show Message)
# ============================================================================

def makeotfexe_wrapper() -> NoReturn:
    """Transition message for makeotfexe -> addfeatures."""
    import sys

    message = (
        "The 'makeotfexe' command has been replaced by 'addfeatures'.\n\n"
        "makeotfexe took a Type 1 font, converted it to a CFF table, and "
        "compiled features into OpenType tables. addfeatures takes a CFF "
        "table as input and compiles the features. The 'makeotf' wrapper "
        "handles this change automatically, so most users won't need to "
        "adjust their workflows.\n\n"
        "If you were calling makeotfexe directly, you may now need to "
        "build a CFF table first using 'afdko tx', which has been "
        "enhanced with some features that were previously exclusive to "
        "makeotfexe, including support for GlyphOrderAndAliasDB files.\n\n"
        "Examples:\n"
        "  Old: makeotfexe -f features.fea font.pfa\n"
        "  New: afdko tx -cff +b font.pfa temp.cff && "
        "afdko addfeatures -f features.fea temp.cff\n\n"
        "  Or use the makeotf command: afdko makeotf -f font.pfa "
        "-ff features.fea\n\n"
        "The makeotfexe wrapper will be removed in the next major "
        "version after March 2027.\n"
    )

    print(message, file=sys.stderr)
    sys.exit(1)
