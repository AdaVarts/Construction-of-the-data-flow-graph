import copy
from classes import Function, Operation, Label
from memory_management import memory_manag, rename_front_arg
from addit_methods import *
from worker import WorkerSignals

def load_llvm(filename, progress):
    functions = []
    known_funcs = []

    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()

    start = False
    progress.emit("start loading")
    for line in lines:
        data = line.split(' ')
        data = remove_empty(data)
        if data[0] == 'define':
            is_params = False
            count = 0
            for word in data:
                if '@' in word:
                    functions.append(Function(get_name(word.split('(')[0]), []))
                    is_params = True
                    count = 1
                    functions[-1].labels.append(Label(''))
                    continue
                if ')' in word:
                    functions[-1].params.append(get_name(word[:-1]))
                    break
                if is_params and count % 2 == 1:
                    functions[-1].params.append(get_name(word[:-1]))
                    count += 1
                elif is_params:
                    count += 1
            start = True
        elif data[0] == 'declare':
            for word in data:
                if '@' in word:
                    known_funcs.append(get_name(word.split('(')[0]))
                    break
            start = True
        elif start:
            if ':' in data[0]:
                if len(functions[-1].labels[-1].operations) == 0:
                    functions[-1].labels[-1].name = data[0].split(':')[0]
                    functions[-1].label_map[functions[-1].labels[-1].name] = functions[-1].labels[-1]
                else:
                    functions[-1].labels.append(Label(data[0].split(':')[0]))
                    functions[-1].label_map[functions[-1].labels[-1].name] = functions[-1].labels[-1]
            elif 'alloca' in data:
                continue
            elif 'store' in data:
                functions[-1].labels[-1].operations.append(Operation('store', value=get_name(data[4]),
                                                                    args=[get_name(data[2])]))
            elif 'call' in data and '=' in data and '...' not in line:
                functions[-1].labels[-1].operations.append(Operation(get_name(data[4].split('(')[0]),
                                                                    value=get_name(data[0]),
                                                                    args=get_args(data)))
            elif 'bitcast' in data:
                functions[-1].labels[-1].operations.append(Operation('bitcast',
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(data[4])]))
            elif 'load' in data:
                functions[-1].labels[-1].operations.append(Operation('load',
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(data[5])]))
            elif 'icmp' in data:
                functions[-1].labels[-1].operations.append(Operation('icmp',
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(data[3]), get_name(data[5]), get_name(data[6])]))
            elif 'getelementptr' in data:
                word = line.split(',')
                functions[-1].labels[-1].operations.append(Operation('getelementptr',
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(word[1].split(' ')[-1]), get_name(word[2].split(' ')[-1])]))
            elif 'mul' in data or 'and' in data or 'add' in data or 'sub' in data or 'or' in data or 'shl' in data or 'lshr' in data or 'xor' in data:
                functions[-1].labels[-1].operations.append(Operation(data[2],
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(data[4]), get_name(data[5])]))
            elif 'trunc' in data or 'sext' in data:
                functions[-1].labels[-1].operations.append(Operation(data[2],
                                                                    value=get_name(data[0]),
                                                                    args=[get_name(data[4])]))
            elif 'ret' in data:
                functions[-1].labels[-1].operations.append(Operation('ret',
                                                                    value='',
                                                                    args=[get_name(data[2])]))
            elif 'br' in data and len(data) == 3:
                functions[-1].labels[-1].operations.append(Operation('br',
                                                                    value=get_name(data[2])))
            elif 'br' in data:
                functions[-1].labels[-1].operations.append(Operation('br',
                                                                    value=get_name(data[2]),
                                                                    args=[get_name(data[4]), get_name(data[6])]))
            elif 'phi' in data:
                functions[-1].labels[-1].operations.append(Operation('phi',
                                                                    value=get_name(data[0]),
                                                                    args=[[get_name(line.split(',')[0].split(' ')[-1]), get_name(line.split(',')[1])],
                                                                        [get_name(line.split(',')[2]), get_name(line.split(',')[3])]]))

    progress.emit("end loading")
    progress.emit("start customising")
    functions = memory_manag(functions, known_funcs)
    progress.emit("end memory management")

    with open("F:\\STU\\FIIT\\BP\\output_llvm.txt", "w") as f:
        for func in functions:
            f.write(func.name)
            f.write('\n')
            f.write(str(func.params))
            f.write('\n')
            for label in func.labels:
                f.write('   '+label.name+'\n')
                for op in label.operations:
                    f.write('      '+op.name+': '+op.value+'\n')
                    if op.args is not None: f.write('         '+str(op.args)+'\n')
    print('-----')
    for func in known_funcs:
        print(func)
    
    return functions, known_funcs


