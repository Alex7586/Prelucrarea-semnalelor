import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.animation as animation
import numpy as np
import math
import time
import csv
from datetime import datetime
import pandas as pd


def Ex1():
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    fig.tight_layout(pad=3.0)
    B = 1
    t = np.arange(-3, 3, 1/10000)
    x = np.vectorize(lambda t: np.sinc(B*t) ** 2)
    F = [1, 1.5, 2, 4]
    Ts = [1/f for f in F]
    for plot in range(4):
        i, j = plot // 2, plot % 2

        tEsantion1 = np.arange(0, -3 - Ts[plot], -Ts[plot])
        tEsantion2 = np.arange(0 + Ts[plot], 3 + Ts[plot], Ts[plot])
        tEsantion = np.concatenate((tEsantion1[::-1], tEsantion2), axis=None)
        xc = np.vectorize(lambda t: np.sum([x(k)*np.sinc((t-k)/(Ts[plot]))
                                            for k in tEsantion]))

        axs[i][j].set(xlabel='t[s]', ylabel='Amplitude',
                      title=fr'$F_s = {F[plot]} Hz$')
        axs[i][j].plot(t, x(t), "k")
        axs[i][j].stem(tEsantion, x(tEsantion), "#FFA500", basefmt='k')
        axs[i][j].plot(t, xc(t), "g--")
    plt.savefig('Exercițiul 1.pdf', format="pdf")


def Ex2():
    def conv(h, x):
        n = np.size(x)
        return [sum([h[k] * x[i-k] for k in range(i)]) for i in range(n)]

    fig, axs = plt.subplots(nrows=4, figsize=(8, 8))

    t = np.arange(0, 1, 1/100)
    x = np.random.random(100)
    x = x - np.average(x)
    axs[0].plot(t, x)

    for i in range(1, 4):
        x = conv(x, x)
        axs[i].plot(t, x)

    plt.savefig('Exercițiul 2.pdf', format="pdf")


def Ex3():
    def genereazaPolinom(N, low=-10, high=10):
        return np.random.randint(low, high+1, N+1)

    Np, Nq = 5, 3
    p = genereazaPolinom(Np)
    q = genereazaPolinom(Nq)

    lenp = Np + 1
    lenq = Nq + 1

    size = lenp + lenq - 1
    
    # inmultire directa
    result = np.zeros(size, dtype=int)
    for i in range(lenp):
        for j in range(lenq):
            result[i + j] += p[i] * q[j]
    print(f'p(x) = {p}\nq(x) = {q}')
    print(result)
    
    # fft
    N = 1
    while N < size:
        N *= 2
        
    P = np.fft.fft(np.pad(p, (0, N - lenp)))
    Q = np.fft.fft(np.pad(q, (0, N - lenq)))

    R = P * Q
    result = np.fft.ifft(R)
    result = np.round(result.real).astype(int)
    print(result[:size])

def Ex4():
    n = 20
    t = np.linspace(0, 2*np.pi, n)
    x = np.sin(t) + 0.5 * np.cos(3*t)
    d = np.random.randint(1, np.size(x))
    y = np.roll(x, d)
    
    # inmultire
    X = np.conj(np.fft.fft(x))
    Y = np.fft.fft(y)
    R = X * Y
    result = np.fft.ifft(R)
    dCalc = np.argpartition(result.real, -1)[-1:][0]
    print(d, dCalc)
    
    # impartire
    X = np.fft.fft(x)
    Y = np.fft.fft(y)
    R = Y / X
    result = np.fft.ifft(R)
    dCalc = np.argpartition(result.real, -1)[-1:][0]
    print(d, dCalc)
    
def Ex5():
    def dreptunghi(N):
        return np.ones(N)
    
    def hanning(N):
        n = np.arange(N)
        return 0.5 * (1 - np.cos(2*np.pi*n / (N-1)))
    
    fig, axs = plt.subplots(nrows=3, figsize=(8, 8))
    fig.tight_layout(pad=3.0)
    
    t = np.linspace(0, 0.4, 1000)
    f = 100
    x = np.vectorize(lambda t: np.sin(2 * np.pi * f * t))(t)
    Nw = 200
    wd = dreptunghi(Nw)
    wh = hanning(Nw)
    xdrept = x[200:400] * wd
    xhann = x[200:400] * wh
    axs[0].plot(t, x)
    axs[1].plot(t, np.pad(xdrept, (200, 600)))
    axs[2].plot(t, np.pad(xhann, (200, 600)))
    plt.savefig('Exercițiul 5.pdf', format="pdf")
    

#Ex1()
#Ex2()
#Ex3()
#Ex4()
Ex5()
