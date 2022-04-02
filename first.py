# from msilib.schema import Error
# import llvmlite
# import copy
# import typing
from addit_methods import is_constant
from function_manag import merge_in_one, merge_two_funcs
from llvm_parser import parse_llvm
from pycparser import parse_file#, preprocess_file
# import pyparsing as pp
# from llvmlite import ir
# from llvmlite import binding
import llvm_g 
# import io
# import ast
from classes import DFG, Edge, Node, WorkerSignals

def translate_to_c(filename, printW):
    st = parse_file(filename, use_cpp=True, 
            cpp_path='gcc', 
            cpp_args=['-E', r'-IC:/Users/Adalina/AppData/Local/Programs/Python/Python37/Lib/site-packages/pycparser/utils/fake_libc_include'],
            integer_types=False)
            # cpp_args=['-E'])
    f = open("F:\\STU\\FIIT\\BP\\ast_pr.txt", "w")
    st.show(buf = f)
    f.close()

    generator = llvm_g.llvm_Generator(printW)
    generator.visit(st)
    return generator.llvm_module

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
    try:
        dfg, node1 = save_node(dfg, op.args[index])
        edge = Edge(op.name, node1, node) 
    except:
        edge = Edge(op.name, None, node) 
    dfg.edges.append(edge)   
    return dfg

def save_two_tails(dfg, op):
    dfg = save_one_tail(0, dfg, op)
    dfg = save_one_tail(1, dfg, op)
    return dfg

def start_DFG(dfg_def, function, distance, ret_value, progress):
    if dfg_def == None:
        dfg_def = create_dfg(function, progress)
    
    k = 0
    try:
        ret_node = dfg_def.nodes[ret_value]
    except:
        progress.emit(f"Error: returning node is not found")
        return []
    progress.emit(f"starting DFS to length {distance}")
    path = []
    nodes = []
    dfs(ret_node, k, int(distance), path, dfg_def.map_path)

    progress.emit(f"DFS has finished")
    return dfg_def

def dfs(node, k, distance, path, map_path):
    for edge in node.incoming:
        if k+1 == distance:
            path.append([k+1, edge.tail, edge])
            if edge.tail.name not in map_path:
                map_path[edge.tail.name] = []
                map_path[edge.tail.name].append([item for item in path])
            elif is_constant(edge.tail.name):
                map_path[edge.tail.name].append([item for item in path])
            path.pop()
            continue
        if k >= distance: return
        path.append([k+1, edge.tail, edge])
        dfs(edge.tail, k+1, distance, path, map_path)
        path.pop()

def create_dfg(function, progress):
    dfg = DFG()
    progress.emit("Data Flow Graph: starting to build")
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
            progress.emit(f"ValueError: {op.name}  -   {op.value} ; {op.args}  {format(e)}")
    progress.emit("Data Flow Graph: was built")
    # print(dfg.__str__())
    return dfg


def convert_C_into_llvm(filename, printW):
    module = translate_to_c(filename, printW)
    m = module.__str__()
    return m

if __name__ == "__main__":
    sss = WorkerSignals()
    
    # module = translate_to_c("F:\\STU\\FIIT\\BP\\Present.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\kalyna.c", sss.progress)
    # translate_to_c("F:\\STU\\FIIT\\BP\\tests\\PR.c")

    # m = module.__str__()
    # llvm_ir_parsed = binding.parse_assembly(str(module))
    # llvm_ir_parsed.verify()

    # f1 = open("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll", "w")
    # f1.write(m)
    # f1.close()
    # print(m)


    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\pr.ll", sss.progress)
    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll", sss.progress)
    # func = merge_in_one(functions, 'encrypt', ['Sbox'], ['fromHexStringToBytes', 'fromBytesToLong', 'fromHexStringToLong', 'fromLongToBytes', 'fromLongToHexString'], sss.progress)
    
    # merge_two_funcs(encrypt_f, sbox_f, sss.progress)
    
    # dfg = create_dfg(func, sss.progress)
    # for key in dfg.nodes.keys():
    #     if 'encrypt' not in key:
    #         print(key)
    # print("*******")
    # start_DFG(dfg, func, 4, f'encrypt_%state-63', sss.progress)
    # start_DFG(dfg, func, 5, f'encrypt_%state-63', sss.progress)
    # start_DFG(dfg, func, 6, f'encrypt_%state-63', sss.progress)
    # start_DFG(dfg, func, 7, f'encrypt_%state-63', sss.progress)
    # start_DFG(dfg, func, 9, f'encrypt_%state-63', sss.progress)
    # path = get_path(dfg, 7, '1', f'encrypt_%state-63', 2, sss.progress)
    # for i, n in path.items():
        # print(n)
    
    # for f in functions:
    #     if f.name == 'encrypt':
    #         start_DFG(f)
