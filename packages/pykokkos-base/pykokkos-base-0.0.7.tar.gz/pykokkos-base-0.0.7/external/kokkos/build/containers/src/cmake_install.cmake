# Install script for directory: /Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/containers/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/opt/kokkos")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/opt/local/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/containers/src/" FILES_MATCHING REGEX "/[^/]*\\.hpp$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.3.6.99.dylib"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.3.6.dylib"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.3.6.99.dylib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.3.6.dylib"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      execute_process(COMMAND /usr/bin/install_name_tool
        -delete_rpath "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/core/src"
        "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/opt/local/bin/strip" -x "${file}")
      endif()
    endif()
  endforeach()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.dylib")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/core/src"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/opt/local/bin/strip" -x "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.3.6.99.dylib"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.3.6.dylib"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.3.6.99.dylib"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.3.6.dylib"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      execute_process(COMMAND /usr/bin/install_name_tool
        -delete_rpath "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/core/src"
        "${file}")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/opt/local/bin/strip" -x "${file}")
      endif()
    endif()
  endforeach()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/src/libkokkoscontainers.dylib")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    execute_process(COMMAND /usr/bin/install_name_tool
      -delete_rpath "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/core/src"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/opt/local/bin/strip" -x "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libkokkoscontainers.dylib")
    endif()
  endif()
endif()

