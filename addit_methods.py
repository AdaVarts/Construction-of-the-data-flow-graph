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




def in_function(function, label):
    for l in function.labels:
        if l.name == label:
            return True
    return False

def reduce_to_value(name):
    b = name[ : : -1 ][ : : -1 ]
    return b.replace('%', '')

def set_new_name(name, map):
    map[get_the_real_name(name)] +=1
    if map[get_the_real_name(name)] == 1:
        return name
    else:
        return get_the_real_name(name)+'-'+str(map[get_the_real_name(name)]-1)

def get_prev_name(name, map):
    if map[get_the_real_name(name)]-1 == 0:
        return get_the_real_name(name)
    return get_the_real_name(name)+'-'+str(map[get_the_real_name(name)]-1)

def get_current_name(name, function):
    if function.ssa_map_lbl[get_the_real_name(name)] == 0:
        return name
    else:
        return get_the_real_name(name)+'-'+str(function.ssa_map_lbl[get_the_real_name(name)])

def get_the_real_name(name):
    return name.split('-')[0]

def is_constant(value):
    if '%' not in value:
        return True
    return False
