import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0 ,1, 1000)
f = 6
fs = 2 * f
y = 4 * np.sin(2 * np.pi * f * t + np.pi / 3)
sample_t = []
sample_y = []
for i in range(0, fs):
    ti = i/fs
    yi = 4 * np.sin(2 * np.pi * f * ti + np.pi / 3)
    sample_t.append(ti)
    sample_y.append(yi)
print(*sample_t,'\n')
print(*sample_y,'\n')
N = len(sample_y)
spectrum = []

for x in range(N):
    sum_real = 0
    sum_imag = 0
    for n in range(N):
        alpha = 2 * np.pi * x * n / N
        real_val = sample_y[n] * np.cos(alpha)
        imag_val = sample_y[n] * (-np.sin(alpha))
        sum_real += real_val
        sum_imag += imag_val
    spectrum.append(complex(sum_real, sum_imag))
amplitudes = [abs(k)/(N ) for k in spectrum]
freq = np.arange(N) * (fs / N) 
print(freq)
print(amplitudes)
plt.figure(1, figsize=(10, 5)) 
plt.plot(t, y, 'b-', label='Непрерывный сигнал')
plt.stem(sample_t, sample_y, linefmt='-r', markerfmt='ro', basefmt=' ', label=f'Отсчеты')
plt.title('Дискретизация сигнала по времени')
plt.xlabel('Время (с)')
plt.ylabel('Амплитуда')
plt.legend()
plt.grid(True)

plt.figure(2, figsize=(10, 5)) 
plt.stem(freq, amplitudes, linefmt='-g', markerfmt='go', basefmt=' ') 
plt.title('Спектр')
plt.xlabel('Частота (Гц)')
plt.ylabel('|F(k)|')
plt.xticks(np.arange(0, N, 1)) 
plt.grid(True)
plt.show()