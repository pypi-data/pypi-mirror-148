
def primos(num):
    numPrimos = []
    for i in range(2, num + 1):
        primo = True
        for x in range(2, i):
            if x != num and i % x == 0:
                primo = False;
        if primo:
            numPrimos.append(i)
    return numPrimos
