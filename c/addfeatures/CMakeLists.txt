add_subdirectory(hotconv)
add_subdirectory(pstoken)

add_library(addfeatures OBJECT
    cb.cpp
    main.cpp
    fcdb.cpp
    cb.h
    fcdb.h
)

target_link_libraries(addfeatures
    PUBLIC hotconv pstoken shared afdko_version)
target_include_directories(addfeatures PUBLIC AFTER include ../shared/resource)

set_property(TARGET addfeatures APPEND PROPERTY
             COMPILE_DEFINITIONS MAKEOTFLIB_EXPORTS=1)
