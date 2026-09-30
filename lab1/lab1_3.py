import numpy as np
import matplotlib.pyplot as plt

def DFT(y):
    N = len(y)
    sample_y = []
    for x in range(N):
        sum_real = 0
        sum_imag = 0
        for n in range(N):
            alpha = 2 * np.pi * x * n / N
            real_val = y[n] * np.cos(alpha)
            imag_val = y[n] * (-np.sin(alpha))
            sum_real += real_val
            sum_imag += imag_val
        sample_y.append(complex(sum_real, sum_imag))
    return np.array(sample_y)

def quantize(y, bits):
    levels = 2**bits
    a = y.min()
    b = y.max()
    q = np.round((y-a)/(b-a)*(levels-1))
    return q/(levels-1)*(b-a)+a

f = 6
fs = 12*f
t = np.arange(0, 1, 1/fs)
y = 4*np.sin(2*np.pi*f*t + np.pi/3)
N = len(y)
X = DFT(y)
A = np.abs(X)/N
freq = np.arange(N)*fs/N
bits_list = [3, 4, 5, 6]
errors = []
spectrums = []
for bits in bits_list:
    yq = quantize(y, bits)
    Xq = DFT(yq)
    Aq = np.abs(Xq)/N
    error = np.mean(np.abs(y-yq))
    errors.append(error)
    spectrums.append(Aq)
    print(f"{bits} бит: средняя ошибка = {error:f}")

plt.figure(1)
for i, bits in enumerate(bits_list):
    plt.subplot(4, 1, i+1)
    yq = quantize(y, bits)
    plt.stem(t, y, linefmt='-g', markerfmt='go', label="Исходный")
    plt.stem(t, yq, label=f"{bits} бит")
    plt.title(f"Квантование {bits} бит")
    plt.xlabel("Время, с")
    plt.ylabel("Амплитуда")
    plt.grid()
    plt.legend()
plt.tight_layout()

plt.figure(2)
for i, bits in enumerate(bits_list):
    plt.subplot(4, 1, i+1)
    plt.plot(freq[:N//2 + 1], A[:N//2 + 1], label="Исходный")
    plt.plot(freq[:N//2 + 1], spectrums[i][:N//2 + 1], label=f"{bits} бит")
    plt.title(f"Спектр {bits} бит")
    plt.xlabel("Частота, Гц")
    plt.ylabel("|C(k)|")
    plt.grid()
    plt.legend()
plt.tight_layout()

plt.figure(3)
plt.plot(bits_list, errors, "o-")
plt.xlabel("Разрядность АЦП, бит")
plt.ylabel("Средняя ошибка")
plt.title("Ошибка квантования")
plt.grid()
plt.xticks(bits_list)
plt.show()