# Install script for directory: /Users/jrmadsen/devel/python/pykokkos-base/external/kokkos

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

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/core/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/containers/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/algorithms/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/example/cmake_install.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos" TYPE FILE FILES
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosConfig.cmake"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosConfigCommon.cmake"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosConfigVersion.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos/KokkosTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos/KokkosTargets.cmake"
         "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/CMakeFiles/Export/lib/cmake/Kokkos/KokkosTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos/KokkosTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos/KokkosTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos" TYPE FILE FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/CMakeFiles/Export/lib/cmake/Kokkos/KokkosTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/Kokkos" TYPE FILE FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/CMakeFiles/Export/lib/cmake/Kokkos/KokkosTargets-release.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_config.h")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE PROGRAM FILES
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/bin/nvcc_wrapper"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/bin/hpcbind"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/temp/kokkos_launch_compiler"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE FILE FILES
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_config.h"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_Config_FwdBackend.hpp"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_Config_SetupBackend.hpp"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_Config_DeclareBackend.hpp"
    "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/KokkosCore_Config_PostInclude.hpp"
    )
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/Users/jrmadsen/devel/python/pykokkos-base/external/kokkos/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
