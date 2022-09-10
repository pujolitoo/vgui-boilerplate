# VGui template
Create vgui style standalone application.

![alt text](https://github.com/pujolitoo/vgui-boilerplate/blob/master/res/demo.png?raw=true)

## Building

First, clone the repository:

```
git clone --recursive https://github.com/pujolitoo/vgui-boilerplate.git
```

Then, enter the repo directory:

```
cd vgui-boilerplate
```

> The application must be compiled on Visual Studio 2013 toolset and targetting x86, otherwise it won't work.

```
mkdir build
cd build
cmake .. -G"Visual Studio 12 2013" -A Win32
cmake --build .
```