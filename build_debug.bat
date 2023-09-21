@echo off

cmake -DCMAKE_BUILD_TYPE="Debug" -B "./build" -G"Visual Studio 12 2013" -A Win32
cmake --build ./build --config Debug