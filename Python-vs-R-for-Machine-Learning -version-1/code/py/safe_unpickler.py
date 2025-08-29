# file: code/py/safe_unpickler.py
# 2018-compatible allow-listing unpickler
import pickle

ALLOWED = {
    ('builtins', 'list'), ('builtins', 'dict'), ('builtins', 'str'),
    ('builtins', 'int'), ('builtins', 'float'), ('builtins', 'tuple')
}

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in ALLOWED:
            mod = __import__(module, fromlist=[name])
            return getattr(mod, name)
        raise pickle.UnpicklingError("blocked: {m}.{n}".format(m=module, n=name))

def safe_load(fp):
    return SafeUnpickler(fp).load()
