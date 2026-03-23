add_library(sfntedit OBJECT
    sfntedit.cpp
)

target_link_libraries(sfntedit PRIVATE shared)
target_include_directories(sfntedit PRIVATE ../spot/sfnt_includes)
