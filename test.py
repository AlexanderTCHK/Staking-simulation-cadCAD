import random
import numpy as np

num = np.random.lognormal(10, .5, 1000)
print(np.mean(num))
