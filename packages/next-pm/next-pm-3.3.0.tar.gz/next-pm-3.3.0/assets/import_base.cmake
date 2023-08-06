set(__NAME_PROJECT_UPPER_CASE___DIR __DIR_LIB__)

#########################
#       Lib Moon        #
#########################
if(${WIN32})

    set(__NAME_PROJECT_UPPER_CASE___INCLUDE_DIR 
    ${__NAME_PROJECT_UPPER_CASE___DIR}
    ${__NAME_PROJECT_UPPER_CASE___DIR}/..
    ${__NAME_PROJECT_UPPER_CASE___DIR}/template 
    ${__NAME_PROJECT_UPPER_CASE___DIR}/include )

    set(__NAME_PROJECT_UPPER_CASE__ __FILE_BUILD_ABS__)

elseif(${UNIX})

    set(__NAME_PROJECT_UPPER_CASE___INCLUDE_DIR 
        ${__NAME_PROJECT_UPPER_CASE___DIR}
        ${__NAME_PROJECT_UPPER_CASE___DIR}/..
        ${__NAME_PROJECT_UPPER_CASE___DIR}/template 
        ${__NAME_PROJECT_UPPER_CASE___DIR}/include )
        
    set(__NAME_PROJECT_UPPER_CASE__ __FILE_BUILD_ABS__)

endif()