def br_two(functions, op):
    val = op.value
    num = None
    for label in functions[-1].labels[::-1]:
        for oper in label.operations[::-1]:
            if val == oper.value:
                if oper.name == 'icmp':
                    val = oper.args[1]
                    num = oper.args[2]
                    continue
                elif oper.name == 'load' or oper.name == 'store':
                    val = oper.args[0]
                elif oper.name == 'add':
                    num = str(int(num)-int(oper.args[1]))
                    val = oper.args[0]
                elif oper.name == 'sub':
                    num = str(int(num)+int(oper.args[1]))
                    val = oper.args[0]
                elif oper.name == 'mul':
                    num = str(int(num)/int(oper.args[0]))
                    val = oper.args[1]
                elif oper.name == 'div':
                    num = str(int(num)*int(oper.args[0]))
                    val = oper.args[1]
                if is_constant(val):
                    if val != num:
                        return op.args[0]
                    else:
                        return op.args[1]
    return False
    # raise RuntimeError("ERROR while unrolling br with two branches")

def add_l2(source, functions, l2):
    branch = None
    for op in l2.operations:
        functions[-1].labels[-1].operations.append(copy.deepcopy(op))
        if op.name == 'br' and op.args is None:
            functions[-1].labels[-1].operations[-1].value = \
                '%' + get_current_name(reduce_to_value(functions[-1].labels[-1].operations[-1].value), functions[-1])
            branch = op.value
            return branch, functions
        elif op.name == 'br':
            functions[-1].labels[-1].operations.append(Operation(op.name, op.value,
                                                        ['%'+get_current_name(reduce_to_value(arg), functions[-1]) for arg in op.args]))
            branch, functions = unroll_two(source, functions, op)
    return branch, functions

def add_label(source, functions, l1, l2):
    branch = None
    for op in l1.operations:
        functions[-1].labels[-2].operations.append(copy.deepcopy(op))
        if op.name == 'br' and op.args is None:
            functions[-1].labels[-2].operations[-1].value = \
                '%' + get_current_name(reduce_to_value(functions[-1].labels[-2].operations[-1].value), functions[-1])
            branch = op.value
            br2, functions = add_l2(source, functions, l2)
            if branch == br2:
                return branch, functions
            else:
                pass
                # unroll_label
        elif op.name == 'br':
            functions[-1].labels[-2].operations.append(Operation(op.name, op.value,
                                                                 [get_current_name(reduce_to_value(arg), functions[-1]) for arg in op.args]))
            branch, functions = unroll_two(source, functions, op)
    return branch, functions


def unroll_two(source, functions, op):
    # if not in_function(functions[-1], op.args[0]):
    functions[-1].labels.append(Label(set_new_name(reduce_to_value(op.args[0]), functions[-1].ssa_map_lbl)))
    # if not in_function(functions[-1], op.args[1]):
    functions[-1].labels.append(Label(set_new_name(op.args[1][1:], functions[-1].ssa_map_lbl)))
    branch, functions = add_label(source, functions, source.label_map[op.args[0][1:]], source.label_map[op.args[1][1:]])
    return branch, functions

