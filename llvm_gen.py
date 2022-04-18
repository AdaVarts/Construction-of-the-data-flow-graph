from llvmlite import ir
import pycparser.c_ast as c_ast


class llvm_Generator(object):
    def __init__(self, printW):
        self.module = ir.Module(name=__file__)
        self.builder = ir.IRBuilder()
        ir.global_context.identified_types = {}
        ir.global_context.scope._useset = {''}

        self.global_vars = {}
        self.defined_types = {}
        self.defined_structs = {}
        self.struct_type_list = {}
        self.defined_functions = {}
        self.cur_function = None
        self.function_args = {}
        self.local_memory = {}
        self.blocks_for_continue = []
        self.blocks_for_break = []
        # self.cur_block = None

        self.printW = printW

        self.types = {
            'char': ir.IntType(8),
            'short': ir.IntType(16),
            'int': ir.IntType(32),
            'long': ir.IntType(64),
            'double': ir.DoubleType(),
            'float': ir.FloatType(),
            'void': ir.VoidType(),
            'i8': ir.IntType(8),
            'i16': ir.IntType(16),
            'i32': ir.IntType(32),
            'i64': ir.IntType(64),
        }

        self.int_types = {
            ir.IntType(8): 8,
            ir.IntType(16): 16,
            ir.IntType(32): 32,
            ir.IntType(64): 64,
            'i8': 8,
            'i16': 16,
            'i32': 32,
            'i64': 64
        }

        self.sizeof = {
            ir.IntType(8): 1,
            ir.IntType(16): 2,
            ir.IntType(32): 4,
            ir.IntType(64): 4,
            ir.DoubleType(): 8,
            ir.FloatType(): 4
        }

    def visit(self, node, key=[0,0]):
        method = 'visit_' + node.__class__.__name__
        return getattr(self, method, self.generic_visit)(node, key)

    def generic_visit(self, node, key=[0,0]):
        if isinstance(node, c_ast.EmptyStatement):
            return
        print("Unknown node: " + node.__class__.__name__)   #!!!
        self.printW.emit("Unknown node: " + node.__class__.__name__)   #!!!

    def visit_FileAST(self, n, key=[0,0]):
        for ext in n.ext:
            self.printW.emit(ext.__class__.__name__)
            print(ext.__class__.__name__)
            if isinstance(ext, c_ast.FuncDef):
                self.visit(ext, key=[0,0])
            elif isinstance(ext, c_ast.Decl):
                self.visit(ext, key=[1,0])
            elif isinstance(ext, c_ast.Typedef):
                self.visit(ext, key=[1,0])


    def visit_Typedef(self, n, key=[0,0]):
        if isinstance(n.type, c_ast.TypeDecl):
            self.visit(n.type)

    def visit_PtrDecl(self, n, key=[0,0]):
        if key[1] != 0:
            return ir.PointerType(self.visit(n.type, key))
        return self.visit(n.type, key=[key[0]+1,0])

    def visit_IdentifierType(self, n, key=[0,0]):
        return self._find_type(n.names[0])
    
    def _find_type(self, n):
        if n in self.types.keys():
            return self.types[n]
        elif n in self.defined_types:
            return self.defined_types[n]
        elif n in self.defined_structs:
            return ir.global_context.get_identified_type('struct.'+n)
        else: return None
    
    def visit_DeclList(self, n, key=[0,0]):
        if n.decls:
            for decl in n.decls:
                self.visit(decl, key=[0,0])
        return 

    def _struct_def(self, n, name):
        if n.decls == None:
            return None
        if n.name is None: n.name = name
        if n.name not in self.defined_structs:
            self.defined_structs[n.name] = [item.name for item in n.decls]
            types = []
            for item in n.decls:
                if item.name not in self.defined_types:
                    if type(item.type) == c_ast.ArrayDecl:
                        if isinstance(item.type.type.type, c_ast.Struct):
                            if not item.type.type.type.name: item.type.type.type.name = item.type.type.declname
                            typ_new_s = self._struct_def(item.type.type.type, item.name)
                            self.defined_types[item.name] = ir.ArrayType(typ_new_s, int(item.type.dim.value))
                        else:
                            arr = self.visit(item.type)
                            self.defined_types[item.name] = arr
                        self.struct_type_list[item.name] = n.decls.index(item)
                        types.append(self.defined_types[item.name])
                    elif type(item.type) == c_ast.PtrDecl:
                        key = self.visit(item.type, key=[0,0])[0]
                        if key == 1:
                            declname = item.type.type.declname
                        elif key == 2:
                            declname = item.type.type.type.declname
                        elif key == 3:
                            declname = item.type.type.type.type.declname
                        self.struct_type_list[declname] = n.decls.index(item)
                        types.append(self.defined_types[declname])
                    else:
                        self.defined_types[item.type.declname] = self._find_type(item.type.type.names[0])
                        self.struct_type_list[item.type.declname] = n.decls.index(item)
                        types.append(self.defined_types[item.type.declname])
            typ = ir.global_context.get_identified_type('struct.'+n.name)
            typ.set_body(*types)
        else:
            if 'struct.'+n.name in ir.global_context.identified_types:
                ir.global_context.identified_types.pop('struct.'+n.name)
                ir.global_context.scope._useset.remove('struct.'+n.name)
            typ = ir.global_context.get_identified_type('struct.'+n.name)
            types = [self._find_type(item) for item in n.decls]
            typ.set_body(*types)
        return typ
    
    def visit_EnumeratorList(self, n, key=[0,0]):
        arr = {}
        types = []
        for value in n.enumerators:
            if value.value == None:
                arr[value.name] = ir.Constant(ir.IntType(32), n.enumerators.index(value))
            else:
                arr[value.name] = value.value
            self.global_vars[value.name] = arr[value.name]
            self.defined_types[value.name] = arr[value.name]
        return arr

    def visit_TypeDecl(self, n, key=[0,0]):
        if key[1] != 0:
            return self.visit(n.type, key)
        if isinstance(n.type, c_ast.Enum):
            enum = self.visit(n.type.values)
            self.defined_structs[n.declname] = [k for k in enum.keys()]
            typ = ir.global_context.get_identified_type('struct.'+n.declname)
            typ.set_body(*enum.values())
            self.defined_types[n.declname] = typ
        elif not isinstance(n.type, c_ast.Struct) and (n.declname not in self.defined_types or self.defined_types[n.declname] is None):
            if key[0] == 0:
                self.defined_types[n.declname] = self._find_type(n.type.names[0])
            elif key[0] == 1:
                self.defined_types[n.declname] = ir.PointerType(self._find_type(n.type.names[0]))
            elif key[0] == 2:
                self.defined_types[n.declname] = ir.PointerType(ir.PointerType(self._find_type(n.type.names[0])))
        elif isinstance(n.type, c_ast.Struct):
            typ = self._struct_def(n.type, n.declname)
            if key[0] == 0:
                self.defined_types[n.declname] = typ
            elif key[0] == 1:
                self.defined_types[n.declname] = ir.PointerType(typ)
            elif key[0] == 2:
                self.defined_types[n.declname] = ir.PointerType(ir.PointerType(typ))
        return key

    def visit_FuncDef(self, n, key=[0,0]):
        self.cur_function = self.visit(n.decl, key=[2,0])
        self.function_args.clear()
        self.local_memory.clear()
        self.blocks_for_continue.clear()
        self.blocks_for_break.clear()

        if n.body:
            self.builder = ir.IRBuilder(self.cur_function.append_basic_block())

            for arg in self.cur_function.args:
                self.function_args[arg.name] = self.builder.alloca(arg.type, name=arg.name)
                self.builder.store(arg, self.function_args[arg.name])

            ret = self.visit(n.body)
            if not ret:
                self.builder.ret_void()

        self.blocks_for_continue.clear()
        self.blocks_for_break.clear()
        self.function_args.clear()
        self.cur_block = None

    def visit_For(self, n, key=[1,0]):
        if n.init:
            self.visit(n.init)
        for_precond = self.cur_function.append_basic_block("for_precond")
        for_loop = self.cur_function.append_basic_block("for_loop")
        for_cond = self.cur_function.append_basic_block("for_cond")
        for_end = self.cur_function.append_basic_block("for_end")
        self.blocks_for_break.append(for_end)
        self.blocks_for_continue.append(for_cond)
        self.builder.branch(for_precond)
        self.builder.position_at_end(for_precond)
        if isinstance(n.next, c_ast.UnaryOp):
            if n.next.op == '--':
                expr = self.visit(n.next.expr, key=[1,0])
                self.builder.sub(expr, ir.Constant(expr.type, 1))
            elif n.next.op == '++':
                expr = self.visit(n.next.expr, key=[1,0])
                self.builder.add(expr, ir.Constant(expr.type, 1))
        cond = self.visit(n.cond, key=[1,0])
        cond = self._correct_cond(cond)
        self.builder.cbranch(cond, for_loop, for_end)
        self.builder.position_at_end(for_loop)
        self.visit(n.stmt)
        self.builder.branch(for_cond)
        self.builder.position_at_end(for_cond)
        i = self.visit(n.next, key=[1,1])
        try:
            for i_i in range(0, len(cond.operands[0].operands)):
                self.builder.store(i[i_i], cond.operands[0].operands[i_i])
        except:
            try:
                self.builder.store(i, cond.operands[0].operands[0])
            except:
                pass
        self.builder.branch(for_precond)
        self.builder.position_at_end(for_end)
        self.blocks_for_continue.pop()
        self.blocks_for_break.pop()
    
    def visit_While(self, n, key=[1,0]):
        while_cond = self.cur_function.append_basic_block("while_cond")
        while_loop = self.cur_function.append_basic_block("while_loop")
        while_end = self.cur_function.append_basic_block("while_end")
        self.blocks_for_break.append(while_end)
        self.blocks_for_continue.append(while_cond)
        self.builder.branch(while_cond)
        self.builder.position_at_end(while_cond)
        cond = self.visit(n.cond, key=[1,0])
        cond = self._correct_cond(cond)
        self.builder.cbranch(cond, while_loop, while_end)
        self.builder.position_at_end(while_loop)
        self.visit(n.stmt)
        self.builder.branch(while_cond)
        self.builder.position_at_end(while_end)
        self.blocks_for_continue.pop()
        self.blocks_for_break.pop()
    
    def visit_DoWhile(self, n, key=[1,0]):
        dowhile_loop = self.cur_function.append_basic_block("dowhile_loop")
        dowhile_cond = self.cur_function.append_basic_block("dowhile_cond")
        dowhile_end = self.cur_function.append_basic_block("dowhile_end")
        self.blocks_for_break.append(dowhile_end)
        self.blocks_for_continue.append(dowhile_cond)
        self.builder.branch(dowhile_loop)
        self.builder.position_at_end(dowhile_loop)
        self.visit(n.stmt)
        self.builder.branch(dowhile_cond)
        self.builder.position_at_end(dowhile_cond)
        cond = self.visit(n.cond, key=[1,0])
        cond = self._correct_cond(cond)
        self.builder.cbranch(cond, dowhile_loop, dowhile_end)
        self.builder.position_at_end(dowhile_end)
        self.blocks_for_continue.pop()
        self.blocks_for_break.pop()
    
    def _correct_cond(self, cond):
        if cond.type is not ir.IntType(1):
            cond = self.builder.icmp_signed('!=', cond, ir.Constant(cond.type, 0))
        return cond
    
    def visit_Break(self, n, key=[0,0]):
        block = self.blocks_for_break[-1]
        self.builder.branch(block)
    
    def visit_Continue(self, n, key=[0,0]):
        block = self.blocks_for_continue[-1]
        self.builder.branch(block)
    
    def visit_Switch(self, n, key=[0,0]):
        if n.stmt.block_items:
            switch_begin = self.cur_function.append_basic_block("switch_begin")
            switch_end = self.cur_function.append_basic_block("switch_end")
            self.builder.branch(switch_begin)
            self.blocks_for_break.append(switch_end)

            default = self.visit(n.stmt.block_items[-1], key=[0,0])
            con_blocks = len(self.blocks_for_continue)
            self.blocks_for_continue.append(default)
            self.builder.position_at_end(switch_begin)

            cond = self.visit(n.cond, key=[1,0])
            switch = self.builder.switch(cond, default)
            for stmt in n.stmt.block_items[::-1][1:]:
                const_val = self.visit(stmt.expr, key=[0,0])
                case_block = self.visit(stmt, key=[0,0])
                switch.add_case(const_val, case_block)
            
            self.builder.position_at_end(switch_end)
            self.blocks_for_break.pop()
            while len(self.blocks_for_continue) > con_blocks:
                self.blocks_for_continue.pop()
    
    def visit_Case(self, n, key=[0,0]):
        switch_case = self.cur_function.append_basic_block()
        self.builder.position_at_end(switch_case)
        ret = False
        if n.stmts:
            for stmt in n.stmts:
                self.visit(stmt, key=[0,0])
                if isinstance(stmt, c_ast.Break) or isinstance(stmt, c_ast.Continue) or isinstance(stmt, c_ast.Return):
                    ret = True
        if not ret:
            block = self.blocks_for_continue[-1]
            self.builder.branch(block)
        self.blocks_for_continue.append(switch_case)
        return switch_case

    def visit_Default(self, n, key=[0,0]):
        switch_default = self.cur_function.append_basic_block("switch_default")
        self.builder.position_at_end(switch_default)
        ret = False
        if n.stmts:
            for stmt in n.stmts:
                self.visit(stmt, key=[0,0])
                if isinstance(stmt, c_ast.Break) or isinstance(stmt, c_ast.Continue) or isinstance(stmt, c_ast.Return):
                    ret = True
        if not ret:
            block = self.blocks_for_break[-1]
            self.builder.branch(block)
        return switch_default

    def visit_Compound(self, n, key=[0,0]):
        ret = False
        if n.block_items:
            for stmt in n.block_items:
                self.visit(stmt, key=[0,0])
                if isinstance(stmt, c_ast.Return):
                    ret = True
        return ret

    def visit_Assignment(self, n, key=[0,0]):
        left = self.visit(n.lvalue, key=[0,0])
        right = self.visit(n.rvalue, key=[1,0])
        if right == 'NULL':
                right = ir.Constant(ir.IntType(32), 0).bitcast(left.type)

        if n.op == '=':
            if right.type != left.type:
                right = self.builder.bitcast(right, left.type.pointee)
            self.builder.store(right, left)
        else:
            operations = {
                '+=': self.builder.add,
                '-=': self.builder.sub,
                '*=': self.builder.mul,
                '/=': self.builder.sdiv,
                '>>=': self.builder.lshr,
                '<<=': self.builder.shl,
                '^=': self.builder.xor,
                '|=': self.builder.or_,
                '&=': self.builder.and_,
                '%=': self.builder.srem
            }
            if n.op in operations: 
                new_left = left
                if left.type != right.type:
                    if isinstance(left.type, ir.PointerType) and isinstance(left.type.pointee, ir.PointerType):
                        value = self.builder.gep(new_left, [right], inbounds=True)
                        if value.type == left.type:
                            value = self.builder.bitcast(value, left.type.pointee)
                        return self.builder.store(value, left)
                    elif isinstance(left.type, ir.PointerType):
                        new_left = self.builder.load(left)
                        if new_left.type != right.type and self._is_int(new_left):
                            new_left = self._trunc_or_sext(new_left, right)
                value = operations[n.op](new_left, right)
                if left.type.pointee != value.type:
                    value = self.builder.bitcast(value, left.type.pointee)
                self.builder.store(value, left)
            else:
                print(f"Unknown assignment operator: {n.op}")
                self.printW.emit(f"Unknown assignment operator: {n.op}")

    def visit_StructRef(self, n, key=[0,0]):
        if n.type == '.' or n.type == '->':
            ind = self.struct_type_list[n.field.name]
            s = self.visit(n.name, [1, 0, ind])
            v_type = self.defined_types[n.field.name]
            if not isinstance(n.name, c_ast.ArrayRef):
                value = self.builder.gep(s, [ir.Constant(ir.IntType(32), 0),
                                                  ir.Constant(ir.IntType(32), ind)], inbounds=True)
            else:
                value = s
            if key[0] == 0: 
                return self.builder.bitcast(value, v_type.as_pointer())
            elif key[0] == 1:
                return self.builder.bitcast(value, v_type)
    
    def visit_Typename(self, n, key=[0,0]):
        return self.visit(n.type, key)

    def visit_BinaryOp(self, n, key=[0,0]):
        left = self.visit(n.left, key)
        right = self.visit(n.right, key=[1,0])

        operations = {
            '+': self.builder.add,
            '-': self.builder.sub,
            '*': self.builder.mul,
            '/': self.builder.sdiv,
            '&&': self.builder.and_,
            '||': self.builder.or_,
            '>>': self.builder.lshr,
            '<<': self.builder.shl,
            '^': self.builder.xor,
            '|': self.builder.or_,
            '&': self.builder.and_,
            '%': self.builder.srem
        }
        comparison_op = {'<', '<=', '>=', '>', '==', '!='}
        bit_op = {'>>', '<<', '^', '|', '&'}

        if right == 'NULL':
            right = ir.Constant(ir.IntType(32), 0).bitcast(left.type)
        if left == 'NULL':
            left = ir.Constant(ir.IntType(32), 0).bitcast(right.type)
        
        if n.op == '+' or n.op == '-':
            if left.type != right.type:
                if isinstance(left.type, ir.PointerType):
                    value = self.builder.gep(left, [right], inbounds=True)
                    return value
                elif self._is_int(left):
                    right = self._trunc_or_sext(right, left)
            return operations[n.op](left, right)
        elif n.op in {'*', '/', '%'}:
            if left.type != right.type:
                if isinstance(left.type, ir.PointerType):
                    left = self.builder.load(left)
                elif self._is_int(left):
                    right = self._trunc_or_sext(right, left)
            return operations[n.op](left, right)
        elif n.op in {'&&', '||'}:
            left = self.builder.icmp_signed('!=', left, ir.Constant(left.type, 0))
            right = self.builder.icmp_signed('!=', right, ir.Constant(right.type, 0))
            return operations[n.op](left, right)
        elif n.op in comparison_op:
            # if left.type != right.type and self._is_int(left):
            #     left = self._trunc_or_sext(right, left)
            return self.builder.icmp_signed(n.op, left, right)
        elif n.op in bit_op:
            if left.type != right.type and self._is_int(left):
                right = self._trunc_or_sext(right, left)
            return operations[n.op](left, right)
        else:
            print(f"Unknown binary operator: {n.op}")
            self.printW.emit(f"Unknown binary operator: {n.op}")

    def visit_Cast(self, n, key=[0,0]):
        value = self.visit(n.expr, [1,0])
        to_type = self.visit(n.to_type, key=[0,1])
        if value.type != to_type:
            if self._is_int(value) and self._is_int(ir.Constant(to_type, 0)):
                return self._trunc_or_sext(value, ir.Constant(to_type, 0))
            else:
                return self.builder.bitcast(value, to_type)
        else:
            return value

    def visit_TernaryOp(self, n, key=[1,0]):
        cond = self.visit(n.cond, key=[1,0])
        with self.builder.if_else(cond) as (then, otherwise):
            with then:
                iftrue_v = self.visit(n.iftrue, key=[1,0])
                ifblock = self.builder.block
            with otherwise:
                iffalse_v = self.visit(n.iffalse, key=[1,0])
                elblock = self.builder.block
        ret_value = self.builder.phi(iftrue_v.type)
        ret_value.add_incoming(iftrue_v, ifblock)
        ret_value.add_incoming(iffalse_v, elblock)
        return ret_value

    def visit_UnaryOp(self, n, key=[1,0]):
        expr = self.visit(n.expr, key)
        if n.op in ('p++', '++'):
            return self.builder.add(expr, ir.Constant(expr.type, 1))
        elif n.op in ('p--', '--'):
            return self.builder.sub(expr, ir.Constant(expr.type, 1))
        elif n.op == '-':
            return self.builder.neg(expr)
        elif n.op == 'sizeof':
            expr = self.visit(n.expr, key=[key[0], 1])
            expr_type = self.types[expr.intrinsic_name]
            return ir.Constant(expr_type, self.sizeof[expr_type])
        elif n.op == '&':
            return expr
        elif n.op == '*':
            return expr
        elif n.op == '!':
            return self.builder.not_(expr)
        elif n.op == '~':
            return self.builder.not_(expr)
        else:
            print(f"Unknown unary operator: {n.op}")
            self.printW.emit(f"Unknown unary operator: {n.op}")

    def visit_ArrayRef(self, n, key=[0,0]):
        arr = self.visit(n.name)
        index = self.visit(n.subscript, [1,0])
        if isinstance(index.type, ir.types.PointerType):
            index = self.builder.bitcast(index, index.type.pointee)
        new_arr = self.builder.load(arr) if arr.type.pointee.is_pointer else arr
        try:
            ind = ir.Constant(ir.IntType(32), key[2])
            item = self.builder.gep(new_arr, [index, ind], inbounds=True)
            key = [key[0], key[1]]
        except:
            if isinstance(new_arr.type.pointee, ir.types.ArrayType):
                item = self.builder.gep(new_arr, [ir.Constant(ir.IntType(32), 0), index], inbounds=True)
            else:
                item = self.builder.gep(new_arr, [index], inbounds=True)
        if key[0] == 0:
            return item
        elif key[0] == 1:
            try:
                item.type = ir.PointerType(item.type.pointee.element)
                return self.builder.load(item)
            except Exception:
                return self.builder.load(item)

    def visit_If(self, n, key=[0,0]):
        cond = self.visit(n.cond, key=[1,0])
        cond = self._correct_cond(cond)
        if n.iffalse:
            with self.builder.if_else(cond) as (then, otherwise):
                with then:
                    self.visit(n.iftrue, key=[1,0])
                with otherwise:
                    self.visit(n.iffalse, key=[1,0])
        else:
            with self.builder.if_then(cond):
                self.visit(n.iftrue)

    def visit_Decl(self, n, key=[0,0]):
        if n.init:
            if key[0] == 0:
                declaration = self._create_type(n, key)
                variable = self.visit(n.init, key=[1,0])
                if variable.type != self.local_memory[n.name]:
                    variable = self.builder.bitcast(variable, self.local_memory[n.name].type.pointee)
                self.builder.store(variable, self.local_memory[n.name])
            elif key[0] == 1:
                variable = self.visit(n.init, key=[1,0])
                self.global_vars[n.name] = ir.GlobalVariable(self.module, variable.type, name=n.name)
                self.global_vars[n.name].initializer = variable
        else:
            declaration = self._create_type(n, key)

        if key[0] == 2:
            return declaration

    def visit_FuncCall(self, n, key=[0,0]):
        if n.name.name in self.defined_functions.keys():
            function = self.defined_functions[n.name.name]

            if n.args is None: 
                args = []
            else: 
                args = self.visit(n.args, key=[1,0])
        else:
            function, args = self._add_function(n)

        for i in range(0, len(function.args)):
            if function.args[i].type != args[i].type:
                args[i] = self._cast(args[i], function.args[i])
        
        return self.builder.call(function, args)

    def visit_Return(self, n, key=[0,0]):
        if n.expr:
            ret = self.visit(n.expr, key=[1,0])
            self.builder.ret(ret)
        else:
            self.builder.ret_void()
    
    def _cast(self, arg, to_arg):
        try:
            if arg.type.pointee == to_arg.type:
                arg = self.builder.load(arg)
            else: raise ValueError()
        except:
            try:
                if arg.type == to_arg.type.pointee:
                    arg = self.builder.inttoptr(arg, to_arg.type)
                else: raise ValueError()
            except:
                try:
                    arg = self._trunc_or_sext(arg, to_arg)
                except:
                    arg = self.builder.bitcast(arg, to_arg.type)
        return arg

    def _create_type(self, n, key=[0,0], modifiers=[]):
        if type(n) == c_ast.IdentifierType:
            value = self._find_type(n.names[0])
            decl = modifiers.pop(0)
            name = decl.name
            for m in modifiers:
                if type(m) == c_ast.ArrayDecl:
                    if decl.init:
                        arg = len(decl.init.exprs)
                    elif not m.dim:
                        arg = 256
                    else:
                        arg = int(m.dim.value)
                    value = ir.ArrayType(value, arg)
                    if key[0] == 1:
                        self.global_vars[name] = ir.GlobalVariable(self.module, value, name=name)
                        self.global_vars[name].initializer = ir.Constant(value, [ir.Constant(self._find_type(x.type), x.value) for x in decl.init.exprs])
                    elif type(m.type) == c_ast.ArrayDecl:
                        continue
                    elif key[0] == 0:
                        if name not in self.local_memory.keys():
                            self.local_memory[name] = self.builder.alloca(value, name=name)
                elif type(m) == c_ast.PtrDecl:
                    if isinstance(value, ir.VoidType):
                        value = ir.PointerType(ir.IntType(32))
                    value = ir.PointerType(value)
                elif type(m) == c_ast.FuncDecl:
                    paramtypes = []
                    if m.args:
                        for param in m.args.params:
                            paramtypes.append(self._create_type(param, key=[2,0]))
                    value = ir.FunctionType(value, paramtypes)

                if key[0] == 0:
                    if name not in self.local_memory.keys():
                        self.local_memory[name] = self.builder.alloca(value, name=name)
                        self.builder.store(ir.Constant(value, 0), self.local_memory[name])
                elif key[0] == 2:
                    if len(modifiers) > 0 and type(modifiers[0]) == c_ast.FuncDecl:
                        function = ir.Function(self.module, value, name=name)
                        if modifiers[0].args is not None:
                            for j in range(0, len(modifiers[0].args.params)):
                                function.args[j].name = modifiers[0].args.params[j].name
                        self.defined_functions[name] = function
                        return function
                    return value

        elif type(n) in (c_ast.ArrayDecl, c_ast.FuncDecl, c_ast.TypeDecl, c_ast.PtrDecl, c_ast.Decl):
            return self._create_type(n.type, key, modifiers+[n])

    def visit_InitList(self, n, key=[0,0]):
        new_array = []
        for item in n.exprs:
            value = self.visit(item)
            try:
                if item.type == 'string':
                    continue
                new_array.append(value)
            except:
                new_array.append(value)
        if new_array != []:
            return ir.Constant.literal_array(new_array)
        return value

    def visit_Constant(self, n, key=0):
        try:
            if n.type == 'char':
                value = n.value[1:-1].replace('\\n', '\n')
                return ir.Constant(ir.IntType(8), ord(value))
            elif n.type == 'string':
                value = n.value[1:-1].encode('utf8', 'ignore')
                return ir.Constant(ir.ArrayType(ir.IntType(8), len(value)), bytearray(value))
            elif 'long' in n.type:
                return ir.Constant(ir.IntType(64), n.value)
            else:
                return ir.Constant(self.types[n.type], n.value)
        except Exception:
            print(f"Unknown constant type: {n.type}")
            self.printW.emit(f"Unknown constant type: {n.type}")

    def visit_ExprList(self, n, key=[0,0]):
        return [self.visit(item, key) for item in n.exprs]

    def _get_val_or_pointer(self, name, storage, key):
        if key[0] == 0:
            return storage[name]
        elif key[0] == 1:
            return self.builder.load(storage[name])

    def visit_ID(self, n, key=0): 
        if n.name in self.function_args:
            return self._get_val_or_pointer(n.name, self.function_args, key)
        elif n.name in self.local_memory:
            return self._get_val_or_pointer(n.name, self.local_memory, key)
        elif n.name in self.global_vars:
            if key[0] == 0 or key[0] == 1:
                return self.global_vars[n.name]
        else:
            print(f"Unknown variable: {n.name}")
            self.printW.emit(f"Unknown variable: {n.name}")
            return 'NULL'

    def _intrinsic_dec_function(self, name, func_type):
        return self.module.declare_intrinsic(name, (), func_type)

    def _int_type(self, n):
        return self.int_types[n.type]

    def _is_int(self, n):
        if n.type in self.int_types.keys():
            return True
        return False

    def _trunc_or_sext(self, right, left):
        if self._int_type(left) > self._int_type(right):
            return self.builder.sext(right, left.type)
        elif self._int_type(left) < self._int_type(right):
            return self.builder.trunc(right, left.type)

    def _add_function(self, n):
        function_names_not_needed = {"sprintf", "fprintf", "printf", "puts", "gets", "perror"}
        func_type = None
        if n.name.name in ("malloc", "calloc"):
            func_type = ir.FunctionType(ir.IntType(8).as_pointer(), [])
        elif n.name.name in function_names_not_needed:
            func_type = ir.FunctionType(ir.IntType(32), [])
        elif n.name.name == "free":
            func_type = ir.FunctionType(ir.VoidType(), [])
        elif n.name.name in ("memcpy", "memmove"):
            func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32).as_pointer(), ir.IntType(32).as_pointer(), ir.IntType(32)])
        elif n.name.name == "memset":
            func_type = ir.FunctionType(ir.VoidType(), [ir.IntType(32).as_pointer(), ir.IntType(8), ir.IntType(32)])
        elif n.name.name == "memcmp":
            func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32).as_pointer(), ir.IntType(32).as_pointer(), ir.IntType(32)])
        elif n.name.name == "strlen":
            func_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32).as_pointer()])

        if func_type == None:
            print(f"Unknown function: {n.name.name}")
            self.printW.emit(f"Unknown function: {n.name.name}")
        else:
            args = []
            if isinstance(n.args, c_ast.ExprList):
                for expr in n.args.exprs:
                    if isinstance(expr, c_ast.FuncCall):
                        args.append(self.visit(expr))
                    elif n.name.name in ( "memcpy", "memmove", "memset", "memcmp", "strlen"):
                        args.append(self.visit(expr))
            return self._intrinsic_dec_function(n.name.name, func_type), args    

    def visit_ArrayDecl(self, n, key=[0,0]):
        element = None
        if not isinstance(n.type, c_ast.TypeDecl):
            element = self.visit(n.type)
        if element:
            return ir.ArrayType(element, int(n.dim.value))
        arr = ir.ArrayType(self._find_type(n.type.type.names[0]), int(n.dim.value))
        return arr