import copy
from classes import Function, Operation, Label, WorkerSignals
from memory_management import memory_manag, is_overwritten
from addit_methods import *
# import sys
# sys.setrecursionlimit(3000)

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
            elif 'call' in data and '...' not in line:
                if '=' in data:
                    functions[-1].labels[-1].operations.append(Operation(get_name(data[4].split('(')[0]),
                                                                        value=get_name(data[0]),
                                                                        args=get_args(data)))
                else:
                    func_call_name = get_name(data[2].split('(')[0])
                    func_call_args = get_args(data)
                    if func_call_name in ('free'): continue
                    if func_call_name in ('memcpy', 'memmove'):
                        functions[-1].labels[-1].operations.append(Operation(func_call_name,
                                                                        value=func_call_args[0],
                                                                        args=func_call_args[1:]))
                    else:
                        functions[-1].labels[-1].operations.append(Operation(func_call_name,
                                                                            value = '',
                                                                            args=func_call_args))
            elif 'bitcast' in data or 'inttoptr' in data:
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
                if '[' in word[0] or ('struct' in word[0] and word[2].split(' ')[-1] == '0'):
                        functions[-1].labels[-1].operations.append(Operation('getelementptr',
                                                                            value=get_name(data[0]),
                                                                            args=[get_name(word[1].split(' ')[-1]), get_name(word[3].split(' ')[-1])]
                                                                            ))
                else:
                    functions[-1].labels[-1].operations.append(Operation('getelementptr',
                                                                        value=get_name(data[0]),
                                                                        args=[get_name(word[1].split(' ')[-1]), get_name(word[2].split(' ')[-1])]
                                                                        ))
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
                                                                    args=[get_name(data[2])] if len(data)>2 else ['']))
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
            elif 'switch' in data:
                switch_op = Operation('switch', value=get_name(data[2]), args=[get_name(data[4])])
                switch_args = {}
                for i in range(0, int((len(data)-5)/4)):
                    switch_args[get_name(data[i*4+6])] = get_name(data[i*4+8])
                switch_op.args.append(switch_args)
                functions[-1].labels[-1].operations.append(switch_op)

    progress.emit("end loading")
    progress.emit("start customising")

    save_into_logs(functions, "parsed_llvm.txt")

    functions = memory_manag(functions)
    progress.emit("end memory management")

    save_into_logs(functions, "output_llvm.txt")
    print('-----')
    for func in known_funcs:
        print(func)
    
    return functions


def find_val(functions, op):
    val = op.value
    orig_args = list(op.args[1].keys())
    args = list(op.args[1].keys())
    try:
        for label in functions[-1].labels[::-1]:
            for oper in label.operations[::-1]:
                if val == oper.value:
                    if oper.name == 'load' or oper.name == 'store':
                        val = oper.args[0]
                    elif oper.name == 'add':
                        for i in range(0, len(args)):
                            args[i] = str(int(args[i]) - int(oper.args[1]))
                        val = oper.args[0]
                    elif oper.name == 'sub':
                        for i in range(0, len(args)):
                            args[i] = str(int(args[i]) + int(oper.args[1]))
                        val = oper.args[0]
                    elif oper.name == 'mul':
                        for i in range(0, len(args)):
                            args[i] = str(int(args[i]) / int(oper.args[0]))
                        val = oper.args[1]
                    elif oper.name == 'div':
                        for i in range(0, len(args)):
                            args[i] = str(int(args[i]) * int(oper.args[0]))
                        val = oper.args[1]
                    if is_constant(val):
                        return op.args[1][orig_args[args.index(val)]]
    except:
        return False
    return False

def br_two(functions, op):
    val = op.value
    num = None
    try:
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
                        return op.args[1]
    except:
        return False
    return False

def unroll_label(source, functions, l):
    res = True
    for op in l.operations:
        if op.name == 'br':
            if op.args is None:
                res, functions = unroll_label(source, functions, source.label_map[op.value[1:]])
                return res, functions

            lbl = br_two(functions, op)
            if not lbl:
                return False, functions

            index_l = functions[-1].labels.index(functions[-1].labels[-1])
            index_op = functions[-1].labels[-1].operations.index(functions[-1].labels[-1].operations[-1])
            res, functions = unroll_label(source, functions, source.label_map[lbl[1:]])
            functions[-1].labels[index_l].operations.pop(index_op)
            return res, functions
        elif op.name == 'ret':
            functions[-1].labels[-1].operations.append(copy.deepcopy(op))
            return res, functions
        elif op.name == 'phi':
            cur_f = functions[-1]
            cur_f.labels[-1].operations.append(Operation(op.name, op.value,
                                        [[op.args[0][0], '%'+get_prev_name(reduce_to_value(op.args[0][1]),
                                         cur_f.ssa_map_lbl)],
                                        [op.args[1][0], '%'+get_prev_name(reduce_to_value(op.args[1][1]),
                                         cur_f.ssa_map_lbl)]]))
            continue
        elif op.name == 'switch':
            lbl = find_val(functions, op)
            if not lbl:
                return False, functions

            res, functions = unroll_label(source, functions, source.label_map[lbl[1:]])
            return res, functions
        functions[-1].labels[-1].operations.append(copy.deepcopy(op))

