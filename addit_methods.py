import os, sys

# Get name without delimiters
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

# Get arguments of a function call
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
    new_d = [item for item in data if item != '']
    return new_d



# if label exists in function
def in_function(function, label):
    for l in function.labels:
        if l.name == label:
            return True
    return False

# Get the name of variable without '%'
def reduce_to_value(name):
    b = name[ : : -1 ][ : : -1 ]
    return b.replace('%', '')

# Set new name based on SSA for a variable/label and store in ssa map
def set_new_name(name, map):
    real_name = get_the_real_name(name)
    map[real_name] +=1
    if map[real_name] == 1:
        return name
    return real_name+'-'+str(map[real_name]-1)

# Get previous name of a variable/label based on the ssa map
def get_prev_name(name, map, f=None):
    real_name = get_the_real_name(name)
    if real_name not in map:
        return real_name
    if map[real_name]-1 == 0 or map[real_name] == 0:
        return real_name
    return real_name+'-'+str(map[real_name]-1)

# Get current name of a label based on the ssa map
def get_current_name(name, function):
    real_name = get_the_real_name(name)
    if function.ssa_map_lbl[real_name] == 0:
        return name
    return real_name+'-'+str(function.ssa_map_lbl[real_name])

# Get current name of a variable based on the ssa map
def get_current_name_var(name, function):
    real_name = get_the_real_name(name)
    if real_name not in function.ssa_map_var:
        return name
    if function.ssa_map_var[real_name] == 0:
        return name
    return real_name+'-'+str(function.ssa_map_var[real_name])

# Get the name without ssa form
def get_the_real_name(name):
    return name.split('-')[0]

def is_constant(value):
    if '%' not in value:
        return True
    return False

def get_name_without_func(name):
    return '%'+name.split('%')[1]


# Save the intermediate form in the .txt file for logs
def save_into_logs(functions, filename):
    if getattr(sys, 'frozen', False):
        directory = os.path.dirname(sys.executable)
    else:
        directory = os.path.dirname(os.path.abspath(__file__))
    directory = directory.replace('\\','/')
    logs_dir = directory+'/logs/'
    is_path = os.path.exists(logs_dir)
    if not is_path:
        os.makedirs(logs_dir)
    file = f"{logs_dir}/{filename}"
    with open(file, "w") as f:
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