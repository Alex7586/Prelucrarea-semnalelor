import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.animation as animation
import numpy as np
import math
import time
import csv
from datetime import datetime
import pandas as pd

N = 1000
x = np.array([i for i in range(N)])
trend = np.array([3 * i * i + 2 * i + 7 for i in range(N)])
sezon = np.array([1e6 * (np.sin(0.7 * np.pi * i) + np.sin(0.24 * np.pi * i)) for i in range(N)])
variatii = 1e6 * np.random.normal(size=N)
y = trend + sezon + variatii
fig, axs = plt.subplots(nrows=4, figsize=(8, 8))
fig.tight_layout(pad=3.0)

axs[0].set(ylabel = 'y')
axs[1].set(ylabel = 'Trend')
axs[2].set(ylabel = 'Sezon')
axs[3].set(ylabel = 'Variatii')

axs[0].plot(x, y)
axs[1].plot(x, trend)
axs[2].plot(x, sezon)
axs[3].plot(x, variatii)

p = 2
Y = np.column_stack([y[p-1-j : N-1-j] for j in range(p)])
x, _, _, _ = np.linalg.lstsq(Y, y[p:], rcond='None')

yPred = np.array([sum([x[j] * y[j] for i in range()]) for i in range(p-1,N)])




