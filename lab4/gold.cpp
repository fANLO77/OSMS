#include <iostream>
#include <vector>
#include <bitset>
#include <iomanip>


const int N = 31;

std::vector<int> gold(unsigned int x , unsigned int y) {
    std::vector<int> result;
    for (int i = 0; i < N; i++)
    {
        int ox = x & 1u; 
        int oy = y & 1u;
        int out = ox ^ oy;
        result.push_back(out);
        int fx = ((x >> 1) & 1u) ^ (x & 1u);
        int fy = ((y >> 3) & 1u) ^ (y & 1u);
        std::cout << std::left
                << "| " << std::setw(6)  << "Step"
                << "| " << std::setw(8)  << "X"
                << "| " << std::setw(10) << "Output X"
                << "| " << std::setw(12) << "Feedback X"
                << "| " << std::setw(8)  << "Y" 
                << "| " << std::setw(10) << "Output Y"
                << "| " << std::setw(12) << "Feedback Y"
                << "| " << std::setw(8) << "Output"
                << "|\n";
        std::cout << "| " << std::setw(6)  << i + 1
                << "| " << std::setw(8)  << std::bitset<5>(x)
                << "| " << std::setw(10) << ox
                << "| " << std::setw(12) << fx
                << "| " << std::setw(8)  << std::bitset<5>(y)
                << "| " << std::setw(10) << oy
                << "| " << std::setw(12) << fy
                << "| " << std::setw(8) << out 
                << "|\n";
        std::cout << std::string(91, '-') << '\n';
        x = (x >> 1) | (fx << 4);
        y = (y >> 1) | (fy << 4);
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

int main() {
    unsigned int x1 = 0b00011;
    unsigned int y1 = 0b01010;
    unsigned int x2 = 0b00100;
    unsigned int y2 = 0b00101;
    std::cout << "Исходные значения\n";
    std::cout << "x = 3: " << std::bitset<5>(x1) << '\n';
    std::cout << "y = 10: " << std::bitset<5>(y1) << '\n';
    std::cout << "\nГенерация последовательности Голда для исходных значений\n";
    auto seq1 = gold(x1, y1);
    std::cout << "\nИзменные значения\n";
    std::cout << "x = x + 1: " << std::bitset<5>(x2) << '\n';
    std::cout << "y = y - 5: " << std::bitset<5>(y2) << '\n';
    std::cout << "\nГенерация последовательности Голда для измененных значений\n";
    auto seq2 = gold(x2, y2);
    std::cout << "\nАвтокорреляция исходной последовательности Голда\n\n";
    std::cout << std::left << std::setw(8) << "Сдвиг" << "|";
    for (int j = 0; j < N; j++)
    {
        std::cout << std::setw(5) << ("Бит" + std::to_string(j + 1)) << "|";
    }
    std::cout << " Автокорреляция\n";
    std::cout << std::string(8 + N * 6 + 20, '-') << '\n';
    for (int i = 0; i < N; i++)
    {
        std::cout << std::setw(8) << i << "|";
        for (int j = 0; j < N; j++)
        {
            std::cout << std::setw(5)
                      << seq1[(j + i) % N] << "|";
        }
        double R = corr(seq1, seq1, i);
        std::cout << " " << std::fixed << std::setprecision(6)
                  << R << '\n';
    }
    std::cout << "\nКорреляция между исходной и измененной последовательностями Голда\n";
    for (int i = 0; i < N; i++)
    {
        auto R = corr(seq1, seq2, i);
        std::cout << "Сдвиг: " << i << ", R = " << R << '\n';
    }
    return 0;
}