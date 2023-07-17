import numpy as np

def kursverlauf(tendenz, streuung, dt, start):
    newPrice = 0
    sqdt = np.sqrt(dt)
    Y = 2 * np.random.rand() - 1.0
    newPrice =  start * (1 + tendenz * dt + streuung * sqdt * Y)
    return newPrice

start = 5.0 * (2*np.random.rand() - 1.0)
drift = 1.3 * (2*np.random.rand() - 1.0)

price = kursverlauf(tendenz=drift, streuung=1.0, dt=0.001, start=start)

for i in range(25):
    price = kursverlauf(tendenz=drift, streuung=20.0, dt=0.001, start=price)
    while price < 1:
        price = kursverlauf(tendenz=drift, streuung=20.0, dt=0.001, start=price + 1)
        
    print(price)

