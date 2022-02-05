import copy
from addit_methods import is_constant
from classes import Function
import logging

# LOGGER = logging.Logger('function unrollment')

def merge_in_one(fs, name, addsf, dellsf, progress):
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
    progress.emit(f"merging completed")
    return start_f

def merge_two_funcs(dest: Function, source: Function, progress):
    if len(source.labels) > 1:
        progress.emit("Error: The targeted function has more than 1 lable")
        # LOGGER.error("The targeted function has more than 1 lable")
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

def substitute(dest:Function, source: Function, lbl_i, op_i, counter_f, progress):
    for l in range(lbl_i, len(dest.labels)):
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
                put_func(dest, source, l, op, src, counter_f, progress)
                return

def put_func(dest, source, lbl_i, op_i, src, counter_f, progress):
    dest.labels[0].operations.pop(op_i)
    for op in src.labels[0].operations:
        if counter_f > 0:
            val = op.value.split('_')
            op.value = val[0]+f'{counter_f}'+'_'+val[1]
            if op.args != [] and op.args is not None:
                if not is_constant(op.args[0]):
                    op.args[0] = op.args[0].split('_')[0]+f'{counter_f}_'+op.args[0].split('_')[1]
                if len(op.args) > 1 and not is_constant(op.args[1]):
                    op.args[1] = op.args[1].split('_')[0]+f'{counter_f}_'+op.args[1].split('_')[1]
        dest.labels[0].operations.insert(op_i, op)
        op_i += 1
    substitute(dest, source, lbl_i, op_i, counter_f=counter_f+1, progress=progress)