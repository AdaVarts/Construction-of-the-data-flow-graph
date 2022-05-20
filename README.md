# Construction of the data flow graph

The tool is part of my bachelor project at Faculty of Informatics and Information Technologies, Slovak University of Technology. It is designed to simplify the process of inspection the symmetric block cipers implementation written in C within security analysis against DFA (Differential Fault Analysis). 

We implemented three main functionalities. With our tool we convert symmetric cipher algorithm written in C into LLVM code. Then we construct a data flow graph from customized data of an LLVM intermediate representation. The tool has a graphical user interface, using which we provide additional information about the constructed graph. We implemented the method of finding and displaying a path in the graph.

## How to start
### Setup
In order to use the first functionality of converting C into LLVM code, the GCC should be installed. We used gcc 10.3.0. Official installation instructions are written on the developers website
```
https://gcc.gnu.org/install/
```

Otherwise, the tool is a standalone Python application.

Notice: the `fake\_libc\_include` folder should be in the same folder as `start.exe` file (or `start.py` in case of running from python) in order to run the preprocessing of C file correctly.
### From Python
Run file `start.py` - runs main window of gui.

### From exe
To execute it, run the `start.exe` file.

## First window
1 - Choose a C file from a computer and press `Convert into LLVM IR` - it will generate an llvm ir module, which you can save on a computer with format `.ll` . The progress of generating is displayed in a form below.<br />
2 - Choose an llvm file from a computer and press `Load LLVM module` - it will load llvm from a file and execute the customization of every function. Then the window with customized functions is opened.

At the bottom of the window is a place for additional information from the processes during execution. If an error occurs during any of them, the message is also printed in this block. 

### LLVM module window:
The window contains 3 lists of functions:</br>
The first list determines the function, from which DFG will be constructed.</br>
The second list offers the option to unroll other functions in the main one if they are called.</br>
The third list offers the option to delete a specific function calls from the main one.</br>
Warning: deleting will be not executed if functions were already merged, or if a function to be deleted has more than 1 argument.</br>
Button `Generate model` runs merging and deleting chosen functions from the main one. It will trigger auto-filling of fields below describing the final function.</br>
After the entering a distance, at which the tool should find the nodes, and pressing the button `Find nodes`, the tool starts the construction of a customized data flow graph, then it searches for the nodes and the paths to them. The results are written below. The construction of DFG is done the first time by pressing the button `Find nodes`. Then, if entered distance changes, the program searches in an existing graph. The information about total number of edges and nodes will be written, as well asthe total number of found nodes, which are displayed in the list below.</br>
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
