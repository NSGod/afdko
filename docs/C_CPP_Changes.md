# C/C++ Architectural Changes: develop → addfeatures

This is an AI summary of the changes to our C/C++ code, for reference.

## Summary Statistics

### Overall Code Metrics
- **Total source files**: 177 → 150 (-27 files, -15%)
- **C files (.c)**: 170 → 76 (-94 files, -55%)
- **C++ files (.cpp)**: 7 → 74 (+67 files, +957%)
- **Language ratio change**: 96% C / 4% C++ → 51% C / 49% C++

### By Component
- **makeotf → addfeatures**: 52 files → 32 files (-20 files, -38% reduction)
- **spot**: 61 files → 56 files (-5 files, -8% reduction)
- **shared library**: Flattened structure, major C→C++ conversions
- **NEW: c/afdko/**: Unified binary dispatcher (2 files)
- **NO LONGER SEPARATE: tx/**: Integrated into unified binary

## Major Architectural Changes

### 1. Unified Binary (c/afdko/)
**NEW component** providing single entry point for all C++ tools

**Files**:
- `afdko_main.cpp` - Fast dispatcher for C++ commands
- Embeds Python interpreter for Python commands and help

**Design**:
- Fast path: C++ commands dispatched directly without Python overhead
- Python fallback: Help, Python commands, unknown commands → invoke Python
- Links to 9 C++ tool entry points: tx, sfntedit, spot, addfeatures, detype1, type1, sfntdiff, mergefonts, rotatefont
- Abbreviation support built-in (e.g., `se` → sfntedit, `af` → addfeatures)

### 2. makeotf → addfeatures Transformation

**Major refactoring and renaming**:
- 52 source files → 32 source files (-38%)
- Extensive C → C++ conversion in hotconv/ subsystem
- Removed Type 1 → CFF conversion logic (now handled by tx)
- Added CFF2 variable font support
- Cleaner separation of concerns

**File structure changes**:
```
develop: c/makeotf/
  source/
    cbpriv.c, cb.c, mac.c, c_main.c, file.c, fcdb.c, main.cpp
  lib/
    typecomp/    (14 files)
    cffread/     (2 files)
    hotconv/     (26+ files - feature compilation)
    api/         (headers)

addfeatures: c/addfeatures/
  cb.cpp, fcdb.cpp, main.cpp    (C→C++ conversions)
  hotconv/     (30 files, many C→C++ conversions)
    - BASE.cpp, GDEF.cpp, GPOS.cpp, GSUB.cpp
    - MVAR.cpp, STAT.cpp (new variable font support)
    - OS_2.cpp, head.cpp, hmtx.cpp, vmtx.cpp
    - FeatParser.cpp, FeatLexer.cpp, FeatVisitor.cpp
    - cmap.cpp, name.cpp, post.cpp, maxp.cpp
    - hot.cpp, otl.cpp, sfnt.cpp
  pstoken/     (parser component)
  include/
  utils/
```

**Eliminated components** (moved to shared or removed):
- typecomp/ library (Type 1 compilation - now in tx/shared)
- cffread/ library (CFF reading - now in shared)
- File I/O abstractions consolidated

### 3. Shared Library Restructuring

**Structure flattening**:
```
develop: c/shared/source/
  tx_shared/tx_shared.c
  uforead/uforead.c
  ufowrite/ufowrite.c
  t1read/t1read.c
  t1cstr/t1cstr.c
  t2cstr/t2cstr.c
  svgwrite/svgwrite.c
  pdfwrite/pdfwrite.c
  ... (many subdirectories)

addfeatures: c/shared/
  tx_shared.cpp       (C→C++)
  uforead.cpp         (C→C++)
  ufowrite.cpp        (C→C++)
  t1read.cpp          (C→C++)
  t1cstr.cpp          (C→C++)
  t2cstr.cpp          (C→C++)
  svgwrite.cpp        (C→C++)
  pdfwrite.cpp        (C→C++)
  sfntread.cpp        (C→C++)
  sfntwrite.cpp       (C→C++)
  ttread.cpp          (C→C++)
  goadb.cpp           (NEW - GOADB support from makeotfexe)
  designspace.cpp     (NEW - designspace parsing)
  varsupport.cpp      (NEW - variable font support)
  ... (flat structure, many more .cpp files)
```

**Key changes**:
- Eliminated deeply nested directory structure
- Major C → C++ conversions throughout
- Consolidated font reading/writing code
- Added new support libraries (GOADB, designspace, variable fonts)

### 4. C → C++ Conversions

**Major files converted**:
- `tx_shared.c` → `tx_shared.cpp` (226KB, core tx functionality)
- `uforead.c` → `uforead.cpp` (120KB)
- `ufowrite.c` → `ufowrite.cpp` (47KB)
- `t1read.c` → `t1read.cpp` (107KB)
- `t1cstr.c` → `t1cstr.cpp` (52KB)
- `t2cstr.c` → `t2cstr.cpp` (72KB)
- `ttread.c` → `ttread.cpp` (112KB)
- `svgwrite.c` → `svgwrite.cpp` (21KB)
- `pdfwrite.c` → `pdfwrite.cpp` (50KB)
- `sfntread.c` → `sfntread.cpp` (10KB)
- `sfntwrite.c` → `sfntwrite.cpp` (16KB)
- `cffread_abs.c` → `cffread_abs.cpp` (112KB)
- Many hotconv/ files (GSUB.c → GSUB.cpp, GPOS.c → GPOS.cpp, etc.)

**Total converted**: ~94 .c files eliminated, ~67 new .cpp files created

### 5. Integration Points

**tx integration**:
- No longer separate c/tx/ directory
- Core tx code in shared library (tx_shared.cpp)
- Thin main() in c/afdko/afdko_main.cpp dispatcher
- Same functionality, better code reuse

**Version integration**:
- NEW: c/shared/version.h.in, version.cpp.in (CMake templates)
- FDK_VERSION now generated at build time
- Flows from setuptools_scm → CMake → all tools
- Constructor-based initialization for Cython compatibility

### 6. What Was Kept as C

**Still .c files** (76 total):
- Low-level font manipulation code (ctutil.c, da.c, dynarr.c, sha1.c, smem.c)
- Legacy Type 1 support files (t13fail.c, t13supp.c)
- Core CFF reading (cffread.c)
- Parser token handling (pstoken.c in addfeatures/)
- Some spot/ proof generation code
- Platform-specific code in some cases

## Benefits of These Changes

1. **Code Reduction**: 15% fewer source files overall
2. **Modern C++**: Better type safety, RAII, standard library usage
3. **Unified Architecture**: Single binary entry point, better code sharing
4. **Flatter Structure**: Easier navigation, reduced directory nesting
5. **Better Separation**: Clear boundaries between font I/O, feature compilation, proof generation
6. **Variable Font Support**: New capabilities enabled by cleaner architecture
7. **Build Integration**: Proper version flow, better CMake integration
8. **Performance**: Fast dispatch for C++ commands, Python fallback for flexibility

## Migration Impact

**For users**: Transparent - same functionality, different implementation
**For developers**:
- Much cleaner codebase to work with
- Modern C++ patterns throughout
- Better organized shared library
- Single unified entry point simplifies debugging
- Flatter structure easier to navigate

## Technical Debt Addressed

1. **Eliminated** deeply nested directory structures
2. **Consolidated** redundant font reading/writing code
3. **Removed** obsolete Type 1 → CFF conversion from addfeatures
4. **Unified** command dispatch architecture
5. **Modernized** C → C++ for better maintainability
6. **Integrated** version string generation properly

## Future Path

This architectural foundation supports:
- Further C → C++ conversions as needed
- Additional variable font features
- Better testing and code coverage
- Potential for shared library distribution
- Cleaner plugin/extension architecture
