from typing    import Callable, Any, Optional, Type
from functools import wraps
from .logger   import Log


class Run:
    """
    Class to handle runtime
    """
    
    @staticmethod
    def Error(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Error function to catch errors
        
        @param func: The function to wrap.
        @return:     Custom error message
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Run.handle_error(e)
                return None 
        return wrapper

    @staticmethod
    def handle_error(exception: Exception) -> Optional[None]:
        """
        Handling an error
        
        @param exception: Exception that occured
        """
        Log.Error(f"Error occurred: {exception}")
        exit()
        
class Utils:
    
    @staticmethod
    def between(
        main_text: Optional[str],
        value_1: Optional[str],
        value_2: Optional[str],
        ) -> Type[str]:
        return main_text.split(value_1)[1].split(value_2)[0]