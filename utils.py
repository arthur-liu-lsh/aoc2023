import time
from typing import Any, Callable, List


def parse(file_name: str, func:Callable = None) -> List[str]:
    with open(file_name, 'r') as file:
        if func is not None:
            lines = [func(line.rstrip()) for line in file.readlines()]
        else:
            lines = [line.rstrip() for line in file.readlines()]

    return lines

def measure(func:Callable) -> Callable:
    def inner(*args, **kwargs) -> Any:
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"Execution time: {(end-start)*1000} ms")
    return inner