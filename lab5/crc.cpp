
#include <iostream>
#include <bitset>
#include <cstdlib>

const int N = 250;
const int CRC_SIZE = 7;

using Bits = std::bitset<N + CRC_SIZE>;

unsigned int crc_check(unsigned int G, Bits remainder) {
    for (int i = N + CRC_SIZE - 1; i >= CRC_SIZE; i--) 
    {
        if (remainder[i]) 
        {
            for (int j = 0; j <= CRC_SIZE; j++) 
            {
                remainder[i - CRC_SIZE + j] =
                    remainder[i - CRC_SIZE + j] ^ ((G >> j) & 1u);
            }
        }
    }

    unsigned int crc = 0;

    for (int i = 0; i < CRC_SIZE; i++) 
    {
        if (remainder[i]) {
            crc |= (1u << i);
        }
    }

    return crc;
}

int main() {
    unsigned int G = 0b11101111;
    Bits x;

    for (int i = 0; i < N; i++) 
    {
        x[i + CRC_SIZE] = rand() % 2;
    }

    unsigned int crc = crc_check(G, x);

    Bits packet = x;

    for (int i = 0; i < CRC_SIZE; i++) 
    {
        packet[i] = (crc >> i) & 1u;
    }

    std::cout << "Исходные данные с добавленными нулями: " << x << '\n';
    std::cout << "Вычисленная CRC: " << std::bitset<CRC_SIZE>(crc) << '\n';
    std::cout << "Пакет данных с CRC: " << packet << '\n';

    unsigned int priemnik = crc_check(G, packet);

    if (priemnik != 0) 
    {
        std::cout << "На приемной стороне обнаружена ошибка\n";
    }
    else 
    {
        std::cout << "На приемной стороне ошибок не обнаружено\n";
    }

    std::cout << "Остаток от деления на приемной стороне: " << std::bitset<CRC_SIZE>(priemnik) << '\n';

    int corruped = 0;
    for (int i = 0; i < CRC_SIZE + N; i++)
    {
        Bits corruped_packet = packet;
        corruped_packet.flip(i);

        if (crc_check(G, corruped_packet) != 0) 
        {
            // std::cout << "Обнаружена ошибка при искажении бита № " << i << '\n';
            corruped++;
        }
        // else
        // {
        //     std::cout << "Ошибка не обнаружена при искажении бита № " << i << '\n';
        // }
    }

    std::cout << "Всего обнаружено ошибок: " << corruped << '\n';
    std::cout << "Всего проверено битов: " << CRC_SIZE + N << '\n';

    return 0;    
}