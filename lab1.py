import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0 ,1, 1000)
f = 6
fs_values = [3 * f, 12 * f]
y = 4 * np.sin(2 * np.pi * f * t + np.pi / 3)
for fs in fs_values:
    sample_t = []
    sample_y = []
    for i in range(0, fs):
        ti = i/fs
        yi = 4 * np.sin(2 * np.pi * f * ti + np.pi / 3)
        sample_t.append(ti)
        sample_y.append(yi)
    print(f"\nЧастота дискретизации: {fs} Гц")
    print("Отсчёты времени:")
    print(*sample_t, '\n')
    print("Отсчёты сигнала:")
    print(*sample_y, '\n')
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
    amplitudes = [abs(k)/(N) for k in spectrum]
    freq = np.arange(N) * (fs / N)
    print("Частоты:")
    print(freq)
    print("Амплитуды спектра:")
    print(amplitudes)
    porog = max(amplitudes) * 0.1
    sush_freq = [fr for fr, a in zip(freq[:N//2 + 1], amplitudes[:N//2 + 1]) if a > porog]
    print("Значимые частоты:")
    print(sush_freq)
    print("Ширина спектра (0...f):", max(sush_freq) - min(sush_freq), "Гц")
    total_bytes = N * np.dtype(np.float64).itemsize
    print("Объём массива float64 (байт):", total_bytes)

    plt.figure()
    plt.plot(t, y, 'b-', label='Непрерывный сигнал')
    plt.stem(sample_t, sample_y, linefmt='-r', markerfmt='ro', basefmt=' ', label='Отсчёты')
    plt.title(f'Дискретизация сигнала: fs = {fs} Гц')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)

    plt.figure()
    plt.stem(freq[:N//2 + 1], amplitudes[:N//2 + 1], linefmt='-g', markerfmt='go', basefmt=' ')
    plt.title(f'Спектр: fs = {fs} Гц')
    plt.xlabel('Частота (Гц)')
    plt.ylabel('|C(k)|')
    plt.xticks(freq[:N//2 + 1])
    plt.grid(True)

    plt.figure()
    plt.plot(t, y, 'b-', label='Оригинальный сигнал')
    plt.plot(sample_t, sample_y, 'r.-', label='Восстановлено по отсчётам')
    plt.title(f'Оригинал и отсчёты: fs = {fs} Гц')
    plt.xlabel('Время (с)')
    plt.ylabel('Амплитуда')
    plt.legend()
    plt.grid(True)
plt.show()
