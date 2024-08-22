# Importing necessary modules (assumed to be defined elsewhere)
# import time
# import functools
# from typing import Callable, Any


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


# Define a metaclass that adds logging to all methods of a class
class LogMethodCalls(type):
    """A metaclass that adds logging to all methods of a class."""
    
    # __new__ is called when a new class is being created
    def __new__(cls, name, bases, attrs):
        # cls: The metaclass itself (LogMethodCalls)
        # name: The name of the class being created
        # bases: The base classes of the class being created
        # attrs: A dictionary of attributes (including methods) of the class being created
        
        # Iterate through all attributes of the class being created
        for attr_name, attr_value in attrs.items():
            # If the attribute is callable (i.e., a method)
            if callable(attr_value):
                # Wrap the method with the debug decorator
                attrs[attr_name] = debug(attr_value)
        
        # Call the parent class's __new__ method to create the class
        # with the modified attributes
        return super().__new__(cls, name, bases, attrs)

# Define a singleton decorator (assumed to be defined elsewhere)
# def singleton(cls: type) -> type:
#     ...

# Define the DatabaseConnection class using the LogMethodCalls metaclass
# and the singleton decorator
@singleton
class DatabaseConnection(metaclass=LogMethodCalls):
    # Constructor method
    def __init__(self):
        print("Initializing database connection")
    
    # Query method
    def query(self, sql: str) -> str:
        return f"Executing: {sql}"

# Usage of the DatabaseConnection class
db = DatabaseConnection()  # Creates a singleton instance of DatabaseConnection
                           # The __init__ method is called here

# Call the query method
db.query("SELECT * FROM users")

# Expected output:
# Initializing database connection  (from __init__ method)
# Calling query('SELECT * FROM users')  (added by debug decorator via metaclass)
# 'query' returned 'Executing: SELECT * FROM users'  (added by debug decorator)

# Explanation of the output:
# 1. "Initializing database connection" is printed when the DatabaseConnection
#    instance is created.
# 2. "Calling query('SELECT * FROM users')" is printed by the debug decorator,
#    which was added to the query method by the LogMethodCalls metaclass.
# 3. "'query' returned 'Executing: SELECT * FROM users'" is also printed by
#    the debug decorator, showing the return value of the query method.

# This example demonstrates how a metaclass (LogMethodCalls) can be used to
# automatically modify all methods of a class (adding logging via the debug
# decorator) without explicitly decorating each method. It also shows how
# multiple class decorators (@singleton) can be combined with a metaclass.



###################################################################################

# Importing necessary modules
import time  # For measuring execution time
import functools  # For the @functools.wraps decorator
from typing import Callable, Any  # For type hinting

# Define two basic decorators

def timer(func: Callable) -> Callable:
    """Measures execution time of a function."""
    @functools.wraps(func)  # Preserves metadata of the original function
    def wrapper(*args, **kwargs):
        # *args and **kwargs allow the wrapper to accept any arguments
        start_time = time.time()  # Record start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record end time
        # Print execution time
        print(f"{func.__name__} ran in {end_time - start_time:.4f} seconds")
        return result  # Return the result of the original function
    return wrapper  # Return the wrapper function

def debug(func: Callable) -> Callable:
    """Prints function name and arguments when called."""
    @functools.wraps(func)  # Preserves metadata of the original function
    def wrapper(*args, **kwargs):
        # Create string representations of arguments
        args_repr = [repr(a) for a in args]  # Positional arguments
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # Keyword arguments
        signature = ", ".join(args_repr + kwargs_repr)  # Join all arguments
        # Print function call information
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)  # Call the original function
        # Print return value
        print(f"{func.__name__!r} returned {result!r}")
        return result  # Return the result of the original function
    return wrapper  # Return the wrapper function

# Compose decorators by stacking
@timer  # Applied second (outer decorator)
@debug  # Applied first (inner decorator)
def slow_add(a: int, b: int) -> int:
    """Adds two numbers with a delay."""
    time.sleep(1)  # Simulate a slow operation
    return a + b

# Usage
result = slow_add(3, 4)

# Explanation of the output:
# 1. "Calling slow_add(3, 4)" - From the debug decorator
# 2. "'slow_add' returned 7" - From the debug decorator
# 3. "slow_add ran in 1.0013 seconds" - From the timer decorator

# Note on decorator stacking order:
# The @debug decorator is applied first (closer to the function definition),
# so its wrapper is called first. Then the @timer decorator's wrapper is called.
# This is why we see the debug output before the timer output.

####################################################################################
# Importing necessary modules (assumed to be imported)
# import functools
# from typing import Callable

