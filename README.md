# multidispatch
파이썬 내장 라이브러리인 functools에는 singledispatch라는 함수 존재함. 이 기능을 확장하여 multidispatch 함수를 만듦.

# 실행환경
python의 내부 라이브러리인 functools를 import하기 때문에 외부 라이브러리에 종속되지 않는다. 다만 python의 functools에 존재하는 get_cache_token, _find_impl, update_wrapper 사용하므로 python 버전에 영향을 받을수도 있다. 해당 프로젝트는 python version 3.9에서 작성되었다.

# 사용방법
[singledispatch와 굉장히 흡사하다.](https://docs.python.org/ko/3/library/functools.html#functools.singledispatch)
[프로젝트내의 example.py를 참고하면 된다.](https://github.com/hail-kang/multidispatch/blob/main/example.py)

# 주의사항
다만 singledispatch와는 달리 register에 타입에 해당하는 인자값을 직접 넣어주는 방법은 사용할 수 없다.
```python
@multidispatch
def fun(arg):
    print("Let me just say,", end=" ")
    print(arg)

# 아래와 같이 사용할 수 없다
@fun.register(complex)
def _(arg):
    print("Better than complicated.", end=" ")
    print(arg.real, arg.imag)

# 아래와 같이 타입힌트를 제공하는 방법으로만 동작한다.
@fun.register
def _(arg: complex):
    print("Better than complicated.", end=" ")
    print(arg.real, arg.imag)
```