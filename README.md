# Construction of the data flow graph

## How to start

Run file `startWind.py` - main window of gui

## Available options
1 - Choose C file from a computer and press `Convert into LLVM` - it will generate an llvm ir module, which you can save on a computer with format .ll . The progress of generating is displayed in a form on the right.<br />
2 - Choose llvm file from a computer and press `Build DFG`

## Libraries and environment
Python 3.7.4<br />
PyQt5 - for gui<br />
pycparser - for parsing C file<br />
llvmlite - for constructing llvm module<br />
