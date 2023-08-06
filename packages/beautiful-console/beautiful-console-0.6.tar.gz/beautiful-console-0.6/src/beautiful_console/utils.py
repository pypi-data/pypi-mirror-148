def end_point(beautiful_console):
    def wrapper(*args, **kwargs):
        if "get_input" in kwargs:
            if kwargs["get_input"] is True:
                text = input(beautiful_console(*args, **kwargs))
                print("\u001b[0m")
                return text
            else:
                raise AttributeError("\"get_input\" value must be boolean")
        elif "get_input" in args:
            text = input(beautiful_console(*args, **kwargs))
            print("\u001b[0m")
            return text       
        else:
            return beautiful_console(*args, **kwargs)
    return wrapper
