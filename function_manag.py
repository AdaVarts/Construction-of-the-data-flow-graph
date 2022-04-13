import copy
from addit_methods import is_constant
from classes import Function

from memory_management import rename_front_arg

def get_ret_values(function, progress):
    res = []
    for param in function.params:
        try:
            try:
                ind = function.ssa_map_var[function.name+'_'+param+'.1'] - 1
            except:
                ind = function.ssa_map_var[function.name+'_'+param] - 1
            var = f'{function.name}_{param}.1-{ind}'
            res.append(var)
        except:
            continue
    if len(res) == 0:
        progress.emit(f"Error: no changed value to return was found")
    return res

def merge_in_one(fs, name, addsf, delsf, progress):
    for f in fs:
        if f.name == name:
            start_f = copy.deepcopy(f)
    progress.emit(f"found initial function {name}")
    for addf in addsf:
        for func in fs:
            if addf == func.name:
                add_function = copy.deepcopy(func)
                break
        progress.emit(f"start merging with function {add_function.name}")
        merge_two_funcs(start_f, add_function, progress)
        progress.emit(f"merging with function {add_function.name} completed")

    for delf in delsf:
        for func in fs:
            if delf == func.name:
                del_function = copy.deepcopy(func)
                break
        progress.emit(f"start deleting function {del_function.name} from source")
        # progress.emit(f"Warning: deleting is possible only if functions were not merged! And if function has less than 2 arguments!")
        delete_f(start_f, del_function, progress)
        progress.emit(f"deleting function {del_function.name} completed")

    progress.emit(f"merging completed")
    for param in start_f.params[::-1]:
        if param == '':
            start_f.params.pop(start_f.params.index(param))
    return start_f

def delete_f(dest: Function, source: Function, progress):
    if len(source.params) > 1:
        progress.emit(f"Error: deleting function {source.name} is not possible!")
        return

    for l in dest.labels:
        for op in l.operations[::-1]:
            if op.name == source.name:
                progress.emit(f"found instance of function {source.name}")
                rename_front_arg(dest, op.value, op.args[0], l.operations.index(op)+1, dest.labels.index(l))
                l.operations.pop(l.operations.index(op))
    
    with open("F:\\STU\\FIIT\\BP\\dell_func.txt", "w") as f:
        f.write(dest.name)
        f.write('\n')
        f.write(str(dest.params))
        f.write('\n')
        for label in dest.labels:
            f.write('   '+label.name+'\n')
            for op in label.operations:
                f.write('      '+op.name+': '+op.value+'\n')
                if op.args is not None: f.write('         '+str(op.args)+'\n')

def merge_two_funcs(dest: Function, source: Function, progress):
    if len(source.labels) > 1:
        progress.emit("Error: The targeted function has more than 1 label")
        # LOGGER.error("The targeted function has more than 1 label")
    else:
        substitute(dest, source, 0, 0, 0, progress)



        with open("F:\\STU\\FIIT\\BP\\encrypt.txt", "w") as f:
            f.write(dest.name)
            f.write('\n')
            f.write(str(dest.params))
            f.write('\n')
            for label in dest.labels:
                f.write('   '+label.name+'\n')
                for op in label.operations:
                    f.write('      '+op.name+': '+op.value+'\n')
                    if op.args is not None: f.write('         '+str(op.args)+'\n')

def substitute(dest:Function, source: Function, l_i, op_i, counter_f, progress):
    op = op_i
    while op < len(dest.labels[l_i].operations)-1:
        out = False
        for l in range(l_i, len(dest.labels)):
            for op in range(op_i, len(dest.labels[l].operations)):
                if dest.labels[l].operations[op].name == source.name:
                    src = copy.deepcopy(source)
                    if dest.labels[l].operations[op].args is None or dest.labels[l].operations[op].args == []:
                        continue
                    for arg in dest.labels[l].operations[op].args:
                        for oper_s in src.labels[0].operations:
                            if oper_s.args is None:
                                continue
                            for arg_s in oper_s.args:
                                if not is_constant(arg_s) and src.params[dest.labels[l].operations[op].args.index(arg)] == arg_s.split('_')[1]:
                                    src.labels[0].operations[src.labels[0].operations.index(oper_s)].args[oper_s.args.index(arg_s)] = arg
                    if src.labels[0].operations[-1].name != 'ret':
                        # LOGGER.error("Return operation is not the last in source function")
                        progress.emit("Return operation is not the last in source function")
                    ret_value = src.labels[0].operations[-1].args[0]
                    for op_s in src.labels[0].operations[::-1]:
                        if op_s.value == ret_value:
                            op_s.value = dest.labels[l].operations[op].value
                    src.labels[0].operations.pop()
                    put_func(dest, l, op, src, counter_f, progress)
                    l_i = l
                    op_i = op
                    out = True
                    break
            if out:
                break

def put_func(dest, lbl_i, op_i, src, counter_f, progress):
    dest.labels[lbl_i].operations.pop(op_i)
    for op in src.labels[0].operations:
        if counter_f > 0:
            val = op.value.split('_')
            op.value = val[0]+f'{counter_f}'+'_'+val[1] if val[0] == src.name else op.value
            if op.args != [] and op.args is not None:
                if not is_constant(op.args[0]):
                    arg0_spl = op.args[0].split('_')
                    op.args[0] = arg0_spl[0]+f'{counter_f}_'+arg0_spl[1] if arg0_spl[0] == src.name else op.args[0]
                if len(op.args) > 1 and not is_constant(op.args[1]):
                    arg1_spl = op.args[1].split('_')
                    op.args[1] = arg1_spl[0]+f'{counter_f}_'+arg1_spl[1] if arg1_spl[0] == src.name else op.args[1]
        dest.labels[lbl_i].operations.insert(op_i, op)
        op_i += 1