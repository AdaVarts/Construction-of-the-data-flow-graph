# from msilib.schema import Error
# import llvmlite
import copy
from function_manag import merge_in_one, merge_two_funcs
from llvm_parser import parse_llvm
from pycparser import parse_file#, preprocess_file
# import pyparsing as pp
# from llvmlite import ir
# from llvmlite import binding
import llvm_g 
# import io
# import ast
from classes import DFG, Edge, Node
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
    nodes = []
    try:
        ret_node = dfg_def.nodes[ret_value]
    except:
        progress.emit(f"Error: returning node is not found")
        return []
    progress.emit(f"starting DFS to length {distance}")
    dfs(ret_node, k, int(distance), nodes)
    progress.emit(f"DFS has finished")
    return nodes

def dfs(node, k, distance, found_nodes):
    for edge in node.incoming:
        if k+1 == distance:
            found_nodes.append(edge.tail)
            continue
        if k >= distance: return
        dfs(edge.tail, k+1, distance, found_nodes)

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
            raise ValueError(f"{op.name}  -   {op.value} ; {op.args}  {format(e)}")
    progress.emit("Data Flow Graph: was built")
    # print(dfg.__str__())
    return dfg

def get_path(dfg, distance, value, ret_value, number, progress):
    path = {}
    ret_node = dfg.nodes[ret_value]
    dfs_for_path(ret_node, 0, int(distance), value, 0, number, path)
    return path

def dfs_for_path(node: Node, k, distance, value, found_n, number, path):
    for edge in node.incoming:
        if k+1 == distance and edge.tail.name == value:
            found_n += 1
            if number == 0 or found_n == number:
                path[k+1] = [edge.tail, edge]
                return found_n
            else: continue
        if k >= distance:
            return found_n
        found_n = dfs_for_path(edge.tail, k+1, distance, value, found_n, number, path)
        if found_n == number:
            path[k+1] = [edge.tail, edge]
            return found_n
    return found_n

def convert_C_into_llvm(filename, printW):
    module = translate_to_c(filename, printW)
    m = module.__str__()
    return m

# if __name__ == "__main__":
#     # module = translate_to_c("F:\\STU\\FIIT\\BP\\Present.c")
#     # translate_to_c("F:\\STU\\FIIT\\BP\\tests\\PR.c")

#     # m = module.__str__()
#     # llvm_ir_parsed = binding.parse_assembly(str(module))
#     # llvm_ir_parsed.verify()


#     # f1 = open("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll", "w")
#     # f1.write(m)
#     # f1.close()
#     # print(m)
#     sss = WorkerSignals()
#     functions = parse_llvm("F:\\STU\\FIIT\\BP\\pr.ll", sss.progress)
#     # for f in functions:
#     #     if f.name == 'encrypt':
#     #         encrypt_f = copy.deepcopy(f)
#     #     if f.name == 'Sbox':
#     #         sbox_f = copy.deepcopy(f)
#     func = merge_in_one(functions, 'encrypt', ['Sbox'], ['fromHexStringToBytes', 'fromBytesToLong', 'fromHexStringToLong', 'fromLongToBytes', 'fromLongToHexString'], sss.progress)
#     # merge_two_funcs(encrypt_f, sbox_f, sss.progress)
#     dfg = create_dfg(func, sss.progress)
#     path = get_path(dfg, 7, '1', f'encrypt_%state-63', 2, sss.progress)
#     for i, n in path.items():
#         print(n)
#     # for f in functions:
#     #     if f.name == 'encrypt':
#     #         start_DFG(f)
