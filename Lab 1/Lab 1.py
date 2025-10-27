import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import scipy.io.wavfile


def save_image(filename):
  
    p = PdfPages(filename)
    
    fig_nums = plt.get_fignums()  
    figs = [plt.figure(n) for n in fig_nums]
    
    for fig in figs:   
        fig.savefig(p, format='pdf') 
        
    p.close()  

def Ex1():
    n = 3
    fig, axs = plt.subplots(n)
    fig.suptitle('Exercitiul 1')
   
    for ax in axs.flat:
        ax.set_xlim([0, 0.03])
    samples = int(0.03/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y0 = [np.cos(520 * np.pi * t + np.pi/3) for t in x]
    y1 = [np.cos(280 * np.pi * t - np.pi/3) for t in x]
    y2 = [np.cos(120 * np.pi * t + np.pi/3) for t in x]

    axs[0].plot(x,y0)
    axs[1].plot(x,y1)
    axs[2].plot(x,y2)

    samples = int(200*0.03)
    x = [i/200 for i in range(samples)]
    y0 = [np.cos(520 * np.pi * nt + np.pi / 3) for nt in x]
    y1 = [np.cos(280 * np.pi * nt - np.pi / 3) for nt in x]
    y2 = [np.cos(120 * np.pi * nt + np.pi / 3) for nt in x]

    axs[0].stem(x,y0)
    axs[1].stem(x,y1)
    axs[2].stem(x,y2)
                
    plt.savefig('Exercițiul 1.pdf', format='pdf')

def Ex2():
    n = 4
    fig1, axs = plt.subplots(4)
    fig1.suptitle('Exercitiul 2')
    
    
    #semnal sinusoidal fv= 400Hz, 1600 esantioane
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y = [np.sin(800 * np.pi * t) for t in x]
    axs[0].set_xlim([0, 0.01])
    axs[0].plot(x, y)
    
    rate = int(10e5) 
    scipy.io.wavfile.write('nume.wav', rate, np.array(y))
    
    samples = 1600
    xEsantionat = [i/1600 for i in range(samples)]
    yEsantionat = [np.sin(800 * np.pi * nt) for nt in xEsantionat]
    axs[0].stem(xEsantionat, yEsantionat)
    
    #semnal sinusoidal care să dureze 3s
    samples = int(3/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y = [np.sin(1600 * np.pi * t) for t in x]
    axs[1].set_xlim([0, 0.01])
    axs[1].plot(x,y)
    
    #semnal sawtooth fv = 240Hz
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y = [2*(t*240 - np.floor(0.5+t*240)) for t in x]
    axs[2].set_xlim([0, 0.1])
    axs[2].plot(x,y)
    
    #semnal square fv = 300Hz
    samples = int(1/0.0001)
    x = [i*0.0001 for i in range(samples)]
    y = [np.sign(np.sin(600 * np.pi * t)) for t in x]
    axs[3].set_xlim([0,0.05])
    axs[3].plot(x,y)
    
    #2D semnal
    fig2 = plt.figure()
    x = y = 128
    a = np.array(np.random.rand(x,y))
    plt.imshow(a)
    
    #2D semnal random
    def data(x,y):
        return [[(_x+np.log(_y))%20 for _y in range(y)] for _x in range(x)]
    
    fig3 = plt.figure()
    a = np.array(data(x,y))
    plt.imshow(a)
    
    save_image('Exercițiul 2.pdf')
    

#Ex1()
Ex2()
