include(FetchContent)

if(NOT DEFINED ANTLR4_TAG)
  # Set to branch name to keep library updated at the cost of needing to rebuild after 'clean'
  # Set to commit hash to keep the build stable and does not need to rebuild after 'clean'
  set(ANTLR4_TAG dev)
endif()

if(ANTLR4_ZIP_REPOSITORY)
  set(fetch_content_args
      URL ${ANTLR4_ZIP_REPOSITORY}
  )
else()
  set(fetch_content_args
      GIT_REPOSITORY https://github.com/antlr/antlr4.git
      GIT_TAG ${ANTLR4_TAG}
  )
endif()
# Only try system package if explicitly requested by distro packagers
# Note: ANTLR4 runtime must match the version used to generate parser files
# Default is to build from source to ensure version compatibility
if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.24 AND DEFINED ENV{FORCE_SYSTEM_ANTLR4})
  list(APPEND fetch_content_args FIND_PACKAGE_ARGS CONFIG)
endif()
FetchContent_Declare(antlr4-runtime
    SOURCE_SUBDIR runtime/Cpp
    EXCLUDE_FROM_ALL
    ${fetch_content_args}
)

option(ANTLR_BUILD_CPP_TESTS "Override: afdko" OFF)
option(ANTLR_BUILD_SHARED "Override: afdko" OFF)
option(ANTLR_BUILD_STATIC "Override: afdko" ON)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(WITH_STATIC_CRT OFF CACHE BOOL "Use dynamic CRT on Windows" FORCE)

# Handle FORCE_SYSTEM_ANTLR4 for CMake < 3.24
if(CMAKE_VERSION VERSION_LESS 3.24 AND DEFINED ENV{FORCE_SYSTEM_ANTLR4})
  find_package(antlr4-runtime REQUIRED CONFIG)
else()
  # For CMake 3.24+, FIND_PACKAGE_ARGS handles FORCE_SYSTEM_ANTLR4
  if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.24 AND DEFINED ENV{FORCE_SYSTEM_ANTLR4})
    set(CMAKE_REQUIRE_FIND_PACKAGE_antlr4-runtime ON)
  endif()
  FetchContent_MakeAvailable(antlr4-runtime)
endif()

# Create alias - antlr4_static exists whether from system or built
if(NOT TARGET afdko::antlr4)
  add_library(afdko::antlr4 ALIAS antlr4_static)
endif()
