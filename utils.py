from functools import wraps


def info_dec(func):
    """ Декоратор, для отображения имени обернутой функции в консоль """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} was called.")
        return func(*args, **kwargs)

    return wrapper


def change_dec(last_arg_change=1):
    """ Декоратор, для изменения последнего аргумента, переданного в функцию """
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            *el, last = args
            last *= last_arg_change
            args = *el, last
            return func(*args, **kwargs)

        return wrapper

    return dec
