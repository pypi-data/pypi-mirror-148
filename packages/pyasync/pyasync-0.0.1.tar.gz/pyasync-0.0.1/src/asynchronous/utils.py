

def get_timeout(size: int):
    """Obtain the timeout according to the threshold value"""
    if 0 <= size < 1e2:
        timeout = 3e1
    elif 1e2 < size < 5e2:
        timeout = 6e1
    else:
        timeout = 6e1 * 2
    return timeout
