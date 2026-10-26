import numpy as np
import matplotlib.pyplot as plt

TxPowerBS = 46 #Дбм
TxPowerUE = 24 #Дбм
AntGainBS = 21 #Дби
MIMOGain = 3 #Дб
PenetrationM = 15 #Дб
IM = 1 #Дб
FeederLoss = 2 + 0.4 + 0.5 #Дб
BW_UL = 10 * 1e6 #Гц
BW_DL = 20 * 1e6 #Гц
NoiseFigureBS = 2.4 #Дб
NoiseFigureUE = 6 #Дб
SINRUL = 4 #Дб
SINRDL = 2 #Дб
f_GHz = 1.8 #ГГц
f_MHz = f_GHz * 1e3 #МГц
hBS = 30 #м
hms = 2 #м
A = 46.3
B = 33.9
h = 15 #м
b = 50 #м
w = 25 #м
phi = 67 #градусов


TermalNoiseUL = -174 + 10 * np.log10(BW_UL) 
RxSensBS = NoiseFigureBS + TermalNoiseUL + SINRUL
print(f"\nЧувствительность приемника базовой станции: {RxSensBS:.4f} дБм")
MAPL_UL = TxPowerUE - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensBS
print(f"Уровень максимально допустимых потерь сигнала восходящего канала: {MAPL_UL:.4f} дБ")

TermalNoiseDL = -174 + 10 * np.log10(BW_DL)
RxSensUE = NoiseFigureUE + TermalNoiseDL + SINRDL
print(f"Чувствительность приемника пользовательского устройства: {RxSensUE:.4f} дБм")
MAPL_DL = TxPowerBS - FeederLoss + AntGainBS + MIMOGain - IM - PenetrationM - RxSensUE
print(f"Уровень максимально допустимых потерь сигнала нисходящего канала: {MAPL_DL:.4f} дБ\n")



d_UMiNLOS = np.arange(1, 4*1e3, 1)
PL_d_UMiNLOS = (26 * np.log10(f_GHz) + 22.7 + 36.7 * np.log10(d_UMiNLOS))

d_UL_UMiNLOS = 10 ** ((MAPL_UL - 26 * np.log10(f_GHz) - 22.7)/ 36.7)
d_DL_UMiNLOS = 10 ** ((MAPL_DL - 26 * np.log10(f_GHz) - 22.7)/ 36.7)
print(f"Расстояние до базовой станции для восходящего канала: {d_UL_UMiNLOS:.4f} м")
print(f"Расстояние до базовой станции для нисходящего канала: {d_DL_UMiNLOS:.4f} м")

R_UMiNLOS = min(d_UL_UMiNLOS, d_DL_UMiNLOS)
print(f"Максимальное расстояние до базовой станции: {R_UMiNLOS:.4f} м")

S_UMiNLOS = 1.95 * R_UMiNLOS**2
print(f"Площадь обслуживания базовой станции: {S_UMiNLOS:.4f} м^2")

NBS_UMiNLOS = np.ceil(4*1e6 / S_UMiNLOS)
print(f"Количество базовых станций: {NBS_UMiNLOS:.4f}\n")


terrian = ['DU', 'U', 'SU', 'RURAL', 'ROAD']
d_Hat = np.linspace(0.1, 100, 100)
for i, fig in zip(terrian, range(1, len(terrian)+1)):
    if i in ('DU', 'U'):
        a_hms = 3.2 * (np.log10(11.75 * hms))**2 - 4.97
        Lclutter = 3 if i == 'DU' else 0
    else:
        a_hms = (1.1 * np.log10(f_MHz)) * hms - (1.56 * np.log10(f_MHz) - 0.8)
        if i == 'SU':
            Lclutter = -(2 * (np.log10(f_MHz / 28))**2 + 5.4)
        elif i == 'RURAL':
            Lclutter = -(4.78 * (np.log10(f_MHz))**2 - 18.33 * np.log10(f_MHz) + 40.94)
        else:
            Lclutter = -(4.78 * (np.log10(f_MHz))**2 - 18.33 * np.log10(f_MHz) + 35.94)

    C = A + B * np.log10(f_MHz) - 13.82 * np.log10(hBS) - a_hms + Lclutter

    s1 = 44.9 - 6.55 * np.log10(f_MHz)
    s2 = (47.88 + 13.9 * np.log10(f_MHz) - 13.9 * np.log10(hBS)) * 1/np.log10(50) 

    d_UL_t = 10 ** ((MAPL_UL - C) / s1)
    if d_UL_t >= 1:
        d_UL_Hat = d_UL_t
    else:
        d_UL_Hat = 10 ** ((MAPL_UL - C) / s2)

    d_DL_t = 10 ** ((MAPL_DL - C) / s1)
    if d_DL_t >= 1:
        d_DL_Hat = d_DL_t
    else:
        d_DL_Hat = 10 ** ((MAPL_DL - C) / s2) 

    print(f"Расстояние до базовой станции для восходящего канала в {i} местности: {d_UL_Hat:.4f} км")
    print(f"Расстояние до базовой станции для нисходящего канала в {i} местности: {d_DL_Hat:.4f} км")

    R_hat = min(d_UL_Hat, d_DL_Hat)
    print(f"Максимальное расстояние до базовой станции в {i} местности: {R_hat:.4f} км")

    PL_d_Hat = np.where(d_Hat >= 1, C + s1 * np.log10(d_Hat) , C + s2 * np.log10(d_Hat))
    S_Hat = 1.95 * R_hat**2
    print(f"Площадь обслуживания базовой станции в {i} местности: {S_Hat:.4f} км^2")

    NBS_Hat = np.ceil(100 / S_Hat)
    print(f"Количество базовых станций в {i} местности: {NBS_Hat:.4f}\n")

    plt.figure(fig)
    plt.plot(d_Hat, PL_d_Hat, 'b',label=f'COST231 Hata {i}(1800 МГц)')
    plt.plot(d_Hat, [MAPL_UL]*len(d_Hat), 'r--', label='MAPL_UL')
    plt.plot(d_Hat, [MAPL_DL]*len(d_Hat), 'g--', label='MAPL_DL')
    plt.axvline(x=d_UL_Hat, color='grey', linestyle='--', label='d_UL')
    plt.axvline(x=d_DL_Hat, color='grey', linestyle='--', label='d_DL')
    plt.xlabel('Расстояние между приёмником и передатчиком, км')
    plt.ylabel('Потери сигнала, дБ')
    plt.title(f'Зависимость потерь сигнала от расстояния в {i} местности')
    plt.legend()
    plt.tight_layout()



