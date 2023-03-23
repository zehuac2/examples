add_executable(newtons-method main.cc)

set_target_properties(newtons-method PROPERTIES CXX_STANDARD 20)

add_test(newtons-method newtons-method)
