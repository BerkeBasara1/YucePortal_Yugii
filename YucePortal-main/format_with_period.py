
def format_with_period(n):
    n = str(n)
    n_len = len(n)
    if n_len <= 3:
        return n
    else:
        return format_with_period(n[:-3]) + "." + n[-3:]