execute_process(COMMAND ./json_to_cmake.py test_file.json --output example.cmake
		OUTPUT_VARIABLE output
                RESULT_VARIABLE result ) 

unset(output)

if( result ) 
  message(FATAL_ERROR "cmake_to_json.py failed! ${result}" ) 
endif()

include(example.cmake)

get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
    if( _variableName MATCHES "^json" ) 
       message(STATUS "${_variableName}=${${_variableName}}")
    endif()
endforeach()
