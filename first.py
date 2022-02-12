# from msilib.schema import Error
# import llvmlite
import copy
from function_manag import merge_two_funcs
from llvm_parser import parse_llvm
from pycparser import parse_file#, preprocess_file
# import pyparsing as pp
# from llvmlite import ir
# from llvmlite import binding
import llvm_g 
# import io
# import ast
from DFG_structure import DFG, Edge, Node
from worker import WorkerSignals

def translate_to_c(filename, printW):
    st = parse_file(filename, use_cpp=True, 
            cpp_path='gcc', 
            cpp_args=['-E', r'-IC:/Users/Adalina/AppData/Local/Programs/Python/Python37/Lib/site-packages/pycparser/utils/fake_libc_include'],
            integer_types=False)
            # cpp_args=['-E'])
    # f = open("F:\\STU\\FIIT\\BP\\ast_pr.txt", "w")
    # st.show(buf = f)
    # f.close()

    generator = llvm_g.llvm_Generator(printW)
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

def save_one_tail(index, dfg, op):
    dfg, node = save_node(dfg, op.value)
    dfg, node1 = save_node(dfg, op.args[index])
    edge = Edge(op.name, node1, node) 
    dfg.edges.append(edge)   
    return dfg

def save_two_tails(dfg, op):
    dfg = save_one_tail(0, dfg, op)
    dfg = save_one_tail(1, dfg, op)
    return dfg

def start_DFG(dfg_def, function, distance, ret_value, progress):
    if dfg_def == None:
        dfg = create_dfg(function)
    

    k = 0
    nodes = []
    ret_node = dfg.nodes[ret_value]
    dfs(ret_node, k, int(distance), nodes)
    return nodes

def dfs(node, k, distance, found_nodes):
    for edge in node.incoming:
        if k+1 == distance:
            found_nodes.append(edge.tail)
            continue
        if k >= distance: continue
        dfs(edge.tail, k+1, distance, found_nodes)

def create_dfg(function):
    dfg = DFG()
    for op in function.labels[0].operations:
        try:
            if op.name == 'store':
                save_one_tail(0, dfg, op)
            elif op.name == 'br' or op.name == 'ret':
                continue
            # elif op.name == 'ret':
            #     dfg, node1 = save_node(dfg, op.args[0])
            #     edge = Edge(op.name, node1) 
            #     dfg.edges.append(edge)  
            elif op.name == 'phi':
                dfg, node = save_node(dfg, op.value)
                dfg, node1 = save_node(dfg, op.args[0][0])
                edge = Edge(op.name, node1, node) 
                dfg.edges.append(edge)
                dfg, node = save_node(dfg, op.value)
                dfg, node1 = save_node(dfg, op.args[1][0])
                edge = Edge(op.name, node1, node) 
                dfg.edges.append(edge)
            elif op.args is not None and len(op.args) == 2:
                save_two_tails(dfg, op)
            else:
                save_one_tail(0, dfg, op)
        except Exception as e:
            raise ValueError(f"{op.name}  -   {op.value} ; {op.args}  {format(e)}")
            
    print(dfg.__str__())
    return dfg

def convert_C_into_llvm(filename, printW):
    module = translate_to_c(filename, printW)
    m = module.__str__()
    return m

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
    sss = WorkerSignals()
    functions = parse_llvm("F:\\STU\\FIIT\\BP\\pr.ll", sss.progress)
    for f in functions:
        if f.name == 'encrypt':
            encrypt_f = copy.deepcopy(f)
        if f.name == 'Sbox':
            sbox_f = copy.deepcopy(f)
    merge_two_funcs(encrypt_f, sbox_f, sss.progress)
    # for f in functions:
    #     if f.name == 'encrypt':
    #         start_DFG(f)
