
def curried(orig, argc=None):
    if argc is None:
        if isinstance(orig, type):
            argc = orig.__init__.__code__.co_argcount - 1
        else:
            argc = orig.__code__.co_argcount
    def wrapper(*a):
        if len(a) == argc:
            return orig(*a)
        def new_wrapper(*b):
            return orig(*a, *b)
        return curried(new_wrapper, argc - len(a))
    
    func_name = getattr(orig, "__name__", getattr(orig, "__class__").__name__)
    wrapper.__name__ = func_name
    return wrapper

if __name__ == "__main__":
    @curried
    def add3(a, b, c):
        return a + b + c

    @curried
    class ThreeThings:
        def __init__(self, a, b, c):
            self.vals = [a, b, c]
        def __str__(self):
            return f'{self.vals}'

    # All equivalent!
    print(add3(1)(2)(3))
    print(add3(1,2)(3))
    print(add3(1,2,3))

    # All equivalent!
    print(ThreeThings(1,2,3))
    print(ThreeThings(1,2)(3))
    print(ThreeThings(1)(2)(3))