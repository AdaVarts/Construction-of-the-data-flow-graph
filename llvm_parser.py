class Function:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        # self.ret_value = ret_value
        self.labels = []
        self.label_map = {}
        self.ssa_map = {}
    
class Operation:
    def __init__(self, name, value=None, args=None):
        self.name = name
        self.value = value
        self.args = args

class Label:
    def __init__(self, name):
        self.name = name
        self.operations = []

def get_name(name):
    if '\n' in name:
        name = name.replace('\n', '')
    if ',' in name:
        name = name.replace(',', '')
    if ']' in name:
        name = name.replace(']', '')
    if ' ' in name:
        name = name.replace(' ', '')
    if '[' in name:
        name = name.replace('[', '')
    if '@' in name:
        name = name.replace('@', '')
    if '\"' in name:
        name = name.replace('\"', '')
    return name

def get_args(data):
    args = []
    for word in data:
        if '()' in word:
            return []
        if ',' in word:
            args.append(get_name(word[:-1]))
        elif ')' in word:
            args.append(get_name(word.split(')')[0]))
    return args

def remove_empty(data):
    new_d = [ele for ele in data if ele != '']
    return new_d

def load_llvm(filename):
    functions = []
    known_funcs = []

    lines = []
    with open(filename, "r") as f:
        lines = f.readlines()

    start = False
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

    functions = memory_manag(functions, known_funcs)

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


def is_constant(value):
    if '%' not in value:
        return True
    return False

def br_two(functions, op):
    val = op.value
    num = None
    # slt = False
    # sge = False
    for label in functions[-1].labels[::-1]:
        for oper in label.operations[::-1]:
            if val == oper.value:
                if oper.name == 'icmp':
                    val = oper.args[1]
                    num = oper.args[2]
                    # if oper.args[0] == 'slt':   # !=
                    #     slt = True
                    # elif oper.args[0] == 'sge':   # !=
                    #     sge = True
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


def set_new_name(name, function):
    try:
        function.ssa_map[name] += 1
        return name+str(function.ssa_map[name])
    except Exception:
        function.ssa_map[name] = 0
        return name

def get_current_name(name, function):
    try:
        number = function.ssa_map[name[1:]]
        return name+str(number+1)
    except Exception:
        return name

def add_l2(source, functions, l2):
    branch = None
    for op in l2.operations:
        functions[-1].labels[-1].operations.append(op)
        if op.name == 'br' and op.args is None:
            branch = op.value
            return branch, functions
        elif op.name == 'br':
            functions[-1].labels[-1].operations.append(Operation(op.name, op.value,
                                                                 [get_current_name(arg, functions[-1]) for arg in op.args]))
            branch, functions = unroll_two(source, functions, op)
    return branch, functions

def add_label(source, functions, l1, l2):
    branch = None
    for op in l1.operations:
        functions[-1].labels[-2].operations.append(op)
        if op.name == 'br' and op.args is None:
            branch = op.value
            functions[-1].labels[-2].operations[-1].value = \
                '%' + get_current_name(functions[-1].labels[-2].operations[-1].value[1:], functions[-1])
            br2, functions = add_l2(source, functions, l2)
            if branch == br2:
                return branch, functions
            else:
                pass
                # unroll_label
        elif op.name == 'br':
            functions[-1].labels[-2].operations.append(Operation(op.name, op.value,
                                                                 [get_current_name(arg, functions[-1]) for arg in op.args]))
            branch, functions = unroll_two(source, functions, op)
    return branch, functions

def in_function(function, label):
    for l in function.labels:
        if l.name == label:
            return True
    return False

def unroll_two(source, functions, op):
    # if not in_function(functions[-1], op.args[0]):
    functions[-1].labels.append(Label(set_new_name(op.args[0][1:], functions[-1])))
    # if not in_function(functions[-1], op.args[1]):
    functions[-1].labels.append(Label(set_new_name(op.args[1][1:], functions[-1])))
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
                                                               [get_current_name(arg, functions[-1]) for arg in op.args]))
                    branch, functions = unroll_two(source, functions, op)
                    functions[-1].labels.append(Label(set_new_name(branch[1:], functions[-1])))
                    functions = unroll_label(source, functions, source.label_map[branch[1:]])
                else:
                    index_l = functions[-1].labels.index(functions[-1].labels[-1])
                    index_op = functions[-1].labels[-1].operations.index(functions[-1].labels[-1].operations[-1])
                    functions = unroll_label(source, functions, source.label_map[lbl[1:]])
                    functions[-1].labels[index_l].operations.pop(index_op)
                return functions
        elif op.name == 'ret':
            functions[-1].labels[-1].operations.append(op)
            return functions
        functions[-1].labels[-1].operations.append(op)
    

def unroll_llvm(fs, known_funcs):
    functions = []
    for f in fs:
        functions.append(Function(f.name, f.params))
        functions[-1].labels.append(Label(set_new_name(f.labels[0].name, functions[-1])))
        functions = unroll_label(f, functions, f.labels[0])


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


def is_used_backw(f, val, index_op, index_l):
    for j in range(index_op, -1, -1):
        if f.labels[index_l].operations[j].value == val:
            return True
    for i in range(index_l-1, -1, -1):
        for j in range(len(f.labels[i].operations)-1, -1, -1):
            if f.labels[i].operations[j].value == val:
                return True
    return False

