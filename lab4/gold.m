clear; clc; close all;

N = 31;
x1 = [0 0 0 1 1];   % x = 3
y1 = [0 1 0 1 0];   % y = 10
x2 = [0 0 1 0 0];   % x = 4
y2 = [0 0 1 0 1];   % y = 5

fprintf('Исходные значения\n');
fprintf('x = 3 : %s\n', num2str(x1, '%d'));
fprintf('y = 10: %s\n\n', num2str(y1, '%d'));
fprintf('Генерация последовательности Голда для исходных значений\n');
seq1 = gold_seq(x1, y1, N, true);
fprintf('\nИзменённые значения\n');
fprintf('x = x + 1: %s\n', num2str(x2, '%d'));
fprintf('y = y - 5: %s\n\n', num2str(y2, '%d'));
fprintf('Генерация последовательности Голда для изменённых значений\n');
seq2 = gold_seq(x2, y2, N, true);
fprintf('\nПоследовательность 1: %s\n', num2str(seq1, '%d'));
fprintf('Последовательность 2: %s\n', num2str(seq2, '%d'));

a = 1 - 2*seq1;
b = 1 - 2*seq2;

[cxx, lags] = xcorr(a, a);
cxx = cxx / N;
fprintf('\nАвтокорреляция исходной последовательности\n\n');
fprintf('%-7s |', 'Сдвиг');

for j = 1:N
    fprintf(' Бит %-3d|', j);
end
fprintf(' Автокорреляция\n');
fprintf('%s\n', repmat('-', 1, 8 + 10*N + 18));

for s = 0:N-1
    shifted = circshift(seq1, -s);
    fprintf('%-7d |', s);
    for j = 1:N
        fprintf(' %-6d|', shifted(j));
    end
    R = cxx(lags == s);
    fprintf(' %12.6f\n', R);

end
[cxy, ~] = xcorr(a, b);
cxy = cxy / N;
fprintf('\nВзаимная корреляция исходной и изменённой последовательностей\n');

for i = 1:length(lags)
    fprintf('Сдвиг: %3d, R = %8.4f\n', lags(i), cxy(i));
end
[acf, acf_lags] = autocorr(a, 'NumLags', N-1);
fprintf('\nautocorr: первые значения (лаги 0..5):\n');
disp([acf_lags(1:6); acf(1:6)]');

figure('Name', 'Автокорреляция кода Голда - xcorr');
stem(lags, cxx, 'filled', 'MarkerSize', 4);
grid on;
xlabel('Задержка (lag)');
ylabel('R(lag)');
title('Автокорреляция кода Голда (xcorr)');

figure('Name', 'Взаимная корреляция - xcorr');
stem(lags, cxy, 'filled', 'MarkerSize', 4);
grid on;
xlabel('Задержка (lag)');
ylabel('R(lag)');
title('Взаимная корреляция двух кодов Голда (xcorr)');

if ~isempty(acf)
    figure('Name', 'Автокорреляция - autocorr');
    stem(acf_lags, acf, 'filled', 'MarkerSize', 4);
    grid on;
    xlabel('Задержка (lag)');
    ylabel('Автокорреляция');
    title('Автокорреляция кода Голда (autocorr)');
end

function seq = gold_seq(x, y, N, verbose)
    seq = zeros(1, N);
    if verbose
        fprintf('| %-5s| %-8s| %-9s| %-11s| %-8s| %-9s| %-11s| %-7s|\n', ...
            'Step', 'X', 'Output X', 'Feedback X', ...
            'Y', 'Output Y', 'Feedback Y', 'Output');
    end
    for i = 1:N
        ox = x(5);
        oy = y(5);
        out = xor(ox, oy);
        fx = xor(x(4), x(5));
        fy = xor(y(2), y(5));
        if verbose
            fprintf('| %-5d| %-8s| %-9d| %-11d| %-8s| %-9d| %-11d| %-7d|\n', ...
                i, num2str(x, '%d'), ox, fx, ...
                num2str(y, '%d'), oy, fy, out);
        end
        seq(i) = out;
        x = [fx, x(1:4)];
        y = [fy, y(1:4)];

    end
end