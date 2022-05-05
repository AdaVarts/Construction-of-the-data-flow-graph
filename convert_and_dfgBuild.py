import time
from addit_methods import is_constant
from library.pycparser import parse_file
import llvm_gen 
import os, sys
from classes import DFG, Edge, Node, WorkerSignals

# Preprocess C file with gcc and convert it to LLVM 
def translate_to_c(filename, printW):
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.abspath(__file__))

    dir_for_path = directory.replace('\\','/')
    logs_dir = dir_for_path+'/logs/'
    is_path = os.path.exists(logs_dir)
    if not is_path:
        os.makedirs(logs_dir)
    path = f'-I{dir_for_path}/fake_libc_include'
    st = parse_file(filename, use_cpp=True, 
        cpp_path='gcc', 
        cpp_args=['-E', r''+path],
        integer_types=False)
    f = open(f"{logs_dir}/ast_pr.txt", "w")
    st.show(buf = f)
    f.close()

    generator = llvm_gen.llvm_Generator(printW)
    generator.visit(st)
    return generator.module

def get_function(module, name_f):
    for f in module.functions:
        if f.name == name_f:
            return f

# Save one node into DFG
def save_node(dfg, name):
    node = dfg.get_node(name)
    if node is None:
        node = Node(name)
        dfg.nodes[node.name] = node
    return dfg, node

# Save an edge into DFG
def save_one_tail(index, dfg, op):
    dfg, node = save_node(dfg, op.value)
    try:
        dfg, node1 = save_node(dfg, op.args[index])
        for elem in set(node.incoming).intersection(node1.outgoing):
            if op.name == elem.name:
                return dfg
        edge = Edge(op.name, node1, node) 
    except:
        edge = Edge(op.name, None, node) 
    dfg.edges.append(edge)   
    return dfg

# Save two edges to one node into DFG
def save_two_tails(dfg, op):
    dfg = save_one_tail(0, dfg, op)
    dfg = save_one_tail(1, dfg, op)
    return dfg

# Save three edges to one node into DFG
def save_three_tails(dfg, op):
    dfg = save_one_tail(0, dfg, op)
    dfg = save_one_tail(1, dfg, op)
    dfg = save_one_tail(2, dfg, op)
    return dfg

# Create dfg if it doesn't exist and search for the nodes and paths
def start_DFG(dfg_def, function, distance, ret_value, progress):
    start_time=time.time()
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
    try:
        dfs(ret_node, k, int(distance), path, dfg_def.map_path)
    except:
        progress.emit(f"No node found")

    delay = time.time()-start_time
    progress.emit(f"DFS has finished")
    progress.emit(f"Delay: {delay}")
    return dfg_def

# Search for the nodes at entered distance with DFS and 
#  store them with their paths from a returning value
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

# Construct a DFG from the final function
def create_dfg(function, progress):
    dfg = DFG()
    progress.emit("Data Flow Graph: starting to build")
    for op in function.labels[0].operations:
        try:
            if op.name == 'br' or op.name == 'ret':
                continue 
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
            elif op.args is not None and len(op.args) == 3:
                save_three_tails(dfg, op)
            else:
                save_one_tail(0, dfg, op)
        except Exception as e:
            progress.emit(f"ValueError: {op.name}  -   {op.value} ; {op.args}  {format(e)}")
    progress.emit("Data Flow Graph: was built")
    return dfg

# Trigger the C into LLVM converting process
def convert_C_into_llvm(filename, printW):
    try:
        module = translate_to_c(filename, printW)
        m = module.__str__()
        return m
    except:
        printW.emit("Error: converting was not successful")
        return None

if __name__ == "__main__":
    sss = WorkerSignals()
    
    module = translate_to_c("F:\\STU\\FIIT\\BP\\Present.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\kalyna.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\aes.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\des.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\arcfour.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\base64.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\blowfish.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\md5.c", sss.progress)
    module = translate_to_c("F:\\STU\\FIIT\\BP\\rot-13.c", sss.progress)

