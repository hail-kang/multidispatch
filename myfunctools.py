
def multidispatch(func):
    from functools import get_cache_token, _find_impl, update_wrapper
    import types, weakref
    import typing

    registry = {}
    dispatch_cache = {}
    cache_token = None

    def dispatch(cls):
        nonlocal cache_token
        if cache_token is not None:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token
        try:
            impl = dispatch_cache[cls]
        except KeyError:
            try:
                impl = registry[cls]
            except KeyError:
                impl = _find_impl(cls, registry)
            dispatch_cache[cls] = impl
        return impl

    def register(func):
        nonlocal cache_token
        if isinstance(func, type):
            return lambda f: register(func, f)
        ann = getattr(func, '__annotations__', {})
        if not ann:
            raise TypeError(
                f"Invalid argument to `register()`: {func!r}. "
                f"Use plain `@register` "
                f"on an annotated function."
            )

        from typing import get_type_hints

        type_hints = get_type_hints(func)
        if 'return' in type_hints:
            type_hints.pop('return')
        type_hints_keys = type_hints.keys()
        type_hints_values = type_hints.values()
        for argname, cls in zip(type_hints_keys, type_hints_values):
            if not isinstance(cls, type):
                raise TypeError(
                    f"Invalid annotation for {argname!r}. "
                    f"{cls!r} is not a class."
                )
        registry_key = hash(tuple(type_hints_values))
        registry[registry_key] = func
        if cache_token is None and hasattr(cls, '__abstractmethods__'):
            cache_token = get_cache_token()
        dispatch_cache.clear()
        return func

    def wrapper(*args, **kw):
        if not args:
            raise TypeError(f'{funcname} requires at least '
                            '1 positional argument')

        dispatch_key = hash(tuple(arg.__class__ for arg in args))
        return dispatch(dispatch_key)(*args, **kw)

    funcname = getattr(func, '__name__', 'singledispatch function')
    registry[object] = func
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.registry = types.MappingProxyType(registry)
    wrapper._clear_cache = dispatch_cache.clear
    update_wrapper(wrapper, func)
    return wrapper