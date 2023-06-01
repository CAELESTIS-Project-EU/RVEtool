# Set minimum CMake version
cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

# Set project name, version and languages
project(RVEtool VERSION 1.0)

# Find packages


# Set verbosity
set(CMAKE_VERBOSE_MAKEFILE OFF)

# Define options
option(ENABLE_GMSH "Enable the use of Gmsh" ON)

# Git modules
set(ENABLE_GMSH "ON" CACHE STRING "Enable the use of Gmsh")

# Set CMake modules pathe
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Include Git submodules
if(ENABLE_GMSH)
    include(gmsh)
    add_subdirectory(RVE_mesher)
endif()
