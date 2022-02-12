# Construction of the data flow graph

## How to start

Run file `startWind.py` - main window of gui

## Available options
1 - Choose a C file from a computer and press `Convert into LLVM` - it will generate an llvm ir module, which you can save on a computer with format `.ll` . The progress of generating is displayed in a form on the right.<br />
2 - Choose an llvm file from a computer and press `Build DFG` - it will load llvm from a file and execute the customization of every function. Then the window with customized functions is opened.

### LLVM module window:
The window contains 3 lists of functions:</br>
The first list determines the function, from which DFG will be constructed.</br>
The second list offers the option to unroll other functions in the main one if they are called.</br>
The third list offers the option to delete a specific function from the main one. All instances of calling this function in the main one will be excluded.</br>
Warning: deleting will be not executed if functions were already merged, or if a function to be deleted has more than 1 argument.</br>
Button `Generate model` will run merging and deleting chosen functions from the main one. It will trigger auto-filling of fields below describing the final function.

## Customisation 
excluding memory management operations</br>
identification variables based on functions</bt>
unrolling, where possible</br>
SSA for variables in every function</br>

## Libraries and environment
Python 3.7.4<br />
PyQt5 - for gui<br />
pycparser - for parsing C file<br />
llvmlite - for constructing llvm module<br />
