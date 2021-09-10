
cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(gg)

include_directories(gengi/include)

file(GLOB SOURCES 
  gengi/src/*.cpp
  gengi/src/Scanner/*.cpp
  )

add_executable(${PROJECT_NAME} ${SOURCES})