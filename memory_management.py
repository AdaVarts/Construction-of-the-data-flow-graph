from addit_methods import save_into_logs
from classes import Operation

def memory_manag(fs, k_fs):
    val = None
    index = None
    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name in ['printf', 'sprintf', 'free', 'puts']:
                    l.operations.pop(l.operations.index(op))

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'bitcast':
                    rename_backw_val(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                    rename_front_val(f, op.value, op.args[0], l.operations.index(op)+1, f.labels.index(l))
                    print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                    l.operations.pop(l.operations.index(op))

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'trunc' or op.name == 'sext':
                    rename_front_arg(f, op.value, op.args[0], l.operations.index(op)+1, f.labels.index(l))
                    print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                    l.operations.pop(l.operations.index(op))

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'store':
                    if (not is_used_front(f, op.value, l.operations.index(op)+1, f.labels.index(l)) and
                       is_used_args(f, op.args[0], l.operations.index(op)+1, f.labels.index(l))):
                        rename_backw_val(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
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
                    rename_front_val(f, op.args[0], op.value, l.operations.index(op)+1, f.labels.index(l))
                    print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                    l.operations.pop(l.operations.index(op))

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'store':
                    if is_overwritten(f, op.value, l.operations.index(op)+1, f.labels.index(l)):
                        # rename_backw(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))

    save_into_logs(fs, "output_mem_man_before_store.txt")

    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                if op.name == 'store':
                    if (not is_used_front(f, op.args[0], l.operations.index(op)+1, f.labels.index(l)) and
                       is_used_backw(f, op.args[0], l.operations.index(op)-1, f.labels.index(l)) and
                       is_arr(f, op.value, l.operations.index(op)-1, f.labels.index(l)) is False and
                       is_arr(f, op.args[0], l.operations.index(op)-1, f.labels.index(l)) is False):
                        rename_backw_val(f, op.value, op.args[0], l.operations.index(op)-1, f.labels.index(l))
                        print(f.name+'  : '+l.name+'  -  '+op.name+' '+op.value+'  '+str(op.args))
                        l.operations.pop(l.operations.index(op))

    save_into_logs(fs, "output_mem_man_after_store.txt")

    # to change storing the element of array in got element   to   storing into array
    for f in fs:
        for l in f.labels:
            for op in l.operations[::-1]:
                val = is_arr(f, op.value, l.operations.index(op)-1, f.labels.index(l))
                if op.name in ('memcpy', 'memmove', 'store') and val:
                    op.args.append(op.value)
                    l.operations.insert(l.operations.index(op)+1, Operation("store", val, [op.value]))
                    f = store_into_arr_check(f, l, l.operations[l.operations.index(op)+1])

    return fs

def store_into_arr_check(f, l, op):
    new_val = is_arr(f, op.value, l.operations.index(op)-1, f.labels.index(l))
    if op.name in ('memcpy', 'memmove', 'store') and new_val:
        op.args.append(op.value)
        l.operations.insert(l.operations.index(op)+1, Operation("store", new_val, [op.value]))
        f = store_into_arr_check(f, l, l.operations[l.operations.index(op)+1])
    return f

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
    # for i in range(index_l+1, len(f.labels)):
    #     for j in range(0, len(f.labels[i].operations)):
    #         if f.labels[i].operations[j].value == val:
    #             return True
    #         elif f.labels[i].operations[j].args is not None and val in f.labels[i].operations[j].args:
    #             return False
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

def is_arr(f, val, index_op, index_l):
    for j in range(index_op, -1, -1):
        if val == f.labels[index_l].operations[j].value and f.labels[index_l].operations[j].name == 'getelementptr':
            return f.labels[index_l].operations[j].args[0]
    for i in range(index_l-1, -1, -1):
        for j in range(len(f.labels[i].operations)-1, -1, -1):
            if val == f.labels[i].operations[j].value and f.labels[i].operations[j].name == 'getelementptr':
                return f.labels[i].operations[j].args[0]
    return False

def rename_backw_val(f, val, arg, index_op, index_l):
    for j in range(index_op, -1, -1):
        if arg == f.labels[index_l].operations[j].value:
            f.labels[index_l].operations[j].value = val
    for i in range(index_l-1, -1, -1):
        for j in range(len(f.labels[i].operations)-1, -1, -1):
            if arg == f.labels[i].operations[j].value:
                f.labels[i].operations[j].value = val

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
