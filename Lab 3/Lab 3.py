import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.animation as animation
import numpy as np
import math

def X(t, f = 1, A = 1, sigma = 0):
    return A * np.sin(2 * np.pi * f * t + sigma)


def Ex1():
    N = 8
    F = [[math.e**(-2 * np.pi * 1j * m * k / N)/np.sqrt(N) for k in range(N)] for m in range(N)]
    
    for i in range(1,N//2+1):
        fig, axs = plt.subplots(2)
        x = [(i+1)/N for i in range(N)]
        
        y0_Real = [F[i][j].real for j in range(N)]
        y0_Imaginar = [F[i][j].imag for j in range(N)]
        y1_Real = [F[N-i][j].real for j in range(N)]
        y1_Imaginar = [F[N-i][j].imag for j in range(N)]
        
        axs[0].plot(x, y0_Real)
        axs[0].plot(x, y0_Imaginar,'--')
        axs[1].plot(x, y1_Real)
        axs[1].plot(x, y1_Imaginar,'--')
        
    FHF = np.matmul(np.conj(np.transpose(F)), np.matrix(F))
    FFH = np.matmul(np.matrix(F), np.conj(np.transpose(F)))
    print(np.allclose(FHF,FFH))

def Ex2_Fig1():
    fig,axs = plt.subplots(ncols=2)
    x = [i for i in range(1000)]
    y = [X(t/1000, f=5) for t in x]
    cerc = [X(t) * math.e**(-2*np.pi*1j*t/1000) for t in x]
    real = [elem.real for elem in cerc]
    imag = [elem.imag for elem in cerc]
    
    linie, = axs[0].plot(x,y)
    floare, = axs[1].plot(real,imag)
    punct_linie, = axs[0].plot([], [], 'ro', markersize=6)
    punct_floare, = axs[1].plot([], [], 'ro', markersize=6)
    
    fig.tight_layout(pad=3.0)
    axs[0].set(xlabel = 'Timp (esantionare)', ylabel = 'Amplitudine')
    axs[1].set(xlabel = 'Real', ylabel = 'Imaginar')
    
    def update(frame):
        frame = 4*frame
        linie.set_data(x[:frame], y[:frame])
        floare.set_data(real[:frame], imag[:frame])
        
        punct_linie.set_data(x[frame-1], y[frame-1])
        punct_floare.set_data(real[frame-1], imag[frame-1])
        
        return linie, floare, punct_linie, punct_floare
    
    anim = animation.FuncAnimation(fig=fig, func=update, frames=250, interval=1, blit=True)
    anim.save(filename="floare.gif", writer="pillow")
    plt.show()
    
def Ex2_Fig2():
    fig,axs = plt.subplots(nrows=2, ncols=2)
    omegaValues = [1,2,5,7]
    x = [i/1000 for i in range(1000)]

    fig.tight_layout(pad=3.0)
    for i in range(len(omegaValues)):
        omega = omegaValues[i]
        cerc = [X(t,f=5) * math.e**(-2 * np.pi * 1j * omega * t) for t in x]
        real = [elem.real for elem in cerc]
        imag = [elem.imag for elem in cerc]
        
        l, c = i//2, i%2
        
        axs[l][c].set_xlim(-1,1)
        axs[l][c].set_ylim(-1,1)
        axs[l][c].axhline(0, color='black', linewidth=1)  # linia Ox
        axs[l][c].axvline(0, color='black', linewidth=1)  # linia Oy
        axs[l][c].set(xlabel = 'Real', ylabel = 'Imaginar', title=f'ω = {omega}')
        axs[l][c].plot(real, imag)
        plt.savefig("Exercițiul 2.pdf", format = 'pdf')
        
def Ex3():
    def _x(t):
        return X(t, f=59, A=1.37) + \
             X(t, f=8, A=0.28) + \
             X(t, f=94, A=1.92)
    
    fig,axs = plt.subplots(ncols=2, figsize=(15,8))
    x = [i/1000 for i in range(1000)]
    y = [_x(t) for t in x]
    absXom = [abs(sum([_x(x[i])*math.e**(-2 * np.pi * 1j * omega * i / len(x)) for i in range(len(x))])) for omega in range(101)]
    axs[0].plot(x[:301],y[:301])
    axs[1].stem(range(101), absXom)
    plt.savefig("Exercițiul 3.pdf", format = 'pdf')    
    
        
#Ex1()
#Ex2_Fig1()
#Ex2_Fig2()
Ex3()