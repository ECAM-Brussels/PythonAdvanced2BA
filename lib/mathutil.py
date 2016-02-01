def fact(n):
    if n < 0:
        raise ValueError()
    result = 1
    while n > 0:
        result *= n
        n -= 1
    return result