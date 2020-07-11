import functools

def execute_option_hooks(*args, **kwargs):

    def outer_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            local_repository = args[0]
            print(local_repository)

            return func(*args, **kwargs)
        return wrapper

    return outer_wrapper
