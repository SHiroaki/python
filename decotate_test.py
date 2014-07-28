#/opt/python3.4

__author__ = 'hiroakisuzuki'

def decorate(func):
    print("in decorate function decorating", func.__name__)
    def wrapper_func(*args):
        print("Executing", func.__name__)
        return func(*args)
    return wrapper_func

if __name__ == "__main__":
    @decorate
    def myfunc(parameter):
        print(parameter)

    myfunc("hello")