def is_used_args(f, arg, index_op, index_l):
    if '%' not in arg: return True
    for j in range(index_op, len(f.labels[index_l].operations)):
        if f.labels[index_l].operations[j].value == arg:
            return True
    for i in range(index_l+1, len(f.labels)):
        for j in range(0, len(f.labels[i].operations)):
            if f.labels[i].operations[j].value == arg:
                return True
    return False

def is_overwritten(f, val, index_op, index_l):
    for j in range(index_op, len(f.labels[index_l].operations)):
        if f.labels[index_l].operations[j].value == val:
            return True
        elif f.labels[index_l].operations[j].args is not None and val in f.labels[index_l].operations[j].args:
            return False
    for i in range(index_l+1, len(f.labels)):
        for j in range(0, len(f.labels[i].operations)):
            if f.labels[i].operations[j].value == val:
                return True
            elif f.labels[i].operations[j].args is not None and val in f.labels[i].operations[j].args:
                return False
    return False

def is_used_front(f, val, index_op, index_l):
    for j in range(index_op, len(f.labels[index_l].operations)):
        # if f.labels[i].operations[j].args is not None and (val in f.labels[i].operations[j].args or val == f.labels[i].operations[j].value):
        if f.labels[index_l].operations[j].args is not None and val in f.labels[index_l].operations[j].args:
            return True
    for i in range(index_l+1, len(f.labels)):
        for j in range(0, len(f.labels[i].operations)):
            if f.labels[i].operations[j].args is not None and val in f.labels[i].operations[j].args:
                return True
    return False

def rename_backw(f, val, arg, index_op, index_l):
    for j in range(index_op, -1, -1):
        if arg == f.labels[index_l].operations[j].value:
            f.labels[index_l].operations[j].value = val
    for i in range(index_l-1, -1, -1):
        for j in range(len(f.labels[i].operations)-1, -1, -1):
            if arg == f.labels[i].operations[j].value:
                f.labels[i].operations[j].value = val

def is_arr(f, val, index_op, index_l):
    for j in range(index_op, -1, -1):
        if val == f.labels[index_l].operations[j].value and f.labels[index_l].operations[j].name == 'getelementptr':
            return True
    for i in range(index_l-1, -1, -1):
        for j in range(len(f.labels[i].operations)-1, -1, -1):
            if val == f.labels[i].operations[j].value and f.labels[i].operations[j].name == 'getelementptr':
                return True
    return False

def rename_front_arg(f, val, arg, index_op, index_l):
    for j in range(index_op, len(f.labels[index_l].operations)):
        if f.labels[index_l].operations[j].args is not None and val in f.labels[index_l].operations[j].args:
            f.labels[index_l].operations[j].args[f.labels[index_l].operations[j].args.index(val)] = arg
    for i in range(index_l+1, len(f.labels)):
        for j in range(0, len(f.labels[i].operations)):
            if f.labels[i].operations[j].args is not None and val in f.labels[i].operations[j].args:
                f.labels[i].operations[j].args[f.labels[i].operations[j].args.index(val)] = arg

def rename_front_val(f, val, arg, index_op, index_l):
    for j in range(index_op, len(f.labels[index_l].operations)):
        if arg == f.labels[index_l].operations[j].value:
            f.labels[index_l].operations[j].value = val
    for i in range(index_l+1, len(f.labels)):
        for j in range(0, len(f.labels[i].operations)):
            if arg == f.labels[i].operations[j].value:
                f.labels[i].operations[j].value = val

def memory_manag(fs, k_fs):
    val = None
    index = None
    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name in ['printf', 'sprintf', 'free', 'puts']:
                    l.operations.pop(l.operations.index(op))
            # for op in l.operations:
                # elif op.name == 'load':
                #     if not is_used(f, op.value, l, l.operations.index(op), f.labels.index(l)):
                #         print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                #         l.operations.pop(l.operations.index(op))
    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'store':
                    if (not is_used_front(f, op.value, l.operations.index(op)+1, f.labels.index(l)) and
                       is_used_args(f, op.args[0], l.operations.index(op)+1, f.labels.index(l))):
                        rename_backw(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))
                    elif op.args[0] in f.params:
                        rename_front_arg(f, op.value, op.args[0], l.operations.index(op)+1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))
    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'load':
                    rename_front_arg(f, op.value, op.args[0], l.operations.index(op)+1, f.labels.index(l))
                    print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                    l.operations.pop(l.operations.index(op))

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'bitcast':
                    rename_backw(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                    rename_front_val(f, op.value, op.args[0], l.operations.index(op)+1, f.labels.index(l))
                    print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                    l.operations.pop(l.operations.index(op))

    # with open("F:\\STU\\FIIT\\BP\\output_unroll.txt", "w") as f1:
    #     for func in fs:
    #         f1.write(func.name)
    #         f1.write('\n')
    #         f1.write(str(func.params))
    #         f1.write('\n')
    #         for label in func.labels:
    #             f1.write('   '+label.name+'\n')
    #             for op in label.operations:
    #                 f1.write('      '+op.name+': '+op.value+'\n')
    #                 if op.args is not None: f1.write('         '+str(op.args)+'\n')

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'store':
                    if (is_used_backw(f, op.args[0], l.operations.index(op)-1, f.labels.index(l)) and
                       not is_arr(f, op.value, l.operations.index(op)-1, f.labels.index(l))):
                        rename_backw(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))
                    elif is_overwritten(f, op.value, l.operations.index(op)+1, f.labels.index(l)):
                        # rename_backw(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))
    return fs

fs, k_fs = load_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_pr.ll")
# fs = memory_manag(fs, k_fs)
unroll_llvm(fs, k_fs)