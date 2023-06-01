message(STATUS "Checking whether Gmsh Git submodule has cloned ...")

#if (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/gmsh/CMakeLists.txt")
#  message("Cloning into 'gmsh'...")
#  include(FetchContent)
#  FetchContent_Declare(
#    gmsh
#    GIT_REPOSITORY "https://gitlab.onelab.info/gmsh/gmsh.git"
#    GIT_TAG "origin/master"
#    CONFIGURE_COMMAND "-DENABLE_METIS=OFF -DENABLE_TESTS=OFF"
#  )
#  if(NOT gmsh_POPULATED)
#    FetchContent_Populate(gmsh)
#    add_subdirectory(${gmsh_SOURCE_DIR} ${gmsh_BINARY_DIR})
#  endif()
#else()
#  add_subdirectory(gmsh)
#endif()

if(ENABLE_GMSH)
  set(GMSH_PATH "${CMAKE_CURRENT_BINARY_DIR}/gmsh" CACHE INTERNAL "Path of Gmsh")
  include(ExternalProject)
  ExternalProject_Add(
    gmsh
    PREFIX ${GMSH_PATH}
    GIT_REPOSITORY "https://gitlab.onelab.info/gmsh/gmsh.git"
    GIT_TAG master
    CONFIGURE_COMMAND ${CMAKE_COMMAND} -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER} -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER} -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE} -DCMAKE_INSTALL_PREFIX:PATH=${GMSH_PATH} -DENABLE_METIS=OFF -DENABLE_BUILD_DYNAMIC=1 -DENABLE_TESTS=OFF ${GMSH_PATH}/src/gmsh
    )
endif()
