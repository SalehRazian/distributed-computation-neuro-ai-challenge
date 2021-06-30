from dist_computation import compute_this


@compute_this
def func(x):
    return x*x


out = func.compute(25)
print(out)
