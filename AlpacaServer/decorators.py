def retry_redis_request(func, times=5):
    def wrapper(*args, **kwargs):
        val = None
        for _ in range(times):
            try:
                val = func(*args, **kwargs)
            except:
                pass
            if val is not None:
                break
        return val
    return wrapper
