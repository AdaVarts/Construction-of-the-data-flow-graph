class Function:
    def __init__(self, name, params):
        self.name = name
        self.params = params
        # self.ret_value = ret_value
        self.labels = []
        self.label_map = {}
        self.ssa_map_lbl = {}
        self.ssa_map_var = {}
    
    def init_ssamap(self, source_labels):
        for l in source_labels:
            self.ssa_map_lbl[l.name] = 0
    
    def init_ssavarmap(self, source_labels):
        for l in source_labels:
            for op in l.operations:
                if op.name != 'br' and op.name != 'ret' and op.value != '' \
                   and op.value not in self.ssa_map_var.keys():
                    self.ssa_map_var[op.value] = 0
    
class Operation:
    def __init__(self, name, value=None, args=None):
        self.name = name
        self.value = value
        self.args = args

class Label:
    def __init__(self, name):
        self.name = name
        self.operations = []