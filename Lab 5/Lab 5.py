import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.animation as animation
import numpy as np
import math
import time
import csv
from datetime import datetime
import pandas as pd


# (e)
x = np.genfromtxt('Train.csv', delimiter=',')[1:, 2]
if np.average(x) == 0:
    print('Nu are componentă continuă')
else:
    print(f'Semnualul prezinta o componenta continua DC = {np.average(x)}')
    x = x-np.average(x)
    print(x)
print('\n\n')

# (d)
X = np.fft.fft(x)
N = len(x)
X = abs(X/N)
X = X[:N//2]
Fs = 3 * (10 ** (-4))
f = Fs * np.linspace(0, N//2, N//2) / N

fig, axs = plt.subplots()
plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
axs.set(xlabel = 'Frecvențe')
axs.plot(f[:len(f)//3], X[:len(f)//3])
plt.savefig("FFT - bullet train.pdf", format="pdf")

    
# (f)
ind = np.argpartition(X, -4)[-4:]
top4FFT = X[ind]
top4Fv = f[ind]
axs.scatter(top4Fv, top4FFT)
print(top4Fv,'\n\n')

# (g)
df = pd.read_csv('Train.csv',\
                 usecols = ["Datetime", "Count"],\
                parse_dates = ["Datetime"],\
                dayfirst = True)

indexPrimaLuni = df.iloc[1000:][df.iloc[1000:]["Datetime"].dt.weekday == 0].index.min()
esantioane = np.arange(indexPrimaLuni, indexPrimaLuni+744)  
nrMasini = np.array([df["Count"][i] for i in esantioane])
fig, axs = plt.subplots()
axs.set(xlabel = 'Esantioane', ylabel = 'Numar masini')
axs.plot(esantioane, nrMasini)
plt.savefig("Traficul dintr-o luna.pdf", format = "pdf")
