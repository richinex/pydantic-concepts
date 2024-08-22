## Decorators
# Importing necessary modules
# time: Used for adding delays and measuring execution time
# functools: Provides the wraps decorator to preserve metadata of wrapped functions
# typing: Offers type hinting capabilities for better code documentation
import time
import functools
from typing import Callable, Any, Dict

# Define a decorator factory that creates a parameterized decorator
# This factory allows us to create decorators with custom settings
def retry_with_delay(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Create a decorator that retries the wrapped function with a delay between attempts.
    
    Args:
        max_attempts (int): Maximum number of retry attempts (default: 3)
        delay (float): Delay in seconds between retry attempts (default: 1.0)
    
    Returns:
        Callable: A decorator function
    """
    
    # Define the actual decorator function
    # This function will wrap around the original function
    def decorator(func: Callable) -> Callable:
        """
        The decorator function that wraps the original function.
        
        Args:
            func (Callable): The function to be decorated
        
        Returns:
            Callable: The wrapped function
        """
        
        # Use functools.wraps to preserve the metadata of the original function
        # This ensures that the wrapped function retains its original name, docstring, etc.
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            The wrapper function that adds retry logic to the original function.
            
            Args:
                *args: Positional arguments to pass to the original function
                **kwargs: Keyword arguments to pass to the original function
            
            Returns:
                Any: The return value of the original function
            
            Raises:
                Exception: If all retry attempts fail
            """
            
            # Initialize attempts counter
            attempts = 0
            
            # Continue trying until max_attempts is reached
            while attempts < max_attempts:
                try:
                    # Attempt to execute the original function
                    return func(*args, **kwargs)
                except Exception as e:
                    # Increment the attempts counter
                    attempts += 1
                    
                    # Log the exception and attempt number
                    print(f"Attempt {attempts} failed: {str(e)}")
                    
                    # If this was the last attempt, re-raise the exception
                    if attempts == max_attempts:
                        raise
                    
                    # Wait for the specified delay before the next attempt
                    time.sleep(delay)
            
            # This line should never be reached due to the raise in the loop
            # It's here to satisfy mypy type checking
            raise Exception("Unexpected end of retry loop")
        
        # Return the wrapper function
        return wrapper
    
    # Return the decorator function
    return decorator

# Define a metaclass for logging method calls
# Metaclasses are used to customize class creation
class LogMethodCalls(type):
    """
    A metaclass that adds logging to all methods of a class.
    """
    
    # Override the __new__ method to customize class creation
    def __new__(cls, name: str, bases: tuple, attrs: Dict[str, Any]) -> type:
        """
        Create a new class with logging added to its methods.
        
        Args:
            name (str): Name of the class being created
            bases (tuple): Base classes of the class being created
            attrs (Dict[str, Any]): Attributes dictionary of the class being created
        
        Returns:
            type: The newly created class
        """
        
        # Iterate through all attributes of the class
        for attr_name, attr_value in attrs.items():
            # Check if the attribute is a method (but not a special method)
            if callable(attr_value) and not attr_name.startswith("__"):
                # Wrap the method with a logging decorator
                attrs[attr_name] = cls.log_method(attr_value)
        
        # Call the parent __new__ method to create the class
        return super().__new__(cls, name, bases, attrs)
    
    # Define a static method to create a logging wrapper for methods
    @staticmethod
    def log_method(method: Callable) -> Callable:
        """
        Create a wrapper that logs method calls.
        
        Args:
            method (Callable): The method to be wrapped
        
        Returns:
            Callable: The wrapped method with logging
        """
        
        # Use functools.wraps to preserve the metadata of the original method
        @functools.wraps(method)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that adds logging to the method.
            
            Args:
                *args: Positional arguments to pass to the original method
                **kwargs: Keyword arguments to pass to the original method
            
            Returns:
                Any: The return value of the original method
            """
            
            # Log the method call
            print(f"Calling method: {method.__name__}")
            
            # Call the original method and store its result
            result = method(*args, **kwargs)
            
            # Log the method completion
            print(f"Method {method.__name__} completed")
            
            # Return the result of the original method
            return result
        
        # Return the wrapper function
        return wrapper

# Define a class that uses our metaclass and decorated methods
class DatabaseConnection(metaclass=LogMethodCalls):
    """
    A class representing a database connection with retry logic.
    """
    
    # Initialize the connection status
    def __init__(self) -> None:
        """
        Initialize the DatabaseConnection instance.
        """
        self.connected = False
    
    # Apply the retry decorator to the connect method
    @retry_with_delay(max_attempts=5, delay=2.0)
    def connect(self) -> None:
        """
        Attempt to connect to the database.
        
        Raises:
            ConnectionError: If the connection attempt fails
        """
        # Simulate a connection attempt that may fail
        if not self.connected:
            # Simulate a 70% chance of failure
            if time.time() % 10 < 7:
                raise ConnectionError("Failed to connect to database")
            self.connected = True
        print("Connected to database")
    
    # Define a query method
    def query(self, sql: str) -> str:
        """
        Execute a SQL query.
        
        Args:
            sql (str): The SQL query to execute
        
        Returns:
            str: The result of the query
        
        Raises:
            RuntimeError: If not connected to the database
        """
        if not self.connected:
            raise RuntimeError("Not connected to database")
        return f"Query result: {sql}"

# Demonstrate the usage of our decorated class
if __name__ == "__main__":
    # Create an instance of DatabaseConnection
    db = DatabaseConnection()
    
    # Attempt to connect to the database
    db.connect()
    
    # Execute a query
    result = db.query("SELECT * FROM users")
    print(result)
