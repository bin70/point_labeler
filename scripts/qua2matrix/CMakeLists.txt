cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(qua2matrix)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

find_package(PCL 1.8 REQUIRED COMPONENT common io visualization filters)
include_directories(${PCL_INCLUDE_DIRS} .)
add_definitions(${PCL_DEFINITIONS})

add_executable(qua2matrix qua2matrix.cpp)
target_link_libraries(qua2matrix ${PCL_LIBRARIES})
