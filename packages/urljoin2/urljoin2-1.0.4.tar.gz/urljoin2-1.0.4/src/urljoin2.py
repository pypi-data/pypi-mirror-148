def urljoin(*args: str) -> str:
    
    """
    Joins arbitrary number of strings to form a url.
    It does not matter if they begin or end with slashes, it takes care of it automatically.
    
    urljoin('foo/', 'bar/', '/baz', '/foobar', '42') ---> 'foo/bar/baz/foobar/42'
    """
    
    if not args:
        return ''
    
    first_arg = args[0]
    
    if not isinstance(first_arg, str):
        raise TypeError(f'Only strings are accepted in the arguments, got: {type(first_arg).__name__}')
    
    res = first_arg
    
    for arg in args[1:]:
        if not isinstance(arg, str):
            raise TypeError(f'Only strings are accepted in the arguments: got {type(arg).__name__}')
            
        if res.endswith('/'):
            if arg.startswith('/'):
                res += arg[1:]
            else:
                res += arg
        else:
            if arg.startswith('/'):
                res += arg
            else:
                res += '/' + arg
    
    return res
