add_library(hotconv STATIC
    # generated
    FeatCtx.cpp
    FeatCtx.h
    FeatLexer.cpp
    FeatLexer.h
    FeatParserBaseVisitor.cpp
    FeatParserBaseVisitor.h
    FeatParser.cpp
    FeatParser.h
    FeatParserVisitor.cpp
    FeatParserVisitor.h
    # static
    anon.cpp
    anon.h
    BASE.cpp
    BASE.h
    cmap.cpp
    cmap.h
    common.h
    FeatCtx.cpp
    FeatCtx.h
    ${GENERATED_SOURCES}
    FeatVisitor.cpp
    FeatVisitor.h
    glyphmetrics.h
    glyphmetrics.cpp
    GDEF.cpp
    GDEF.h
    GPOS.cpp
    GPOS.h
    GSUB.cpp
    GSUB.h
    head.cpp
    head.h
    hmtx.cpp
    hmtx.h
    hot.cpp
    hotlogger.h
    hotlogger.cpp
    hotmap.h
    map.cpp
    maxp.cpp
    maxp.h
    name.cpp
    name.h
    MVAR.h
    MVAR.cpp
    OS_2.cpp
    OS_2.h
    otl.cpp
    otl.h
    post.cpp
    post.h
    schinese.h
    sfnt.cpp
    sfnt.h
    STAT.cpp
    STAT.h
    uniblock.h
    vmtx.cpp
    vmtx.h
    winansi.h
)

set_property(TARGET hotconv PROPERTY C_STANDARD 99)

# ANTLR4CPP_STATIC tells ANTLR4 headers we're using static library
target_compile_definitions(hotconv PRIVATE ANTLR4CPP_STATIC)

target_include_directories(hotconv BEFORE PRIVATE $<$<COMPILE_LANGUAGE:CXX>:${ANTLR4_INCLUDE_DIRS}>)
target_include_directories(hotconv AFTER PRIVATE ../include ../../shared/resource)
# Because hotconv is an object library, all this should do is
# establish the build dependency
target_link_libraries(hotconv PUBLIC afdko::antlr4 shared)

if ( CMAKE_COMPILER_IS_GNUCC )
        set_property(TARGET hotconv APPEND PROPERTY
                     COMPILE_OPTIONS -Wall -Wno-attributes)
endif()
