import llvmlite
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

def save_one_tail(index, dfg, func_name, instr, node_name=None):
    dfg, node = save_node(dfg, func_name+'-'+instr.name)
    value_name0 = str(instr.operands[index].constant) \
        if isinstance(instr.operands[index], ir.Constant) \
        else func_name+'-'+instr.operands[index].name
    dfg, node1 = save_node(dfg, value_name0)
    if node_name is not None:
        edge = Edge(node_name, node1, node) 
    else: edge = Edge(instr.opname, node1, node) 
    dfg.edges.append(edge)   
    return dfg

def save_two_tails(index1, index2, dfg, func_name, instr):
    dfg = save_one_tail(index1, dfg, func_name, instr)
    dfg = save_one_tail(index2, dfg, func_name, instr)
    return dfg

class Loop:
    precond = None
    loop = None
    cond = None
    end = None
    def __init__(self, precond=None, loop=None, cond=None, end=None):
        self.precond = precond
        self.loop = loop
        self.cond = cond
        self.end = end

def unroll(module):
    for func in module.functions:
        blocks_len = len(func.blocks)
    encrypt = get_function(module, 'encrypt')
    loops = {}
    for block in encrypt.blocks:
        print(block.name)
        if "for_precond" in block.name:
            loops[block.name]= Loop(precond=block)
        elif "for_" in block.name:
            setattr(loops[block.name.replace(block.name.split('.')[0], 'for_precond')], block.name.split('.')[0].replace('for_', ''), block)
    print(loops)
    new_loops = []
    for loop in loops.values():
        names = [loop.precond.name, loop.loop.name, loop.cond.name, loop.end.name]
        for instr in loop.precond.instructions:
            if instr.opname == "icmp" and len(loop.precond.instructions)-loop.precond.instructions.index(instr) == 2:
                n = int(instr.operands[1].constant)
        for i in range(1, n):
            new_loops.append(ir.Block(encrypt, name=loop.precond.name+"-"+str(i)))
            new_loops.append(ir.Block(encrypt, name=loop.loop.name+"-"+str(i)))
            new_loops.append(ir.Block(encrypt, name=loop.cond.name+"-"+str(i)))
            for instr_b in loop.precond.instructions:
                new_loops[len(new_loops)-3].instructions.append(ir.Instruction(new_loops[len(new_loops)-3], instr_b.type, instr_b.opname, instr_b.operands, instr_b.name))
                # new_loops[len(new_loops)-1].instructions.append(getattr(ir.instructions, str(instr_b.__class__).split('.')[-1][:-2])(new_loops[len(new_loops)-1], instr_b.operands[0], instr_b.name))
                # if instr_b.opname == 'br':
                    # if instr_b.operands[1].name in names:
                    #     instr_b.operands[1].name = instr_b.operands[1].name+'-'+str(i)
                    # if len(instr_b.operands)==3 and instr_b.operands[2].name in names:
                    #     instr_b.operands[2].name = instr_b.operands[2].name+'-'+str(i)
            
            for instr_b in loop.loop.instructions:
                new_loops[len(new_loops)-2].instructions.append(ir.Instruction(new_loops[len(new_loops)-2], instr_b.type, instr_b.opname, instr_b.operands, instr_b.name))
            for instr_b in loop.loop.instructions:
                new_loops[len(new_loops)-1].instructions.append(ir.Instruction(new_loops[len(new_loops)-1], instr_b.type, instr_b.opname, instr_b.operands, instr_b.name))

            print(new_loops[-3])
            print(new_loops[-2])
            print(new_loops[-1])
            


def start_DFG(module):
    encrypt = get_function(module, 'encrypt')
    print("-------------------------------")
    # print(module)

    dfg = DFG()
    for block in encrypt.blocks:
        for instr in block.instructions:
            
            if instr.opname == 'store':
                value_name1 = str(instr.operands[1].constant) if isinstance(instr.operands[1], ir.Constant) else encrypt.name+'-'+instr.operands[1].name
                value_name0 = str(instr.operands[0].constant) if isinstance(instr.operands[0], ir.Constant) else encrypt.name+'-'+instr.operands[0].name
                dfg, node = save_node(dfg, value_name1)
                dfg, node1 = save_node(dfg, value_name0)
                edge = Edge(instr.opname, node1, node)
                dfg.edges.append(edge)
            # elif instr.opname == 'alloca':
            #     node = dfg.get_node(encrypt.name+'-'+instr.name)
            #     if node is None:
            #         node = Node(encrypt.name+'-'+instr.name)
            #         dfg.nodes[node.name] = node
            elif instr.opname == 'load':
                dfg = save_one_tail(0, dfg, encrypt.name, instr)
            elif instr.opname == 'bitcast':
                dfg = save_one_tail(0, dfg, encrypt.name, instr)
            # elif instr.opname == 'getelementptr':
                # dfg = save_two_tails(0, 2, dfg, encrypt.name, instr)
            elif instr.opname == 'add' or instr.opname == 'xor':
                dfg = save_two_tails(0, 1, dfg, encrypt.name, instr)
            elif instr.opname == 'call':
                if len(instr.operands)<=1: continue
                dfg = save_one_tail(1, dfg, encrypt.name, instr, instr.callee.name)
            
    dfg.rearange()
    print(dfg.__str__())
    

if __name__ == "__main__":
    module = translate_to_c("F:\\STU\\FIIT\\BP\\Present.c")
    # translate_to_c("F:\\STU\\FIIT\\BP\\tests\\PR.c")

    m = module.__str__()
    # llvm_ir_parsed = binding.parse_assembly(str(module))
    # llvm_ir_parsed.verify()


    f1 = open("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll", "w")
    f1.write(m)
    f1.close()
    print(m)

    # unroll(module)

    start_DFG(module)

    # TODO: 
    # + forloopend is not in the end
    # + return from function is not always present
    # + br in the end of each branch
    # + edges
    # unloop
    # + integer types into 2 options
    # + call func as 1 edge - for now
    # -+ find a way to ignore alloca, store, load