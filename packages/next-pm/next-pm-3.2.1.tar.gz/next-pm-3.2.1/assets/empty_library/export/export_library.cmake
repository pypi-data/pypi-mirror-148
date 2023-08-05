# export/export_library.cmake

#########################
#       Lib Moon        #
#########################
if(${WIN32})

    set(__LIB_NAME___INCLUDE_DIR 
    ${__LIB_NAME___DIR}
    ${__LIB_NAME___DIR}/template 
    ${__LIB_NAME___DIR}/include )

    set(__LIB_NAME__ ${__LIB_NAME___DIR}/build/lib__LIB_BINARY__)

elseif(${UNIX})

    set(__LIB_NAME___INCLUDE_DIR 
        ${__LIB_NAME___DIR}
        ${__LIB_NAME___DIR}/template 
        ${__LIB_NAME___DIR}/include )
        
    set(__LIB_NAME__ ${__LIB_NAME___DIR}/build/lib__LIB_BINARY__)

endif()