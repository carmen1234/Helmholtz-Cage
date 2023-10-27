cmake_minimum_required(VERSION 3.0)
project(hcage_gui)

find_package(wxWidgets COMPONENTS core base xrc REQUIRED)


include(${wxWidgets_USE_FILE})
add_subdirectory(mathplot)


set(ROOT "${CMAKE_CURRENT_LIST_DIR}")



set(SRC_DIR "src/")
file(GLOB SRCFILES "${SRC_DIR}/*.cpp")


add_executable(${PROJECT_NAME} "${SRCFILES}")
target_include_directories(${PROJECT_NAME} PRIVATE ${EXTERNAL_LIB_HEADERS} "include/")
target_link_libraries(${PROJECT_NAME} ${wxWidgets_LIBRARIES} mathplot)

install (TARGETS ${PROJECT_NAME} RUNTIME DESTINATION bin)


