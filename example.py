from myfunctools import multidispatch

@multidispatch
def fun(x, y):
    print('default', x, y)

@fun.register
def _(x: int, y: int):
    print('int, int', x, y)

@fun.register
def _(x: str, y: int):
    print('str, int', x, y)

@fun.register
def _(x: str, y: str):
    print('str, str', x, y)


fun(1, 2)
fun('1', 2)
fun('1', '2')