def repeat(times: int) -> Callable:
    """
    A decorator factory that creates a decorator to repeat a function call.
    
    Args:
        times (int): The number of times to repeat the function call.
    
    Returns:
        Callable: A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        """
        The actual decorator that wraps the function.
        
        Args:
            func (Callable): The function to be decorated.
        
        Returns:
            Callable: The wrapped function.
        """
        @functools.wraps(func)  # Preserves metadata of the original function
        def wrapper(*args, **kwargs):
            """
            The wrapper function that repeats the function call.
            
            Args:
                *args: Positional arguments to pass to the function.
                **kwargs: Keyword arguments to pass to the function.
            
            Returns:
                The result of the last function call.
            """
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

def with_logging(logger: Callable) -> Callable:
    """
    A decorator factory that creates a decorator to log function calls.
    
    Args:
        logger (Callable): A function to use for logging.
    
    Returns:
        Callable: A decorator function.
    """
    def decorator(func: Callable) -> Callable:
        """
        The actual decorator that wraps the function.
        
        Args:
            func (Callable): The function to be decorated.
        
        Returns:
            Callable: The wrapped function.
        """
        @functools.wraps(func)  # Preserves metadata of the original function
        def wrapper(*args, **kwargs):
            """
            The wrapper function that logs the function call.
            
            Args:
                *args: Positional arguments to pass to the function.
                **kwargs: Keyword arguments to pass to the function.
            
            Returns:
                The result of the function call.
            """
            logger(f"Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Compose decorators with arguments
@repeat(times=3)  # Applied second (outer decorator)
@with_logging(print)  # Applied first (inner decorator)
def greet(name: str) -> None:
    """Greets a person by name."""
    print(f"Hello, {name}!")

# Usage
greet("Alice")

# Explanation of the output:
# 1. "Calling greet" - Printed once by the with_logging decorator
# 2. "Hello, Alice!" - Printed three times due to the repeat decorator
# 3. "Hello, Alice!"
# 4. "Hello, Alice!"

# Note on decorator execution order:
# 1. @with_logging(print) is applied first, so it logs "Calling greet" once.
# 2. @repeat(times=3) is applied second, so it repeats the entire decorated
#    function (including the logging) three times.
# 3. However, due to how with_logging is implemented, it only logs once
#    before calling the original function, which is then repeated.

# This example demonstrates how to create and compose decorators that take
# arguments. The repeat decorator shows how to create a decorator that
# modifies the behavior of a function, while the with_logging decorator
# shows how to add behavior before executing the function.


###############################################################################
# Importing necessary modules (assumed to be imported)
# import functools
# from typing import Callable

def validate_arguments(func: Callable) -> Callable:
    """
    A decorator that validates the number of arguments passed to a method.
    
    Args:
        func (Callable): The method to be decorated.
    
    Returns:
        Callable: The wrapped method with argument validation.
    """
    @functools.wraps(func)  # Preserves metadata of the original function
    def wrapper(self, *args, **kwargs):
        # self is the instance of the class, *args are positional arguments
        
        # func.__code__.co_argcount gives the total number of arguments
        # We subtract 1 to account for 'self'
        expected_args = func.__code__.co_argcount - 1
        
        if len(args) != expected_args:
            # Raise an error if the number of arguments doesn't match
            raise ValueError(f"Expected {expected_args} arguments, got {len(args)}")
        
        # If validation passes, call the original function
        return func(self, *args, **kwargs)
    
    return wrapper

def memoize(func: Callable) -> Callable:
    """
    A decorator that caches the results of a method.
    
    Args:
        func (Callable): The method to be memoized.
    
    Returns:
        Callable: The wrapped method with memoization.
    """
    cache = {}  # Dictionary to store cached results
    
    @functools.wraps(func)  # Preserves metadata of the original function
    def wrapper(self, *args):
        if args in cache:
            # If result is cached, return it immediately
            return cache[args]
        
        # If not cached, compute the result
        result = func(self, *args)
        
        # Store the result in the cache
        cache[args] = result
        
        return result
    
    return wrapper

class MathOperations:
    @memoize  # Applied first (inner decorator)
    @validate_arguments  # Applied second (outer decorator)
    def fibonacci(self, n: int) -> int:
        """
        Computes the nth Fibonacci number.
        
        Args:
            n (int): The index of the Fibonacci number to compute.
        
        Returns:
            int: The nth Fibonacci number.
        """
        if n < 2:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)

# Usage
math = MathOperations()

# Compute the 100th Fibonacci number
print(math.fibonacci(100))  # Computes quickly due to memoization

# This would raise a ValueError due to argument validation:
# math.fibonacci(100, 200)

# Explanation of decorator behavior:
# 1. @validate_arguments ensures that only one argument (besides self) is passed
# 2. @memoize caches the results of previous computations
# 
# The order of decorators is important:
# - @memoize is applied first (inner), so it caches the results
# - @validate_arguments is applied second (outer), so it checks arguments
#   before the memoized function is called
# 
# This combination allows for both efficient computation (through memoization)
# and proper argument validation.
