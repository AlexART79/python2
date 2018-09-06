"""Returns N-th Fibonacci number"""


def fib(n):
    assert n > 0

    if n == 1: return 0
    if n == 2: return 1

    a = 0
    b = 1
    for i in range(2, n):
        a, b = b, a + b
    return b


"""Returns list of N Fibonacci numbers"""


def fibon(n):
    assert n >= 0

    if n == 0: return []
    if n == 1: return [0]

    res = [0, 1]
    for i in range(2, n):
        res.append(res[-2] + res[-1])
    return res


if __name__ == "__main__":
    print(fib(1))
    print(fib(2))
    print(fib(10))
    print(fibon(0))
    print(fibon(1))
    print(fibon(10))
