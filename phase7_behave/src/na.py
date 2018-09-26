
def transform_parameters(func):
    def _work(val):
        # work with string only!
        print(type(val))
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



@transform_parameters
def aa(a):
    print(a)

@transform_parameters
def t_func(a, b, c):
    print("a: " + a)
    print("b: " + b)
    print("c: " + c)

aa(100)
aa(1.5)
aa((1,2,3))
aa([1,2,3])
aa({"x":188, "y":345})
aa("N/A")
aa("test")
aa("['abc'*100]")
t_func("N/A", b="N/A", c="ana")
