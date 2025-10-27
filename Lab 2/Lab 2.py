import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy.io.wavfile
import sounddevice

def Ex1():
    fig, axs = plt.subplots(2)
    fig.suptitle("Exercițiul 1")
    
    samples = 10000
    x = [i*0.0001 for i in range(samples)]
    y0 = [2 * np.sin(16 * np.pi * t + 1) for t in x]
    y1 = [2 * np.cos(16 * np.pi * t + 1 - np.pi/2) for t in x]
    
    axs[0].plot(x,y0)
    axs[1].plot(x,y1)
    
    plt.savefig('Exercițiul 1.pdf', format="pdf")

def Ex2():
    fig, axs = plt.subplots(4)
    fig.suptitle("Noised signal")
    
    #4 semnale cu faze diferite
    samples = 10000
    x = [i*0.0001 for i in range(samples)]
    
    # y0 = [np.sin(16 * np.pi * t) for t in x]
    # y1 = [np.sin(16 * np.pi * t + 1) for t in x]
    # y2 = [np.sin(16 * np.pi * t + 2) for t in x]
    # y3 = [np.sin(16 * np.pi * t + 3) for t in x]
    # axs[0].plot(x, y0)
    # axs[1].plot(x, y1)
    # axs[2].plot(x, y2)
    # axs[3].plot(x, y3)
    # plt.savefig("Exercițiul 2 - partea 1.pdf", format = 'pdf')
    
    
    z = [np.exp(-t*t/2)/np.sqrt(2*np.pi) for t in x]
    
    SNR = [0.1, 1, 10, 100]
    gamma = [np.sqrt(np.linalg.norm(x)**2 / (np.linalg.norm(z) ** 2 * SNR[i])) for i in range(len(SNR))]
    
    y0 = [np.sin(16 * np.pi * x[i]) + gamma[0]*z[i] for i in range(samples)]
    y1 = [np.sin(16 * np.pi * x[i]) + gamma[1]*z[i] for i in range(samples)]
    y2 = [np.sin(16 * np.pi * x[i]) + gamma[2]*z[i] for i in range(samples)]
    y3 = [np.sin(16 * np.pi * x[i]) + gamma[3]*z[i] for i in range(samples)]
    
    axs[0].plot(x,y0)
    axs[1].plot(x,y1)
    axs[2].plot(x,y2)
    axs[3].plot(x,y3)
    plt.savefig("Exercițiul 2 - partea 2.pdf", format = 'pdf')

def Ex3():
    rate, x = scipy.io.wavfile.read('nume.wav')
    sounddevice.play(x, 44100)

def Ex4():
    fig, axs = plt.subplots(3)
    fig.suptitle("Combinare semnale")
    
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    sinusoidal = [np.sin(15 * np.pi * t) for t in x]
    sawtooth = [2*(t*7.5 - np.floor(0.5+t*7.5)) for t in x]
    combinatie = [sinusoidal[i] + sawtooth[i] for i in range(len(x))]
    
    axs[0].plot(x, sinusoidal)
    axs[1].plot(x, sawtooth)
    axs[2].plot(x, combinatie)
    plt.savefig("Exercițiul 4.pdf", format = 'pdf')
    
def Ex5():
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y0 = [np.sign(np.sin(10 * np.pi * t)) for t in x]
    y1 = [np.sign(np.sin(2 * np.pi * t)) for t in x]
    y = y0 + y1
    sounddevice.play(x, 44100)
    
def Ex6():
    fig, axs = plt.subplots(3)
    fig.suptitle("Chestii treburi frecvență")
    
    fs = 100
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y0 = [np.sin(fs * np.pi * t) for t in x]
    y1 = [np.sin(fs / 2 * np.pi * t) for t in x]
    y2 = [np.sin(2 * np.pi * 0 * t) for t in x]
    
    #Pentru f = fs/2 semnalul este mai des
    axs[0].plot(x,y0)
    #Pentru f = fs/4 semnalul este mai rar
    axs[1].plot(x,y1)
    #Pentru f = 0Hz semnalul se confundă cu axa timpului
    axs[2].plot(x,y2)
    plt.savefig("Exercițiul 6.pdf", format = 'pdf')
    
def Ex7():
    fig, axs = plt.subplots(3)
    fig.suptitle("Decimare")
    
    #0.01 timp; 0.0001 esantioane
    samples = int(0.01/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y = [np.sin(2000 * np.pi * t) for t in x]
    xDecimat = [x[i] for i in range(len(x)) if i%4==0]
    yDecimat = [y[i] for i in range(len(x)) if i%4==0]
    xDecimat2 = [x[i] for i in range(len(x)) if i%4==1]
    yDecimat2 = [y[i] for i in range(len(x)) if i%4==1]
    
    #semnalul original este continuu si frumos, in timp ce semnalul al 
    #doilea e crazy, dar totusi periodic
    axs[0].plot(x, y)
    axs[1].plot(xDecimat, yDecimat)
    #Semnalul acesta e invers fata de al doilea
    axs[2].plot(xDecimat2, yDecimat2)
    plt.savefig("Exercițiul 7.pdf", format = 'pdf')
    
def Ex8():
    fig, axs = plt.subplots(2)
    fig.suptitle("Sin α = α")
    
    samples = int(np.pi/0.0001)
    x = [i*0.0001 - np.pi/2 for i in range(samples)]
    sinx = [np.sin(t) for t in x]
    delta = [sinx[i] - x[i] for i in range(samples)]    
    
    axs[0].plot(x,x)
    axs[0].plot(x,sinx)
    axs[1].plot(x,delta)
    plt.savefig("Exercițiul 8 - sin alfa = alfa.pdf", format = 'pdf')
    
    fig, axs = plt.subplots(2)
    fig.suptitle("Aproximarea Pade")
    
    pade = [(t - (7 * t**3)/60)/(1 + (t ** 2)/20) for t in x]
    delta = [sinx[i] - pade[i] for i in range(samples)]    
    
    axs[0].set_yscale('log')
    axs[0].plot(x,sinx)
    axs[1].set_yscale('log')
    axs[1].plot(x,pade)
    plt.savefig("Exercițiul 8 - aproximarea pade.pdf", format = 'pdf')
    

#Ex1()
#Ex2()
#Ex3()
#Ex4()
#Ex5()
#Ex6()
#Ex7()
Ex8()