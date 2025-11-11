import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.animation as animation
import numpy as np
import math
import time


def xFun(t, f=1, A=1, faza=0):
    return A * np.sin(2 * np.pi * f * t + faza)


def FFT(esantioane, m, n):
    if len(esantioane) == 1:
        return xFun(esantioane[0], f=1000) + \
            xFun(esantioane[0], f=2000, A=0.5, faza=3 * np.pi / 4)
    even = [esantioane[i] for i in range(0, len(esantioane), 2)]
    odd = [esantioane[i] for i in range(1, len(esantioane), 2)]
    return FFT(even, m, len(even)) + \
        np.exp(-2 * np.pi * 1j * m / n) * FFT(odd, m, len(odd))


def Ex1():
    def _x(t):
        return xFun(t, f=1000) + \
            xFun(t, f=2000, A=0.5, faza=3 * np.pi / 4)

    N = [128, 256, 512, 1024, 2048, 4096, 8192]
    fs = 8000
    x = [i/1000 for i in range(1000)]
    y = [_x(t) for t in x]

    xN = range(len(N))
    yDFT = []
    yFFT = []
    ynpFFT = []
    fig, axs = plt.subplots()

    # DFT
    for n in N:
        s = time.time()
        fa = [m*fs/n for m in range(n//2+1)]
        absXom = [abs(sum([_x(x[i])*math.e**(-2 * np.pi * 1j * omega * i / len(x))
                           for i in range(len(x))])) for omega in fa]
        e = time.time()
        yDFT += [round((e - s) * 1000, 3)]

    # FFT
    for n in N:
        s = time.time()
        esantioane = [i*fs/n for i in range(n)]
        X = [abs(FFT(esantioane, m, n)) for m in range(n//2+1)]
        e = time.time()
        yFFT += [round((e-s)*1000, 3)]

    # FFT numpy
    for n in N:
        s = time.time()
        X = np.fft.fft(y, n)
        e = time.time()
        ynpFFT += [round((e-s)*1000, 3)]

    axs.set_yscale("log")
    axs.plot(xN, yDFT)
    axs.plot(xN, yFFT)
    axs.plot(xN, ynpFFT)


def Ex2():
    B=7
    def _x(t):
        return xFun(t, f = B)

    fig, axs = plt.subplots(nrows=2)
    fs = 3
    f1 = 10
    f2 = 4
    x = np.arange(0, 0.7, 1/10000)
    xEsantioane = np.arange(0, 0.7, 1/fs)
    yEsantioane = (lambda t: _x(t))(np.array(xEsantioane))
    y1 = (lambda t: _x(t))(np.array(x))
    y2 = (lambda t: xFun(t, f1))(np.array(x))
    y3 = (lambda t: xFun(t, f2))(np.array(x))

    axs[0].plot(x, y1)
    axs[0].plot(xEsantioane[:8], yEsantioane[:8], 'o')
    axs[1].plot(x, y2)
    axs[1].plot(x, y3)
    axs[1].plot(xEsantioane[:8], yEsantioane[:8], 'o')
    plt.savefig("Exercițiul 2.pdf", format = 'pdf')
    
def Ex3():
    def _x(t, f=1):
        return np.sin(2 * np.pi * f * t)

    fig, axs = plt.subplots(nrows=2)
    f0 = 175
    fs = 1000
    B = fs/2 - 50
    x = np.arange(0, 0.05, 1/10000)
    xEsantioane = [i/fs for i in range(fs)]
    yEsantioane = (lambda t: _x(t, f0))(np.array(xEsantioane))
    y1 = (lambda t: _x(t, f0))(np.array(x))
    y2 = (lambda t: _x(t, f0 - B))(np.array(x))
    y3 = (lambda t: _x(t, f0 + B))(np.array(x))

    axs[0].plot(x[:len(x)//2], y1[:len(x)//2])
    axs[0].plot(xEsantioane[:8], yEsantioane[:8], 'o')
    axs[1].plot(x[:len(x)//2], y2[:len(x)//2])
    axs[1].plot(x[:len(x)//2], y3[:len(x)//2])
    axs[1].plot(xEsantioane[:8], yEsantioane[:8], 'o')
    plt.savefig("Exercițiul 3.pdf", format = 'pdf')

def Ex4():
    print("fs >= 2 * B  ==> fs >= 320; fs - min ==> fs = 320Hz")


#Ex1()
#Ex2()
Ex3()
#Ex4()