def unroll_label(source, functions, l):
    for op in l.operations:
        if op.name == 'br':
            if op.args is None:
                functions = unroll_label(source, functions, source.label_map[op.value[1:]])
                return functions
            else:
                lbl = br_two(functions, op)
                if not lbl:
                    functions[-1].labels[-1].operations.append(Operation(op.name, op.value,
                                                               ['%'+get_current_name(reduce_to_value(arg), functions[-1]) for arg in op.args]))
                    branch, functions = unroll_two(source, functions, op)
                    functions[-1].labels.append(Label(set_new_name(branch[1:], functions[-1].ssa_map_lbl)))
                    functions = unroll_label(source, functions, source.label_map[get_the_real_name(branch[1:])])
                else:
                    index_l = functions[-1].labels.index(functions[-1].labels[-1])
                    index_op = functions[-1].labels[-1].operations.index(functions[-1].labels[-1].operations[-1])
                    functions = unroll_label(source, functions, source.label_map[lbl[1:]])
                    functions[-1].labels[index_l].operations.pop(index_op)
                return functions
        elif op.name == 'ret':
            functions[-1].labels[-1].operations.append(copy.deepcopy(op))
            return functions
        elif op.name == 'phi':
            cur_f = functions[-1]
            cur_f.labels[-1].operations.append(Operation(op.name, op.value,
                                        [[op.args[0][0], '%'+get_prev_name(reduce_to_value(op.args[0][1]),
                                         cur_f.ssa_map_lbl)],
                                        [op.args[1][0], '%'+get_prev_name(reduce_to_value(op.args[1][1]),
                                         cur_f.ssa_map_lbl)]]))
            continue
        functions[-1].labels[-1].operations.append(copy.deepcopy(op))


def unroll_llvm(fs, known_funcs, progress):
    functions = []
    progress.emit("start function identification")
    for f in fs:
        for l in f.labels:
            for op in l.operations:
                if op.name == 'br' and op.args is not None:
                    op.value = f.name+'_'+op.value
                    continue
                elif op.name == 'br': continue

                if op.value != '':
                    op.value = f.name+'_'+op.value
                if op.args == [] or op.args is None:
                    continue

                if op.name == 'phi':
                    op.args[0][0] = f.name+'_'+op.args[0][0]
                    op.args[1][0] = f.name+'_'+op.args[1][0]
                else:
                    if not is_constant(op.args[0]):
                        op.args[0] = f.name+'_'+op.args[0]
                    if len(op.args) > 1 and not is_constant(op.args[1]):
                        op.args[1] = f.name+'_'+op.args[1]
    progress.emit("end function identification")

    with open("F:\\STU\\FIIT\\BP\\func_id.txt", "w") as f:
        for func in fs:
            f.write(func.name)
            f.write('\n')
            f.write(str(func.params))
            f.write('\n')
            for label in func.labels:
                f.write('   '+label.name+'\n')
                for op in label.operations:
                    f.write('      '+op.name+': '+op.value+'\n')
                    if op.args is not None: f.write('         '+str(op.args)+'\n')

    progress.emit("start unrolling")
    for f in fs:
        functions.append(Function(f.name, f.params))
        functions[-1].init_ssamap(f.labels)
        functions[-1].init_ssavarmap(f.labels)
        functions[-1].labels.append(Label(set_new_name(f.labels[0].name, functions[-1].ssa_map_lbl)))
        functions = unroll_label(f, functions, f.labels[0])
    progress.emit("end unrolling")

    with open("F:\\STU\\FIIT\\BP\\output_unroll_before_ssa.txt", "w") as f:
        for func in functions:
            f.write(func.name)
            f.write('\n')
            f.write(str(func.params))
            f.write('\n')
            for label in func.labels:
                f.write('   '+label.name+'\n')
                for op in label.operations:
                    f.write('      '+op.name+': '+op.value+'\n')
                    if op.args is not None: f.write('         '+str(op.args)+'\n')

    
    progress.emit("start variable identification")
    for f in functions:
        for l in f.labels:
            for op in l.operations:
                if op.name != 'br' and op.value != '':
                    var = get_prev_name(op.value, f.ssa_map_var)
                    op.value = set_new_name(op.value, f.ssa_map_var)
                    if op.value != var:
                        rename_front_arg(f, var, op.value, l.operations.index(op)+1, f.labels.index(l))
    progress.emit("end variable identification")
    print("*******************************************************************")
    
    with open("F:\\STU\\FIIT\\BP\\output_unroll.txt", "w") as f:
        for func in functions:
            f.write(func.name)
            f.write('\n')
            f.write(str(func.params))
            f.write('\n')
            for label in func.labels:
                f.write('   '+label.name+'\n')
                for op in label.operations:
                    f.write('      '+op.name+': '+op.value+'\n')
                    if op.args is not None: f.write('         '+str(op.args)+'\n')

    return functions


def parse_llvm(filename, progress):
    fs, k_fs = load_llvm(filename, progress)
    fs = unroll_llvm(fs, k_fs, progress)
    return fs

# sss = WorkerSignals()
# functions = parse_llvm("F:\\STU\\FIIT\\BP\\pr.ll", sss.progress)