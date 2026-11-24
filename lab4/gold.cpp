#include <iostream>
#include <vector>
#include <bitset>
#include <iomanip>
#include <cmath>


const int N = 127;

std::vector<int> gold(unsigned int x , unsigned int y) {
    std::vector<int> result;
    for (int i = 0; i < N; i++)
    {
        int ox = x & 1u; 
        int oy = y & 1u;
        int out = ox ^ oy;
        result.push_back(out);
        int fx = ((x >> 6) & 1u) ^ (x & 1u);
        int fy = ((y >> 6) & 1u) ^ (y & 1u);
        // std::cout << std::left
        //         << "| " << std::setw(6)  << "Step"
        //         << "| " << std::setw(8)  << "X"
        //         << "| " << std::setw(10) << "Output X"
        //         << "| " << std::setw(12) << "Feedback X"
        //         << "| " << std::setw(8)  << "Y" 
        //         << "| " << std::setw(10) << "Output Y"
        //         << "| " << std::setw(12) << "Feedback Y"
        //         << "| " << std::setw(8) << "Output"
        //         << "|\n";
        // std::cout << "| " << std::setw(6)  << i + 1
        //         << "| " << std::setw(8)  << std::bitset<7>(x)
        //         << "| " << std::setw(10) << ox
        //         << "| " << std::setw(12) << fx
        //         << "| " << std::setw(8)  << std::bitset<7>(y)
        //         << "| " << std::setw(10) << oy
        //         << "| " << std::setw(12) << fy
        //         << "| " << std::setw(8) << out 
        //         << "|\n";
        // std::cout << std::string(91, '-') << '\n';
        x = (x >> 1) | (fx << 6);
        y = (y >> 1) | (fy << 6);
    }
    return result;
}

double corr(const std::vector<int>& seq1, const std::vector<int>& seq2, int shift) {
    int ns = 0;
    int R = 0;
    for (int i = 0; i < N; i++)
    {
        if (seq1[i] != seq2[(i + shift) % N]) 
        {
            ns++;
        }
    }
    return (N - 2 * ns) * (1.0 / N);
}

void balance(const std::vector<int>& seq) {
    int count0 = 0;
    bool ok = true;
    for (int i = 0; i < N; i++)
    {
        if (seq[i] == 0)
        {
            count0++;
        }
    }
    if (std::abs((N - count0) - count0) > 1)
    {
        ok = false;
    }
    std::cout << (ok ? "Свойство сбалансированности выполняется\n" : "Свойство сбалансированности не выполняется\n");
    std::cout << "\tКоличество нулей: " << count0 << '\n';
    std::cout << "\tКоличество единиц: " << N - count0 << '\n';
}

void runs(const std::vector<int>& seq, double eps = 0.15) {
    std::vector<int> count(N + 1, 0);   
    int total = 0;                   
    int len = 1;                     
    int maxLen = 1;

    for (int i = 1; i <= N; i++)
    {
        if (i < N && seq[i] == seq[i - 1])
        {
            len++;
        }
        else
        {
            count[len]++;
            total++;
            if (len > maxLen) maxLen = len;
            len = 1;
        }
    }

    std::cout << "\nПроверка цикличности\n";
    std::cout << "\tВсего серий: " << total << ", самая длинная серия: " << maxLen << '\n';
    std::cout << "\t" << std::left << std::setw(8) << "Длина"
              << std::setw(13) << "Количество"
              << std::setw(10) << "Доля"
              << "Идеальная доля\n";

    bool ok = true;
    double ideal = 1.0;
    for (int k = 1; k <= maxLen; k++)
    {
        ideal /= 2.0;                                  
        double share = (double)count[k] / total;
        std::cout << "\t" << std::setw(8) << k
                  << std::setw(13) << count[k]
                  << std::setw(10) << std::fixed << std::setprecision(3) << share
                  << ideal << '\n';
        if (k <= 3 && std::fabs(share - ideal) > eps)
        {
            ok = false;
        }
    }

    std::cout << (ok ? "Свойство цикличности выполняется\n" : "Свойство цикличности не выполняется\n");
}

int main() {
    unsigned int x1 = 0b0000011;
    unsigned int y1 = 0b0001010;
    unsigned int x2 = 0b0000100;
    unsigned int y2 = 0b0000101;
    std::cout << "Исходные значения\n";
    std::cout << "x = 3: " << std::bitset<7>(x1) << '\n';
    std::cout << "y = 10: " << std::bitset<7>(y1) << '\n';
    std::cout << "\nГенерация последовательности Голда для исходных значений\n";
    auto seq1 = gold(x1, y1);
    balance(seq1);
    runs(seq1);
    std::cout << "\nИзменные значения\n";
    std::cout << "x = x + 1: " << std::bitset<7>(x2) << '\n';
    std::cout << "y = y - 5: " << std::bitset<7>(y2) << '\n';
    std::cout << "\nГенерация последовательности Голда для измененных значений\n";
    auto seq2 = gold(x2, y2);
    balance(seq2);
    runs(seq2);
    // std::cout << "\nАвтокорреляция исходной последовательности Голда\n\n";
    // std::cout << std::left << std::setw(8) << "Сдвиг" << "|";
    // for (int j = 0; j < N; j++)
    // {
    //     std::cout << std::setw(7) << ("Бит" + std::to_string(j + 1)) << "|";
    // }
    // std::cout << " Автокорреляция\n";
    // std::cout << std::string(8 + N * 6 + 20, '-') << '\n';
    // for (int i = 0; i < N; i++)
    // {
    //     std::cout << std::setw(8) << i << "|";
    //     for (int j = 0; j < N; j++)
    //     {
    //         std::cout << std::setw(7)
    //                   << seq1[(j + i) % N] << "|";
    //     }
    //     double R = corr(seq1, seq1, i);
    //     std::cout << " " << std::fixed << std::setprecision(6)
    //               << R << '\n';
    // }
    // std::cout << "\nКорреляция между исходной и измененной последовательностями Голда\n";
    // for (int i = 0; i < N; i++)
    // {
    //     auto R = corr(seq1, seq2, i);
    //     std::cout << "Сдвиг: " << i << ", R = " << R << '\n';
    // }
    return 0;
}