if phi >= 0 and phi < 35:
    C_phi = - 10  + 0.354 * phi
elif phi >= 35 and phi < 55:
    C_phi = 2.5 + 0.075 * phi
elif phi >= 55 and phi < 90:
    C_phi = 4 - 0.114 * phi

d_WI = np.linspace(0.1, 10, 100)
L0 = 32.44 + 20 * np.log10(f_MHz) + 20 * np.log10(d_WI)
L2 = - 16.9 - 10 * np.log10(w) + 10 * np.log10(f_MHz) + 20 * np.log10(h - hms) + C_phi
L1_1 = - 18 * np.log10(1 + hBS - h) if hBS > h else 0

if hBS > h:
    k_a = 54
elif hBS <= h and d_WI > 0.5:
    k_a = 54 - 0.8 * (hBS - h)
elif hBS <= h and d_WI <= 0.5:
    k_a = (54 - 0.8 * (hBS - h)) * d_WI/0.5

k_d = 18 - 15 * ((hBS - h )/ h) if hBS <=h else 18
k_f = - 4 + 0.7 * (f_MHz/925 - 1)

L1 = L1_1 + k_a + k_d * np.log10(d_WI) + k_f * np.log10(f_MHz) - 9 * np.log10(b)
L_LOS = 42.6 + 20 * np.log10(f_MHz) + 26 * np.log10(d_WI)
L_NLOS = np.where(L1 + L2 > 0, L0 + L1 + L2, L0)
C_WI = 32.44 + 20 * np.log10(f_MHz) - 18 * np.log10(1 + hBS - h)  + k_a + k_f * np.log10(f_MHz) - 9 * np.log10(b) - 16.9 - 10 * np.log10(w) + 10 * np.log10(f_MHz) + 20 * np.log10(h - hms) + C_phi

d_UL_WI = 10 ** ((MAPL_UL - C_WI) / 38)
d_DL_WI = 10 ** ((MAPL_DL - C_WI) / 38)
print(f"Расстояние до базовой станции для восходящего канала в городской застройке: {d_UL_WI:.4f} км")
print(f"Расстояние до базовой станции для нисходящего канала в городской застройке: {d_DL_WI:.4f} км")

R_WI = min(d_UL_WI, d_DL_WI)
print(f"Максимальное расстояние до базовой станции в городской застройке: {R_WI:.4f} км")

S_WI = 1.95 * R_WI**2
print(f"Площадь обслуживания базовой станции в городской застройке: {S_WI:.4f} км^2")

NBS_WI = np.ceil(4 / S_WI)
print(f"Количество базовых станций в городской застройке: {NBS_WI:.0f}")



plt.figure(6)
plt.plot(d_WI, L_NLOS, 'b',label='Walfish-Ikegami NLOS (1800 МГц)')
plt.plot(d_WI, L_LOS, 'y',label='Walfish-Ikegami LOS (1800 МГц)')
plt.plot(d_WI, [MAPL_UL]*len(d_WI), 'r--', label='MAPL_UL')
plt.plot(d_WI, [MAPL_DL]*len(d_WI), 'g--', label='MAPL_DL')
plt.axvline(x=d_UL_WI, color='grey', linestyle='--', label='d_UL')
plt.axvline(x=d_DL_WI, color='grey', linestyle='--', label='d_DL')
plt.xlabel('Расстояние между приёмником и передатчиком, км')
plt.ylabel('Потери сигнала, дБ')
plt.title('Зависимость потерь сигнала от расстояния')
plt.legend()
plt.tight_layout()



plt.figure(7)
plt.plot(d_UMiNLOS, PL_d_UMiNLOS, 'b',label='UMiNLOS (1800 МГц)')
plt.plot(d_UMiNLOS, [MAPL_UL]*len(d_UMiNLOS), 'r--', label='MAPL_UL')
plt.plot(d_UMiNLOS, [MAPL_DL]*len(d_UMiNLOS), 'g--', label='MAPL_DL')
plt.axvline(x=d_UL_UMiNLOS, color='grey', linestyle='--', label='d_UL')
plt.axvline(x=d_DL_UMiNLOS, color='grey', linestyle='--', label='d_DL')
plt.xlabel('Расстояние между приёмником и передатчиком, м')
plt.ylabel('Потери сигнала, дБ')
plt.title('Зависимость потерь сигнала от расстояния')
plt.legend()
plt.tight_layout()

plt.show()