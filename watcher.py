# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import wavio


path = ['D:/Desktop/测试/带噪音频.wav']#, 'D:/Desktop/lab/waves/new_1n.wav']
path.append('D:/Desktop/测试/new_带噪音频.wav')
# path.append('D:/Desktop/101.wav')


for i in range(len(path)):
    right = 0#画右声道
    start = 2
    
    #防止Spyder不显示图像
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    plt.rcParams['axes.unicode_minus'] = False
    #开始读取文件
    file = wavio.read(path[i])#获得一个对象
    wave_data = file.data
    rate = file.rate#取样频率
    nchannels = wave_data.shape[1]#声道数
    print('nchannels:' + str(nchannels))
    wave_data = wave_data.T#有几个声道就有几行
    
    #通过取样点数和取样频率计算出每个取样的时间,也就是周期T=采样单数/采样率
    time=np.arange(0,wave_data.shape[1])* (1/rate)#仅仅为了画图
    print(rate)
    t = int(time[-1])
    
    fft_freqs = np.fft.fftfreq(rate, 1/rate)#最高频率为rate//2
    #print(fft_freqs[:rate//2])
    #画初始波形图
    plt.figure(str(i))#对话框标注
    plt.subplot(121)#两行两列第一个   

    if nchannels == 1:
        fft_wave = np.fft.fft(wave_data[start*rate:(start+1)*rate])
        plt.plot(time,wave_data,'g')#横纵，颜色（可以RGB）
    else:
        fft_wave = np.fft.fft(wave_data[right][start*rate:(start+1)*rate])
        plt.plot(time,wave_data[right],'g')#横纵，颜色（可以RGB）
        
    plt.xlabel("Time")#x轴标注
    plt.ylabel("Amplitude")#y轴标注
    plt.title("Original wave")#表格标题
    #画频谱图
    #fft_wave[0]=0
    #fft_wave = a * np.power(fft_wave, b)
    # fft_wave = abs(fft_wave)
    # fft_wave = 10 * np.log(fft_wave) / np.log(10)
    #print(fft_wave[:200])
    plt.subplot(122)#两行两列第二个
    plt.plot(fft_freqs,fft_wave,'g')#默认画最后一个整秒（左声道）
    plt.xlabel("Freq (Hz)")#x轴标注
    plt.ylabel("|Y(freq)|")#y轴标注
    plt.title("FFT wave")#表格标题
    
    plt.show()