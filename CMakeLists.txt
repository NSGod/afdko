cmake_minimum_required(VERSION 3.16)

project(afdko LANGUAGES C CXX)

# set(CMAKE_VERBOSE_MAKEFILE ON)

# RelWithDebInfo builds an optimized binary but includes debugging symbols
# Other common possibilities are "Debug" and "Release"
if (NOT CMAKE_BUILD_TYPE)
#    set(CMAKE_BUILD_TYPE "RelWithDebInfo" CACHE STRING "Build type configuration" FORCE)
    set(CMAKE_BUILD_TYPE "Debug" CACHE STRING "Build type configuration" FORCE)
endif()
message(STATUS "Build type is ${CMAKE_BUILD_TYPE}")

set(CMAKE_CXX_STANDARD 17)

# None of AFDKO's C sources are multithreaded, but we need to add
# -pthread on Linux to make ANTLR4 happy when statically linked
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_program(CYTHON "cython")

# add_compile_definitions(HOT_DEBUG)
# add_compile_definitions(STRIP_EXTERN_C)

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Antlr 4 configuration

# This is an alternate way of supplying the Antlr 4 sources that will override
# the git clone of the tag listed below. This is especially useful if you
# encounter compiler problems and need to make small edits to compensate. Start
# with the Antlr project's sources, e.g.
# https://www.antlr.org/download/antlr4-cpp-runtime-4.9.3-source.zip
# set(ANTLR4_ZIP_REPOSITORY "/path_to_antlr4_archive/a4.zip")

set(ANTLR4_WITH_STATIC_CRT OFF)
# set(ANTLR4_TAG tags/4.13.2)
# This is a more recent commit than 4.13.2 that addresses a missing
# include directive needed in more recent Visual Studio releases
set(ANTLR4_TAG df4d68c09cdef73e023b8838a8bc7ca4dff1d1de)
set(LIBXML2_TAG tags/v2.9.13)
add_subdirectory(third_party)

# ============================================================================
# Version Generation
# ============================================================================
# Get version from scikit-build-core (passed via SKBUILD_PROJECT_VERSION)
# or fallback to running Python to get it from setuptools_scm

if(DEFINED SKBUILD_PROJECT_VERSION)
    set(AFDKO_VERSION "${SKBUILD_PROJECT_VERSION}")
    message(STATUS "Version from scikit-build-core: ${AFDKO_VERSION}")
else()
    # Fallback: run Python to get version from setuptools_scm
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "from setuptools_scm import get_version; print(get_version(), end='')"
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        OUTPUT_VARIABLE AFDKO_VERSION
        RESULT_VARIABLE VERSION_RESULT
        ERROR_QUIET
    )
    if(VERSION_RESULT EQUAL 0)
        message(STATUS "Version from setuptools_scm: ${AFDKO_VERSION}")
    else()
        set(AFDKO_VERSION "unknown")
        message(WARNING "Could not determine version, using 'unknown'")
    endif()
endif()

# Generate version header and source files
configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/c/shared/afdko_version.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/c/shared/afdko_version.h
    @ONLY
)

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/c/shared/afdko_version.cpp.in
    ${CMAKE_CURRENT_BINARY_DIR}/c/shared/afdko_version.cpp
    @ONLY
)

# Create version library that all tools can link against
add_library(afdko_version STATIC ${CMAKE_CURRENT_BINARY_DIR}/c/shared/afdko_version.cpp)
target_include_directories(afdko_version PUBLIC ${CMAKE_CURRENT_BINARY_DIR}/c/shared)
set_target_properties(afdko_version PROPERTIES POSITION_INDEPENDENT_CODE ON)

# sanitizer support
# work around https://github.com/pypa/setuptools/issues/1928 with environment
# variable
if(DEFINED ENV{ADD_SANITIZER})
    set(ADD_SANITIZER "$ENV{ADD_SANITIZER}" CACHE STRING "Sanitizer type (\"none\" for no sanitizer")
else()
    set(ADD_SANITIZER "none" CACHE STRING "Sanitizer type (\"none\" for no sanitizer")
endif()
include(AddSanitizer)
add_sanitizer("${ADD_SANITIZER}")

# Ported from old build files, XXX not sure if all of these are needed
if(WIN32)
    add_compile_definitions(CTL_CDECL=__cdecl OS=os_windowsNT $<$<CONFIG:Release>:NDEBUG>)
endif()

include(CheckLibraryExists)
CHECK_LIBRARY_EXISTS(m floor "" HAVE_M_LIB)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

python_add_library(_internal MODULE "${CMAKE_CURRENT_BINARY_DIR}/_internal.c" WITH_SOABI)

if (HAVE_M_LIB)
    target_link_libraries(_internal PRIVATE m)
endif ()

target_link_libraries(_internal PRIVATE LibXml2::LibXml2)

add_custom_command(
    OUTPUT _internal.c
    DEPENDS cython/_internal.pyx
    VERBATIM
    COMMAND "${CYTHON}" "${CMAKE_CURRENT_SOURCE_DIR}/cython/_internal.pyx" --output-file
            "${CMAKE_CURRENT_BINARY_DIR}/_internal.c")

add_subdirectory(c/shared)
add_subdirectory(c/detype1)
add_subdirectory(c/mergefonts)
add_subdirectory(c/rotatefont)
add_subdirectory(c/sfntdiff)
add_subdirectory(c/sfntedit)
add_subdirectory(c/spot)
add_subdirectory(c/type1)
add_subdirectory(c/addfeatures)

target_link_libraries(_internal PRIVATE afdko_version detype1 type1 addfeatures spot sfntedit sfntdiff mergefonts rotatefont shared afdko::antlr4)

if(CMAKE_USE_PTHREADS_INIT)
    target_link_libraries(_internal PRIVATE Threads::Threads)
endif()

install(TARGETS _internal LIBRARY DESTINATION afdko)
