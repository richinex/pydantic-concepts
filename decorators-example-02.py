# Importing necessary modules
import time
import functools
from typing import Callable, Any

# Define two basic decorators
def timer(func: Callable) -> Callable:
    """Measures execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} ran in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

def debug(func: Callable) -> Callable:
    """Prints function name and arguments when called."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {result!r}")
        return result
    return wrapper

# Compose decorators by stacking
@timer
@debug
def slow_add(a: int, b: int) -> int:
    time.sleep(1)
    return a + b

# Usage
result = slow_add(3, 4)
# Output:
# Calling slow_add(3, 4)
# 'slow_add' returned 7
# slow_add ran in 1.0013 seconds



def repeat(times: int) -> Callable:
    """Repeats the function call a specified number of times."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def with_logging(logger: Callable) -> Callable:
    """Logs function calls using the provided logger."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger(f"Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Compose decorators with arguments
@repeat(times=3)
@with_logging(print)
def greet(name: str) -> None:
    print(f"Hello, {name}!")

# Usage
greet("Alice")
# Output:
# Calling greet
# Hello, Alice!
# Hello, Alice!



def singleton(cls: type) -> type:
    """Makes a class a Singleton class."""
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

def log_methods(cls: type) -> type:
    """Adds logging to all methods of a class."""
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, debug(method))
    return cls

# Compose class and function decorators
@singleton
@log_methods
class DatabaseConnection:
    def __init__(self):
        print("Initializing database connection")
    
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"

# Usage
db = DatabaseConnection()
db.query("SELECT * FROM users")
# Output:
# Initializing database connection
# Calling query('SELECT * FROM users')
# 'query' returned 'Executing: SELECT * FROM users'
# Hello, Alice!



def validate_arguments(func: Callable) -> Callable:
    """Validates the number of arguments passed to a method."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if len(args) != func.__code__.co_argcount - 1:
            raise ValueError(f"Expected {func.__code__.co_argcount - 1} arguments, got {len(args)}")
        return func(self, *args, **kwargs)
    return wrapper

def memoize(func: Callable) -> Callable:
    """Caches the results of a method."""
    cache = {}
    @functools.wraps(func)
    def wrapper(self, *args):
        if args in cache:
            return cache[args]
        result = func(self, *args)
        cache[args] = result
        return result
    return wrapper

class MathOperations:
    @memoize
    @validate_arguments
    def fibonacci(self, n: int) -> int:
        if n < 2:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)

# Usage
math = MathOperations()
print(math.fibonacci(100))  # Computes quickly due to memoization
# math.fibonacci(100, 200)  # Raises ValueError due to argument validation
