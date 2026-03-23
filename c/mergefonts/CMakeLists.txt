add_library(mergefonts OBJECT
    mergeFonts.cpp
    mf_help.h
    mf_options.h
    mf_usage.h
)

target_link_libraries(mergefonts PRIVATE shared)
target_include_directories(mergefonts PRIVATE ../shared/resource ../shared/include/tx_help)
