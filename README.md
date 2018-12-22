# json_to_cmake
# Python tool to convert JSON data into cmake variables
usage: json_to_cmake.py [-h] [--output OUTPUT] [--name NAME] [--delim DELIM]
                        jsonfile
```
usage: json_to_cmake.py [-h] [--output OUTPUT] [--name NAME] [--delim DELIM]
                        jsonfile

Flatten a JSON file into single name value pairs for use with CMake.

positional arguments:
  jsonfile         Name of json file to flatten

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  Name of output file to write to
  --name NAME      Namespace to use for json variables (default: json)
  --delim DELIM    Delimiter to use for namespace separation (default: .)
```

# The Details

This follows the example [https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10] but we needed other variables to store the available indicies and subvalues.  The output is intended to be written to a file and used by a CMake include command.

# Example JSON file
Included in this repo is the following example json file.
```json
{
  "1darray" : [ 1,2,3,4,5 ],
  "2darray" : [ [11,12,13 ],
		[21,22,23 ],
                [31,32,33 ] ],
  "arrayofkeys" : [ { "key1" : "val1" },{ "key2" : "val2" } ] ,
  "keysofarray" : {  "keyarr1" : [1,2,3] , "keyarr2" : [4,5,6] },
  "keyof2darray" : { "keyarr2d" : [ [11,12],[21,22] ]}
}
```

To understand the methodology for how this could be represented in CMake, this is just best explained with the output below:

```bash
set( json.keyof2darray keyarr2d )
set( json.2darray.1 0 1 2 )
set( json.2darray.0 0 1 2 )
set( json.2darray.2 0 1 2 )
set( json.2darray.0.1 12 )
set( json.2darray.0.0 11 )
set( json.2darray.0.2 13 )
set( json.2darray.1.0 21 )
set( json.2darray.1.1 22 )
set( json.2darray.1.2 23 )
set( json.arrayofkeys.1.key2 val2 )
set( json.keysofarray.keyarr1.2 3 )
set( json.keysofarray keyarr1 keyarr2 )
set( json.keysofarray.keyarr1.0 1 )
set( json.keyof2darray.keyarr2d.0.1 12 )
set( json.keyof2darray.keyarr2d.0.0 11 )
set( json.1darray 0 1 2 3 4 )
set( json.keyof2darray.keyarr2d.1 0 1 )
set( json.keyof2darray.keyarr2d.0 0 1 )
set( json keysofarray 2darray keyof2darray 1darray arrayofkeys )
set( json.arrayofkeys.0 key1 )
set( json.keysofarray.keyarr1.1 2 )
set( json.arrayofkeys 0 1 )
set( json.keyof2darray.keyarr2d.1.0 21 )
set( json.2darray 0 1 2 )
set( json.2darray.2.2 33 )
set( json.2darray.2.1 32 )
set( json.2darray.2.0 31 )
set( json.arrayofkeys.1 key2 )
set( json.1darray.2 3 )
set( json.1darray.3 4 )
set( json.1darray.0 1 )
set( json.1darray.1 2 )
set( json.1darray.4 5 )
set( json.keysofarray.keyarr2 0 1 2 )
set( json.keysofarray.keyarr1 0 1 2 )
set( json.keysofarray.keyarr2.0 4 )
set( json.keysofarray.keyarr2.1 5 )
set( json.keysofarray.keyarr2.2 6 )
set( json.arrayofkeys.0.key1 val1 )
set( json.keyof2darray.keyarr2d.1.1 22 )
set( json.keyof2darray.keyarr2d 0 1 )
```

# CMake usage example

The example script CMakeExample.cmake shows the usage of the json_to_cmake.py tool.

CMakeExample.cmake
```CMake
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
```
executing the following command:
```bash
cmake -P CMakeExample.cmake
```
Gives the following output
```
-- json=keysofarray;2darray;keyof2darray;1darray;arrayofkeys
-- json.1darray=0;1;2;3;4
-- json.1darray.0=1
-- json.1darray.1=2
-- json.1darray.2=3
-- json.1darray.3=4
-- json.1darray.4=5
-- json.2darray=0;1;2
-- json.2darray.0=0;1;2
-- json.2darray.0.0=11
-- json.2darray.0.1=12
-- json.2darray.0.2=13
-- json.2darray.1=0;1;2
-- json.2darray.1.0=21
-- json.2darray.1.1=22
-- json.2darray.1.2=23
-- json.2darray.2=0;1;2
-- json.2darray.2.0=31
-- json.2darray.2.1=32
-- json.2darray.2.2=33
-- json.arrayofkeys=0;1
-- json.arrayofkeys.0=key1
-- json.arrayofkeys.0.key1=val1
-- json.arrayofkeys.1=key2
-- json.arrayofkeys.1.key2=val2
-- json.keyof2darray=keyarr2d
-- json.keyof2darray.keyarr2d=0;1
-- json.keyof2darray.keyarr2d.0=0;1
-- json.keyof2darray.keyarr2d.0.0=11
-- json.keyof2darray.keyarr2d.0.1=12
-- json.keyof2darray.keyarr2d.1=0;1
-- json.keyof2darray.keyarr2d.1.0=21
-- json.keyof2darray.keyarr2d.1.1=22
-- json.keysofarray=keyarr1;keyarr2
-- json.keysofarray.keyarr1=0;1;2
-- json.keysofarray.keyarr1.0=1
-- json.keysofarray.keyarr1.1=2
-- json.keysofarray.keyarr1.2=3
-- json.keysofarray.keyarr2=0;1;2
-- json.keysofarray.keyarr2.0=4
-- json.keysofarray.keyarr2.1=5
-- json.keysofarray.keyarr2.2=6
```
