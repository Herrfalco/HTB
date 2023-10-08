#!/usr/bin/env python3

import numpy as np
import scipy.io.wavfile as wav

from scipy.fft import fft

N = 1_000_000
T = .0001

if __name__ == '__main__':
    sample_rate, data = wav.read('encrypted.wav')

    amps = fft(data)
    freqs = np.fft.fftfreq(N, T)

    amps = np.abs(amps)
    for a, f in sorted([(a, f) for a, f in zip(amps, freqs) if a > 1 and f > 0]):
        c = f * 10
        while not chr(int(c)).isascii():
            c /= 4
        print(chr(int(c)), end='')
    print()