def clear_labels(functions):
    for f in functions:
        for lbl in f.labels[::-1]:
            if len(lbl.operations) == 1 and lbl.operations[0].name == 'br':
                if lbl.operations[0].args and len(lbl.operations[0].args) == 1:
                    f = rename_label(lbl.name, lbl.operations[0].args[0], f)
                    f.labels.pop(f.labels.index(lbl))
                elif not lbl.operations[0].args:
                    f = rename_label(lbl.name, lbl.operations[0].value, f)
                    f.labels.pop(f.labels.index(lbl))
    return functions

def rename_label(old_name, new_name, f):
    for lbl in f.labels:
        if len(lbl.operations) > 0 and lbl.operations[-1].name == 'br':
            if lbl.operations[-1].args:
                for i in range(0, len(lbl.operations[-1].args)):
                    if lbl.operations[-1].args[i] == '%'+old_name:
                        lbl.operations[-1].args[i] = new_name
            elif lbl.operations[-1].value == '%'+old_name:
                lbl.operations[-1].value = new_name
    return f

def unroll_llvm(fs, progress):
    functions = []
    progress.emit("start function identification")
    for f in fs:
        for l in f.labels:
            for op in l.operations:
                if op.name == 'br':
                    if op.args is not None:
                        op.value = f.name+'_'+op.value
                    continue

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
                    if len(op.args) > 2 and not is_constant(op.args[2]):
                        op.args[2] = f.name+'_'+op.args[2]
    progress.emit("end function identification")

    save_into_logs(functions, "func_id.txt")

    progress.emit("start unrolling")
    fs = clear_labels(fs)
    for f in fs:
        functions.append(Function(f.name, f.params))
        functions[-1].init_ssamap(f.labels)
        functions[-1].init_ssavarmap(f.labels)
        functions[-1].labels.append(Label(set_new_name(f.labels[0].name, functions[-1].ssa_map_lbl)))
        try:
            res, functions = unroll_label(f, functions, f.labels[0])
        except:
            progress.emit(f"Function {f.name} is too big, unrolling failed")
            res = False
        if not res:
            functions[-1].labels.clear()
            for lbl in f.labels:
                functions[-1].labels.append(Label(set_new_name(lbl.name, functions[-1].ssa_map_lbl)))
                for op in lbl.operations:
                    functions[-1].labels[-1].operations.append(copy.deepcopy(op))

    progress.emit("end unrolling")

    save_into_logs(functions, "output_unroll_before_ssa.txt")

    
    progress.emit("start variable identification")
    for f in functions:
        for param in f.params:
            if param == '': continue
            if not is_overwritten(f, f.name+'_'+param, 0, 0) and f.name+'_'+param in f.ssa_map_var.keys():
                f.ssa_map_var[f.name+'_'+param] += 1
    for f in functions:
        for l in f.labels:
            for op in l.operations:
                if op.name != 'br' and op.value != '':
                    if op.args is not None:
                        for i in range(0, len(op.args)):
                            if not is_constant(op.args[i]):
                                op.args[i] = get_prev_name(op.args[i], f.ssa_map_var, f)
                    op.value = set_new_name(op.value, f.ssa_map_var)
                elif op.name == 'ret' and len(op.args) > 0 and op.args[0] != '':
                    op.args[0] = get_prev_name(op.args[0], f.ssa_map_var)

    progress.emit("end variable identification")
    print("*******************************************************************")
    
    save_into_logs(functions, "output_unroll.txt")

    return functions


def parse_llvm(filename, progress):
    fs = load_llvm(filename, progress)
    fs = unroll_llvm(fs, progress)
    return fs

if __name__ == "__main__":
    sss = WorkerSignals()
    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_pr_3.ll", sss.progress)
    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_blowfish_3.ll", sss.progress)
    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_aes.ll", sss.progress)
    functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_aes_copy.ll", sss.progress)
    # functions = parse_llvm("F:\\STU\\FIIT\\BP\\llvm_ir_kalyna_4.ll", sss.progress)