import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read

def FFT(y):
    N = len(y)
    if N == 1:
        return y
    E = FFT(y[0::2])
    O = FFT(y[1::2])
    Y = np.zeros(N, dtype=complex)
    for k in range(N // 2):
        W = np.exp(-1j * 2 * np.pi * k / N)
        t = W * O[k]
        Y[k] = E[k] + t
        Y[k + N//2] = E[k] - t
    return Y


Fs = 1000
BEAT = 0.6
melody = [(329.63, 1.0), (369.99, 1.0), (415.30, 2.0), (369.99, 1.0),
          (329.63, 1.0), (369.99, 0.5), (329.63, 0.5), (311.13, 2.0),
          (329.63, 1.0), (369.99, 1.0), (415.30, 2.0), (369.99, 1.0),
          (329.63, 1.0), (311.13, 1.0), (329.63, 3.0)]

Y = []
for freq, beat in melody:
    duration = BEAT * beat
    t = np.arange(0, duration, 1 / Fs)
    s = np.sin(2 * np.pi * freq * t)
    Y.append(s)
Y = np.concatenate(Y)
N = 2 ** int(np.ceil(np.log2(len(Y))))
Y_padded = np.zeros(N)
Y_padded[:len(Y)] = Y
spectrum = FFT(Y_padded)
amplitudes = [abs(k)/(N ) for k in spectrum]
freq = np.arange(N) * Fs / N
plt.plot(freq, amplitudes)
plt.xlim(250, 500)
plt.xlabel("Частота (Гц)")
plt.ylabel("Амплитуда")
plt.grid(True)
plt.show()