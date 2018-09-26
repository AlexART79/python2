
# converts "N/A" values to empty strings
# converts "[ ... ]" values to generated contents
def transform_parameters(func):
    def _work(val):
        # work with string only!
        if type(val) is not str:
            return val

        res = "" if val == "N/A" else val
        res = eval(res) if res.startswith('[') and res.endswith(']') else res
        return res

    def wrapper(*args, **kwards):
        # transform args and kwards
        aa = [_work(a) for a in args]
        kk = {k: _work(v) for k, v in kwards.items()}

        # pass them to the wrapped function
        func(*aa, **kk)

    return wrapper
