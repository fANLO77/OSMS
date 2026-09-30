import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write


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

fs , y = wavfile.read("test.wav")
print("Размер сигнала:", y.shape)
print("Частота дискретизации:", fs)
time = y.shape[0] / fs
fs_check = y.shape[0] / 16.9
print("Частота дискретизации по независимой длительности:", fs_check, "Гц")
print("Длительность сигнала:", time, "с")
y_10 = y[::10]
Fs_10 = fs/ 10
print("Частота после прореживания:", Fs_10, "Гц")
write("ex.wav", int(Fs_10), y_10)
N_orig = len(y)
N_10_orig = len(y_10)
N = 2 ** int(np.ceil(np.log2(len(y))))
N_10 = 2 ** int(np.ceil(np.log2(len(y_10))))
y_fft = np.pad(y, (0, N - len(y)))
y_10_fft = np.pad(y_10, (0, N_10 - len(y_10)))
spectrum = FFT(y_fft)
spectrum_10 = FFT(y_10_fft)
amplitudes = [abs(k)/(N ) for k in spectrum]
amplitudes_10 = [abs(k)/(N_10) for k in spectrum_10]
freq = np.arange(N) * (fs / N) 
freq_10 = np.arange(N_10) * (Fs_10 / N_10)
porog = max(amplitudes) * 0.1
sush_freq = [fr for fr, a in zip(freq[:N//2 + 1], amplitudes[:N//2 + 1]) if a > porog]
porog_10 = max(amplitudes_10) * 0.1
sush_freq_10 = [fr for fr, a in zip(freq_10[:N_10//2 + 1], amplitudes_10[:N_10//2 + 1]) if a > porog_10]
print("Ширина исходного спектра (0...f):", max(sush_freq) - min(sush_freq), "Гц")
print("Ширина спектра после прореживания (0...f):", max(sush_freq_10) - min(sush_freq_10), "Гц")

plt.figure(1)
t_orig = np.arange(N_orig) / fs
t_10 = np.arange(N_10_orig) / Fs_10
plt.plot(t_orig, y[:N_orig], label='Исходный сигнал')
plt.plot(t_10, y_10, label='После прореживания x10')
plt.title('Сравнение сигналов')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)

plt.figure(2)
plt.plot(freq[:N//2], np.asarray(amplitudes[:N//2]), label='Исходный сигнал')
plt.plot(freq_10[:N_10//2], np.asarray(amplitudes_10[:N_10//2]), label='После прореживания x10')
plt.title('Сравнение спектров')
plt.xlabel('Частота (Гц)')
plt.ylabel('|C(k)|')
plt.legend()
plt.grid(True)

plt.figure(3)
plt.plot(freq[:N//2], np.asarray(amplitudes[:N//2]))
plt.xlabel('Частота (Гц)')
plt.ylabel('|C(k)|')
plt.title('Спектр исходного сигнала')
plt.grid(True)

plt.figure(4)
plt.plot(freq_10[:N_10//2], np.asarray(amplitudes_10[:N_10//2]))
plt.xlabel('Частота (Гц)')
plt.ylabel('|C(k)|')
plt.title('Спектр после прореживания x10')
plt.grid(True)
plt.show()