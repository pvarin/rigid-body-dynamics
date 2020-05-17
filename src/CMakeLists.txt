cmake_minimum_required(VERSION 3.17)
project(
    rigid-body-dynamics
    LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)

# Installed with Homebrew
find_package (Eigen3 3.3 REQUIRED NO_MODULE)

add_executable(
    main
    main.cpp
)

add_library(
    spatial_vectors STATIC
    spatial_vectors.h
    spatial_vectors.cpp
)
    
add_executable(
    test_spatial_vectors
    test_spatial_vectors.cpp 
)

target_link_libraries(
    main
    PRIVATE spatial_vectors
)
target_link_libraries(
    spatial_vectors
    PUBLIC Eigen3::Eigen
)
target_link_libraries(
    test_spatial_vectors
    PRIVATE spatial_vectors
)