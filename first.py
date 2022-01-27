from msilib.schema import Error
import llvmlite
from llvm_parser import parse_llvm
from pycparser import parse_file, preprocess_file
import pyparsing as pp
from llvmlite import ir
from llvmlite import binding
import llvm_g 
import io
import ast
from DFG_structure import DFG, Edge, Node

def translate_to_c(filename):
    st = parse_file(filename, use_cpp=True, 
            cpp_path='gcc', 
            cpp_args=['-E', r'-IC:/Users/Adalina/AppData/Local/Programs/Python/Python37/Lib/site-packages/pycparser/utils/fake_libc_include'],
            integer_types=False)
            # cpp_args=['-E'])
    f = open("F:\\STU\\FIIT\\BP\\ast_pr.txt", "w")
    st.show(buf = f)
    f.close()

    # create functions as I want manually, it doesn't matter for graph

    

    generator = llvm_g.llvm_Generator()
    return generator.start(st)

def get_function(module, name_f):
    for f in module.functions:
        if f.name == name_f:
            return f

def save_node(dfg, name):
    node = dfg.get_node(name)
    if node is None:
        node = Node(name)
        dfg.nodes[node.name] = node
    return dfg, node

def save_one_tail(index, dfg, func_name, op):
    dfg, node = save_node(dfg, func_name+'-'+op.value)
    dfg, node1 = save_node(dfg, func_name+'-'+op.args[index])
    edge = Edge(op.name, node1, node) 
    dfg.edges.append(edge)   
    return dfg

def save_two_tails(dfg, func_name, op):
    dfg = save_one_tail(0, dfg, func_name, op)
    dfg = save_one_tail(1, dfg, func_name, op)
    return dfg

def start_DFG(function):

    dfg = DFG()
    for lbl in function.labels:
        for op in lbl.operations:
            try:
                if op.name == 'store' or op.name == 'ret':
                    save_one_tail(0, dfg, function.name, op)
                elif op.name == 'br':
                    continue
                elif op.name == 'phi':
                    dfg, node = save_node(dfg, function.name+'-'+op.value)
                    dfg, node1 = save_node(dfg, function.name+'-'+op.args[0][0])
                    edge = Edge(op.name, node1, node) 
                    dfg.edges.append(edge)
                    dfg, node = save_node(dfg, function.name+'-'+op.value)
                    dfg, node1 = save_node(dfg, function.name+'-'+op.args[1][0])
                    edge = Edge(op.name, node1, node) 
                    dfg.edges.append(edge)
                elif op.args is not None and len(op.args) == 2:
                    save_two_tails(dfg, function.name, op)
                else:
                    save_one_tail(0, dfg, function.name, op)
            except Exception as e:
                raise ValueError(f"{op.name}  -   {op.value} ; {op.args}  {format(e)}")
            
    print(dfg.__str__())
    

if __name__ == "__main__":
    # module = translate_to_c("F:\\STU\\FIIT\\BP\\Present.c")
    # translate_to_c("F:\\STU\\FIIT\\BP\\tests\\PR.c")

    # m = module.__str__()
    # llvm_ir_parsed = binding.parse_assembly(str(module))
    # llvm_ir_parsed.verify()


    # f1 = open("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll", "w")
    # f1.write(m)
    # f1.close()
    # print(m)

    functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll")
    for f in functions:
        if f.name == 'encrypt':
            start_DFG(f)
