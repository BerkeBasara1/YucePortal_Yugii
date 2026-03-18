
def perc_calculator(T, M):
    if T != 0 and M != 0:
        return "%" + str(round((M / T) * 100))
    else:
        return "%0"