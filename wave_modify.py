# -*- coding: utf-8 -*-
import numpy as np
def wave_modi(fft_wave , freq):
    for i in range(len(freq)):
        if abs(freq[i])<123 or abs(freq[i])>493:
            fft_wave[i]=0
    return fft_wave

def wave_modi1(fft_wave , freq):
    return fft_wave

def wave_modi2(fft_wave, freq):
    a = -2.173e-15
    b = 3.338
    c = 1.014
    return a*np.power(fft_wave, b)+c*fft_wave

def wave_modi3(fft_wave, freq):
    for i in range(len(freq)):
        if abs(freq[i]>10000):
            fft_wave[i] *= 1-(i-10000)/14000
    return fft_wave

def wave_modi4(fft_wave, freq):
    for i in range(len(freq)):
        if abs(freq[i]>1000) and abs(freq[i]<10000):
            fft_wave[i] *= 1-(i-1000)/10000
        elif abs(freq[i]>10000) and abs(freq[i]<15000):
            fft_wave[i] *= i/5000 - 2
        elif abs(freq[i]==10000):
            fft_wave[i] = 0
            print('doit')
    return fft_wave

def low(fft_wave, freq):
    for i in range(len(freq)):
        if abs(freq[i]) > 1000:
            fft_wave[i]=0
    return fft_wave

def high(fft_wave, freq):
    for i in range(len(freq)):
        if abs(freq[i]) < 2000:
            fft_wave[i] = 0
    return fft_wave

def mid(fft_wave , freq):
    for i in range(len(freq)):
        if abs(freq[i]) < 200 or abs(freq[i]) > 4000:
            fft_wave[i]=0
    return fft_wave

def mute_all(fft_wave, freq):
    for i in range(len(freq)):
        fft_wave[i]=0
    return fft_wave

def under_water(fft_wave, freq):
    for i in range(len(freq)):
        x = abs(freq[i])
        p1 = 7.909e-09
        p2 = -0.0001801
        p3 = 1.023
        fft_wave[i] *= p1*x*x + p2*x +p3
    return fft_wave