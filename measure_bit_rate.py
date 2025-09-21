import time
from functools import wraps

def measure_bit_Rate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        result = func(*args, **kwargs)
        et = time.time()
        
        if result is None:
            print(f"Function '{func.__name__}' returned None. Bit rate cannot be calculated.")
            return result
        
        if isinstance(result, str):
            result_bytes = result.encode('utf-8')
        else:
            result_bytes = result
            
        total_bits = len(result_bytes) * 8
        total_time = et-st
        bit_rate = (total_bits / total_time) if total_time > 0 else 0
        
        print(f"Function '{func.__name__}' processed {total_bits} bits in {total_time:.3f}s")
        print(f"Bit rate: {bit_rate:.2f} bits/s")
        return result
    return wrapper
        