from api import compute_this


@compute_this
def func(x):
    for i in range(100000000):
        for j in range(len(x)):
            x[j] += i
    return x


out = func.compute([1,2,3,5,6,76,463,4,75,3,46])
print(out)
