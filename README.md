# Construction of the data flow graph

The tool is a result of bachelor project.

## How to start

Run file `startWind.py` - main window of gui

## Available options
1 - Choose a C file from a computer and press `Convert into LLVM IR` - it will generate an llvm ir module, which you can save on a computer with format `.ll` . The progress of generating is displayed in a form below.<br />
2 - Choose an llvm file from a computer and press `Load LLVM module` - it will load llvm from a file and execute the customization of every function. Then the window with customized functions is opened.

### LLVM module window:
The window contains 3 lists of functions:</br>
The first list determines the function, from which DFG will be constructed.</br>
The second list offers the option to unroll other functions in the main one if they are called.</br>
The third list offers the option to delete a specific function from the main one. All instances of calling this function in the main one will be excluded.</br>
Warning: deleting will be not executed if functions were already merged, or if a function to be deleted has more than 1 argument.</br>
Button `Generate model` runs merging and deleting chosen functions from the main one. It will trigger auto-filling of fields below describing the final function.</br>
By entering a 'distance value' and pressing `Find nodes` program will find all nodes that are at provided distance from a returning variable. If there are multiple returning variables detected, user can choose one, or the first in the list will be chosen automatically. Then the tool will construct a data flow graph (in case of pressing the button for the first time), and search for the path. The information about total edges and nodes will be written, as well asthe total number of found nodes, which are displayed in the list below.</br>
If a user chooses 1 node from this list and presses `Display path`, it will display a path between returning node and chosen one in the table on the right.

## Customization 
excluding memory management operations</br>
identification variables based on functions</bt>
unrolling, where possible</br>
SSA for variables in every function</br>

## Libraries and environment
Python 3.7.4<br />
PyQt5 - for gui<br />
pycparser - for parsing C file<br />
llvmlite - for constructing llvm module<br />
