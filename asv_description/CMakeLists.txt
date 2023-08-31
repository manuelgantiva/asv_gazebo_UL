cmake_minimum_required(VERSION 3.8)
project(asv_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

# Install directory URDF
install(
  DIRECTORY launch rviz meshes config
  DESTINATION share/${PROJECT_NAME}/)

# Install xacro files / macros
install(DIRECTORY urdf/
  DESTINATION share/${PROJECT_NAME}/urdf)

# Install xacro files / macros
install(DIRECTORY models/
DESTINATION share/${PROJECT_NAME}/models)

ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in")
ament_environment_hooks("${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.sh.in")

ament_package()

