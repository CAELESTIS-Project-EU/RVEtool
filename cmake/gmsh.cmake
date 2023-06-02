function(gmsh)

  if(ENABLE_GMSH)
    
    include_directories(${GMSH_INCLUDE_DIR})
    target_link_libraries(${PROJECT_NAME} gmsh)
    
  endif()
  
endfunction()
