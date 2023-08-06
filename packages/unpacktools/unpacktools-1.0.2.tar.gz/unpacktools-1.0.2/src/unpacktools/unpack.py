import inspect
class unpack:
    def __init__(self,iterator):
        def handle_iter(iterator):
            new_iter = []
            for item in iterator:
                if type(item) == type(unpack([])):
                    new_iter.extend(i for i in item.iterator)
                elif hasattr(item, "__iter__") and type(item)!= type(str()):
                    new_iter.append(handle_iter(item))
                else:
                    new_iter.append(item)
            return new_iter
        self.iterator = handle_iter(iterator)
        
    def __repr__(self):
        return f"unpack({self.iterator})"

def func_handler(func):
    func_info = str(inspect.getfullargspec(func))[12:-1]
    def new_func(*args) -> "Original Info: "+ func_info: 
        nonlocal func
        def arg_resolver(arg_list):
            handled_arg_list = []
            for i in arg_list:
                if type(i) == type( unpack([]) ):
                    handled_arg_list.extend( i.iterator )
                elif hasattr(i,"__iter__") and type(i) != type(str()):
                    handled_arg_list.append(arg_resolver(i))
                else:
                    handled_arg_list.append(i)
            return handled_arg_list
        return func(*arg_resolver(args))
    return new_func

def multi_func_handler(*funcs, rt_type = dict ):
    new_funcs = {}
    for func in funcs:
        new_funcs[func.__name__] = func_handler(func)
    return new_funcs if rt_type == dict else rt_type(new_funcs.values())

def class_handler(cls):
    class_methods = {}
    for attr in dir(cls):
        if type(getattr(cls, attr)) == type(func_handler):
            class_methods[attr] = getattr(cls,attr)
    all_ = [method for method in class_methods.values()]
    for method in all_:
        class_methods.update({method.__name__:func_handler(method)})
    class_methods_new = {}
    for i in class_methods.keys():
        class_methods_new[i] = class_methods[i]
    for method_name in class_methods_new.keys():
        setattr(cls,method_name,class_methods_new[method_name])
    return cls

def multi_class_handler(*classes, rt_type = dict):
    new_classes = {}
    for cls in classes:
        new_classes[cls.__name__] = class_handler(cls)
    return new_classes if rt_type == dict else rt_type(new_classes.values())
        
def scope_handler(scope, funcs = True, classes = True, dunders = False)->"Returns a dict. Handles all functions exist in the given scope. Usage: globals().update( scope_handler(globals()) )":
    new_scope = scope.copy()
    for i in scope.keys():
        if (not dunders or not i.startswith("_")) and i not in ("unpack", "func_handler","multi_func_handler",
                                                                "class_handler","multi_class_handler","scope_handler"):
            if classes and type(scope[i]) == type(unpack):
                new_scope.update(multi_class_handler(scope[i]))
            elif funcs and hasattr(scope[i],"__call__"):
                new_scope.update(multi_func_handler(scope[i]))

    return new_scope
