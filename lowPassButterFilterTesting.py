from scipy.fftpack import fft
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Filter requirements.
order = 6
fs = 30.0       # sample rate, Hz
cutoff = 3.6  # desired cutoff frequency of the filter, Hz

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

# Number of sample points
N = 600
# sample spacing
T = 1.0 / 800.0
x = np.linspace(0.0, N*T, N)
z = np.random.randn(600)
y = np.cos(50.0 * 2.0*np.pi*x) + np.sin(100.0 * 2.0*np.pi*x) + np.cos(75.0 * 2.0*np.pi*x) + z 
print(type(y))

fig = plt.figure(1)
fig.clf()
graph1 = fig.add_subplot(211)
graph2 = fig.add_subplot(212)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
yf = fft(y)
graph1.plot(x, y)
graph2.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
graph1.grid(True)
graph2.grid(True)
plt.title("Raw data")

fig = plt.figure(2)
fig.clf()
graph1 = fig.add_subplot(211)
graph2 = fig.add_subplot(212)
data = butter_lowpass_filter(y, cutoff, fs, order)
yf1 = fft(data)
graph1.plot(x, data)
graph2.plot(xf, 2.0/N * np.abs(yf1[0:N/2]))
graph1.grid(True)
graph2.grid(True)
plt.title("Low pass filtered data")

fig = plt.figure(3)
fig.clf()
graph1 = fig.add_subplot(211)
graph2 = fig.add_subplot(212)
graph1.plot(x, data, 'b-', label='filtered data')
graph2.plot(x, y, 'g-',  label='data')
plt.xlabel('Time [sec]')
graph1.grid(True)
graph2.grid(True)
graph1.legend()
graph2.legend()
plt.show()
