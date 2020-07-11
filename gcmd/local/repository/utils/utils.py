import functools

def execute_option_hooks(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        local_repository = args[0]
        
        if local_repository.options:
            print('EEEE')

        return func(*args, **kwargs)

    return wrapper
