# AFDKO Command Wrapper Deprecation

## What's Changing

Starting in AFDKO 5.0, all tools should be invoked through the unified `afdko <command>` interface:

```bash
afdko makeotf -r
afdko tx -dump font.otf
afdko spot myFont.otf
```

Individual command wrappers (e.g., `makeotf`, `tx`, `spot`) are deprecated and will be removed in future releases.

## Removal Timeline

Commands are divided into two groups based on usage:

### Early Removal (6 months after 5.0 release)
Less commonly used commands:
- **C++ tools**: addfeatures, detype1, sfntdiff, type1
- **Build tools**: comparefamily, otc2otf, otf2otc, ttfcomponentizer, ttfdecomponentizer
- **Proofing tools**: charplot, digiplot, fontplot, fontplot2, fontsetplot, hintplot

### Standard Removal (12 months after 5.0 release)
Commonly used, high-impact commands:
- **Core tools**: spot, tx, sfntedit, mergefonts, rotatefont
- **Build tools**: makeotf, buildcff2vf, buildmasterotfs, makeinstancesufo, checkoutlinesufo, otf2ttf, ttxn
- **Hinting tools**: otfautohint, otfstemhist, waterfallplot

## Controlling Warnings

By default, deprecated wrappers work silently. Control behavior with:

**`AFDKO_WRAPPER_MODE`** environment variable:
- `off` (default) - No warnings
- `warn` - Show deprecation warnings
- `error` - Treat deprecated wrappers as errors

**Examples:**

```bash
# Default behavior - no warnings
spot myFont.otf

# See deprecation warnings
export AFDKO_WRAPPER_MODE=warn
spot myFont.otf
# Shows: DeprecationWarning: The 'spot' command wrapper is deprecated...

# Test strict migration
export AFDKO_WRAPPER_MODE=error
spot myFont.otf
# Exits with error

# Suppress warnings (useful for CI)
export AFDKO_WRAPPER_MODE=off
# Or use Python standard:
export PYTHONWARNINGS=ignore
```

## Migration Guide

**Recommended approach**: Start using `afdko <command>` syntax now.

**For scripts and automation**:
1. Update to `afdko <command>` syntax (future-proof)
2. Or temporarily set `AFDKO_WRAPPER_MODE=off` to silence warnings

**Testing your migration**:
```bash
export AFDKO_WRAPPER_MODE=error
# Run your build scripts - any deprecated wrapper will cause an error
```

## Rollout Phases

The deprecation will roll out in phases:

1. **Phase 1 (Initial release)**: Warnings opt-in (default: `off`)
   - Existing workflows continue unchanged
   - Early adopters can enable warnings

2. **Phase 2 (Near removal dates)**: Warnings default (default: `warn`)
   - Users made aware of upcoming removal
   - Can suppress with `AFDKO_WRAPPER_MODE=off`

3. **Phase 3 (At removal dates)**: Wrappers removed from package
   - Only `afdko <command>` interface remains

---

## Implementation Summary (for developers)

The system is implemented in `python/afdko/_deprecated.py` and `pyproject.toml`:

- **Entry points**: All 30 command entry points in `pyproject.toml` point to wrapper functions in `_deprecated.py`
- **Wrapper pattern**: Each wrapper checks `AFDKO_WRAPPER_MODE`, emits warnings if needed, then delegates to actual implementation
- **Mode detection**: `_get_wrapper_mode()` function reads environment variable with fallback to `DEFAULT_WRAPPER_MODE`
- **Alternative spellings**: Accepts variations like `disabled`/`0` for `off`, `1` for `warn`, `strict` for `error`
- **Python override**: Respects standard `PYTHONWARNINGS=ignore`
- **Two message types**: `_format_early_warning()` and `_format_standard_warning()` with different removal timelines
- **Command classification**: `EARLY_COMMANDS` set defines which commands get shorter timeline
- **Error mode**: `_check_error_mode()` exits with error code 1 if mode is `error`
- **Phase transitions**: Change `DEFAULT_WRAPPER_MODE` constant to advance through rollout phases
- **Special case**: `makeotfexe_wrapper()` always shows informational message regardless of mode

Main advantage: Single constant change (`DEFAULT_WRAPPER_MODE`) advances entire deprecation timeline through phases.
