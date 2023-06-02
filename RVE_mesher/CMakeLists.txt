message(STATUS "Cloning into 'gmsh'...")

include(FetchContent)

FetchContent_Declare(
  gmsh
  GIT_REPOSITORY "https://gitlab.onelab.info/gmsh/gmsh.git"
  GIT_TAG "master"
)

FetchContent_GetProperties(gmsh)
FetchContent_MakeAvailable(gmsh)

if(NOT gmsh_POPULATED)
  message(STATUS "Populating 'gmsh'...")
  FetchContent_Populate(gmsh)
  add_subdirectory(${gmsh_SOURCE_DIR} ${gmsh_BINARY_DIR})
endif()

#if(ENABLE_GMSH)
#
#  set(GMSH_PATH "${CMAKE_CURRENT_BINARY_DIR}/gmsh" CACHE INTERNAL "Path of Gmsh")
#
#  message("${CMAKE_CURRENT_BINARY_DIR}/gmsh" )
# 
#  include(ExternalProject)
#
#  ExternalProject_Add(gmsh
#    PREFIX ${GMSH_PATH}
#    DOWNLOAD_DIR "${CMAKE_CURRENT_SOURCE_DIR}/RVE_mesher"
#    GIT_REPOSITORY "https://gitlab.onelab.info/gmsh/gmsh.git"
#    GIT_TAG "master"
#    CONFIGURE_COMMAND
#      ${CMAKE_COMMAND}
#      ${GMSH_PATH}/src/gmsh
#    INSTALL_COMMAND ""
#    )
#   
#endif()
