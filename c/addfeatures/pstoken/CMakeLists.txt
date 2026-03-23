add_library(pstoken STATIC pstoken.c)

set_property(TARGET pstoken APPEND PROPERTY
             COMPILE_DEFINITIONS PSTOKEN_DEBUG=1 CFF_DEBUG=1 CFF_T13_SUPPORT=0)

target_link_libraries(pstoken PRIVATE shared)
target_include_directories(pstoken AFTER PRIVATE ../include ../../shared/resource)
