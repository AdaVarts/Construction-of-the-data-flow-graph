#-----------------------------------------------------------------
# pycparser: __init__.py
#
# This package file exports some convenience functions for
# interacting with pycparser
#
# Eli Bendersky [https://eli.thegreenplace.net/]
# License: BSD
#-----------------------------------------------------------------
__all__ = ['c_lexer', 'c_parser', 'c_ast']
__version__ = '2.20'

import io
from subprocess import check_output
from .c_parser import CParser


def preprocess_file(filename, cpp_path='cpp', cpp_args=''):
    """ Preprocess a file using cpp.

        filename:
            Name of the file you want to preprocess.

        cpp_path:
        cpp_args:
            Refer to the documentation of parse_file for the meaning of these
            arguments.

        When successful, returns the preprocessed file's contents.
        Errors from cpp will be printed out.
    """
    path_list = [cpp_path]
    if isinstance(cpp_args, list):
        path_list += cpp_args
    elif cpp_args != '':
        path_list += [cpp_args]
    path_list += [filename]

    try:
        # Note the use of universal_newlines to treat all newlines
        # as \n for Python's purpose
        text = check_output(path_list, universal_newlines=True)
    except OSError as e:
        raise RuntimeError("Unable to invoke 'cpp'.  " +
            'Make sure its path was passed correctly\n' +
            ('Original error: %s' % e))

    return text

# def change_annotations(text):
#     text_tmp = text.split('\n')
    
#     for line in text_tmp:
#         change = False
#         if "typedef int" in line:
#             line_spl = line.split(' ')
#             if "8" in line_spl[2]:
#                 line_spl[1] = "char"
#                 change = True
#             elif "16" in line_spl[2]:
#                 line_spl[1] = "short"
#                 change = True
#             elif "64" in line_spl[2]:
#                 line_spl[1] = "long"
#                 change = True
#             if change:
#                 i = text_tmp.index(line)
#                 text_tmp.remove(line)
#                 line2 = ""
#                 for l in line_spl:
#                     line2 += l + " "
#                 text_tmp.insert(i, line2)
#                 # line = line2

#     text2 = ""
#     for line in text_tmp:
#         text2 += line + "\n"
#     return text2

def compare_replace(text, text2):
    source = text2.split('\n')
    source_list = {}
    for line in source:
        if "typedef " in line and "struct" not in line:
            type_defined = line.split(' ')
            while '' in type_defined:
                type_defined.remove('')
            if type_defined[1] == 'char' or type_defined[1] == 'long' or type_defined[1] == 'short':
                source_list[type_defined[-1]] = type_defined[1]

    dest = text.split('\n')
    for line in dest:
        if "typedef int " in line:
            line_new = line.split(' ')
            type_need = line_new[2]
            if type_need in source_list:
                tp_n_f = source_list[type_need]
                if tp_n_f is not None:
                    line_new[1] = tp_n_f
                    i = dest.index(line)
                    dest.remove(line)
                    line2 = ""
                    for l in line_new:
                        line2 += l + " "
                    dest.insert(i, line2)
                    line = line2

    text_ret = ""
    for line in dest:
        text_ret += line + '\n'
    return text_ret

def remove_annotation(text, filename):

    UNNESS = ["__ext", "__dl", "bute__((__cd", "__att", "__res", "__unu",  "__nothrow__", "extern", "signed"]
    # UN_LINE = ["__non", "__inline__", "__attribute__((__format__"]

    text_tmp = text.split('\n')
    for line in text_tmp:
        line_spl = line.split(' ')
        if ("typedef struct" in line and "__" in line) or any(iil in line for iil in UNNESS):
            j = 0
            while j<len(line_spl):
                word = line_spl[j]
                if ("typedef struct" in line_spl and "__" in word) or any(iil in word for iil in UNNESS):
                    line_spl.remove(word)
                    i = text_tmp.index(line)
                    text_tmp.remove(line)
                    line2 = ""
                    for l in line_spl:
                        line2 += l + " "
                    text_tmp.insert(i, line2)
                    line = line2
                    j-=1
                j+=1
                

    text2 = ""
    for line in text_tmp:
        text2 += line + "\n"
    return text2

def parse_file(filename, use_cpp=False, cpp_path='cpp', cpp_args='',
               parser=None, integer_types=True):
    """ Parse a C file using pycparser.

        filename:
            Name of the file you want to parse.

        use_cpp:
            Set to True if you want to execute the C pre-processor
            on the file prior to parsing it.

        cpp_path:
            If use_cpp is True, this is the path to 'cpp' on your
            system. If no path is provided, it attempts to just
            execute 'cpp', so it must be in your PATH.

        cpp_args:
            If use_cpp is True, set this to the command line arguments strings
            to cpp. Be careful with quotes - it's best to pass a raw string
            (r'') here. For example:
            r'-I../utils/fake_libc_include'
            If several arguments are required, pass a list of strings.

        parser:
            Optional parser object to be used instead of the default CParser

        When successful, an AST is returned. ParseError can be
        thrown if the file doesn't parse successfully.

        Errors from cpp will be printed out.
    """
    if use_cpp:
        text = preprocess_file(filename, cpp_path, cpp_args)
        if integer_types: text2 = preprocess_file(filename, cpp_path, cpp_args = ['-E'])
    else:
        with io.open(filename) as f:
            text = f.read()

    text = remove_annotation(text, filename)
    if integer_types:
        text2 = remove_annotation(text2, filename)
        text = compare_replace(text, text2)
        file2 = open("preprocesse.c", "w") 
        file2.write(text2)
        file2.close()

    print(text)
    file3 = open("prep_file.c", "w") 
    file3.write(text)
    file3.close()
    
    if parser is None:
        parser = CParser()
    return parser.parse(text, filename)
