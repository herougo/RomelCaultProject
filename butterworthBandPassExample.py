from scipy.signal import butter, lfilter
from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

if __name__ == "__main__":

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 300.0
    lowcut = 65.0
    highcut = 130.0

    # Filter a noisy signal.
    T = 1.0 / fs
    nsamples = T * fs
    a = 0.02
    x = np.linspace(0.0, fs*T, fs)
    xf = np.linspace(0.0, 1.0/(2.0*T), fs/2)
    z = np.random.randn(int(fs))
    y = np.sin(125.0 * 2.0*np.pi*x) + np.cos(75.0 * 2.0*np.pi*x) + z
    c = butter_bandpass_filter(y, lowcut, highcut, fs, order=6)
     
    fig1 = plt.figure(1)
    graph1 = fig1.add_subplot(211)
    graph2 = fig1.add_subplot(212)
    graph1.plot(x, y, '-g', label='Noisy signal')
    graph1.hlines([-3, 3], 0, T, linestyles='--')
    graph1.grid(True)
    graph1.legend(loc='upper left')
    graph2.plot(x, c, '-b', label='Filtered signal (%g Hz)' % fs)
    graph2.hlines([-3, 3], 0, T, linestyles='--')
    graph2.grid(True)
    graph2.legend(loc='upper left')
    plt.xlabel('time (seconds)')
    
    fig2 = plt.figure(2)
    graph1 = fig2.add_subplot(211)
    graph2 = fig2.add_subplot(212)
    graph1.plot(x, y, '-g', label='Noisy signal, time domain')
    graph1.grid(True)
    graph1.legend(loc='upper left')
    y1 = fft(y)
    graph2.plot(xf, 2.0/fs * np.abs(y1[0:fs/2]))
    graph2.grid(True)
    
    fig3 = plt.figure(3)
    graph1 = fig3.add_subplot(211)
    graph2 = fig3.add_subplot(212)
    graph1.plot(x, c, '-g', label='Clean signal, time domain')
    graph1.grid(True)
    graph1.legend(loc='upper left')
    c1 = fft(c)
    graph2.plot(xf, 2.0/fs * np.abs(c1[0:fs/2]))
    graph2.grid(True)

    plt.show()
    