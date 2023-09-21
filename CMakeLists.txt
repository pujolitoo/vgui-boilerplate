cmake_minimum_required(VERSION 3.15)
project(vgui_example)

if(WIN32)
	set(PY_EXE "python")
else()
	set(PY_EXE "python3")
endif()

if (CMAKE_GENERATOR MATCHES "Visual Studio")
	if(CMAKE_SIZEOF_VOID_P EQUAL 8)
		error(FATAL_ERROR "This type of application can not be compiled to 64 bits target")
	endif()
else()
	error(FATAL_ERROR "Generator unsupported, only Visual Studio")
endif()

set(CMAKE_CXX_FLAGS_DEBUG "/MTd")
set(CMAKE_CXX_FLAGS_RELEASE "/MT")

set(SOURCES_DIR src/)
set(SOURCE_SDK sdks/source-sdk-2013/sp/src)
set(SOURCE_SDK_LIB sdks/source-sdk-2013/sp/src/lib/public)
set(VGUI_ADICIONAL_SOURCES ${SOURCE_SDK}/public/vgui_controls/vgui_controls.cpp ${SOURCE_SDK}/public/tier0/memoverride.cpp)

link_directories(${SOURCE_SDK_LIB})

include_directories(${SOURCE_SDK}/public)
include_directories(${SOURCE_SDK}/public/tier1)
include_directories(${SOURCE_SDK}/public/tier0)
include_directories(${SOURCE_SDK}/public/vgui_controls)

file(GLOB_RECURSE SOURCE "${SOURCES_DIR}/*.cpp" "${SOURCES_DIR}/*.h")

if(CMAKE_BUILD_TYPE STREQUAL "Release")
	add_executable(${PROJECT_NAME} WIN32 ${SOURCE} ${VGUI_ADICIONAL_SOURCES})
else()
	add_executable(${PROJECT_NAME} ${SOURCE} ${VGUI_ADICIONAL_SOURCES})
endif()

target_compile_definitions(${PROJECT_NAME} PRIVATE $<$<CONFIG:Release>:NDEBUG> $<$<CONFIG:Debug>:NDEBUG=0>)

target_link_libraries(${PROJECT_NAME} PRIVATE appframework.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE steam_api.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE tier0.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE tier1.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE tier2.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE tier3.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE vgui_controls.lib)
target_link_libraries(${PROJECT_NAME} PRIVATE vstdlib.lib)

set_property(TARGET ${PROJECT_NAME} PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded")

message(STATUS ${CMAKE_BUILD_TYPE})

add_custom_command(
	TARGET ${PROJECT_NAME}
	POST_BUILD
	COMMAND ${PY_EXE} ../scripts/bin_copy.py ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR} ${CMAKE_BUILD_TYPE}
	COMMENT "MoveFiles"
)