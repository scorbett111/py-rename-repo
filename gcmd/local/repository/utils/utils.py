import functools

def execute_option_hooks(options=None):

    def outer_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            local_repository = args[0]
            
            command_options = []
            for option in local_repository.options:
                if option.value is not None:
                    command_options.append(option)


            print(command_options)
                
            return func(*args, **kwargs)
        
        return wrapper

    return outer_wrapper
