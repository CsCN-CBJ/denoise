# -*- coding: utf-8 -*-
import numpy as np
import wave_modify
import wavio
import LMS
import NLMS
import SpectralSub
import matplotlib.pyplot as plt

# deal with one single channel
def origin_handler(old_data, rate, t):
    wave_second = np.array([])
    wave_second = old_data[:t*rate]
    wave_second.shape = -1 , rate
    new_data = np.array([])
    for second in range(t):#对每一秒分别处理
        new_wave = LMS.LMS1(wave_second[second], 64, 0.0001)
        new_data = np.append(new_data , new_wave)
        print(str(second)+'OK')
    #new_data = np.append(new_data , old_data[t*rate:])#把最后剩的接上
    return new_data

def fft_handler(old_data, rate, t, fft_freqs, handler_name):
    wave_second = np.array([])
    wave_second = old_data[:t*rate]
    wave_second.shape = -1 , rate
    new_data = np.array([])
    for second in range(t):#对每一秒分别处理
        modi_wave = np.fft.fft(wave_second[second])
        if handler_name == 'low':
            modi_wave = wave_modify.low(modi_wave , fft_freqs)
        elif handler_name == 'mid':
            modi_wave = wave_modify.mid(modi_wave , fft_freqs)
        elif handler_name == 'high':
            modi_wave = wave_modify.high(modi_wave , fft_freqs)
        # elif handler_name == 'under_water':
        #     modi_wave = wave_modify.under_water(modi_wave , fft_freqs)
        else:
            raise ValueError
        # modi_wave = np.fft.fftshift(modi_wave)
        new_wave = np.fft.ifft(modi_wave).real
        new_data = np.append(new_data , new_wave)
    #new_data = np.append(new_data , old_data[t*rate:])#把最后剩的接上
    #print(new_data.shape)
    return new_data

def invalid_killer(data):
    '''
    param: data 一维数组
    return: 去除非法数字的数组
    '''
    for i in range(len(data)):
        if data[i] == np.nan or abs(data[i]) == np.inf:
            data[i]=0
    return data

def wave_reader(src , dest, handler_name='null', denoise = True):
    #防止Spyder不显示图像
    #plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    #plt.rcParams['axes.unicode_minus'] = False
    #开始读取文件
    file = wavio.read(src)#获得一个对象
    file_sampwidth = file.sampwidth
    wave_data = file.data
    rate = file.rate#取样频率
    nchannels = wave_data.shape[1]#声道数
    #print('nchannels:'+str(nchannels))
    wave_data = wave_data.T#
    #print(type(wave_data))
    #通过取样点数和取样频率计算出每个取样的时间,也就是周期T=采样单数/采样率
    time=np.arange(0,wave_data.shape[1])* (1.0/rate)#仅仅为了画图
    t = int(time[-1])
    fft_freqs = np.fft.fftfreq(rate , time[1] - time[0])#最高频率为rate//2
    #对音频进行处理（我知道这样写很蠢）
    #print(wave_data[1][10000:11000])
    new_data = np.array([])
    if nchannels == 1:
        #wave_data虽然只有一行，但也要取第0行
        new_data = wave_data[1]
        if denoise:
            new_data = SpectralSub.handler(new_data, rate)
        new_data = invalid_killer(new_data)
        if handler_name != 'null':
            new_data = fft_handler(new_data, rate, t, fft_freqs, handler_name)
        # new_data -= np.mean(new_data)

    #双声道需要一个两行的数组
    
    else:
        #new_data = fft_handler(wave_data[0], rate, t, fft_freqs)
        #new_data = origin_handler(wave_data[0], rate, t)
        # print(wave_data[0].shape)
        # print(wave_data[0][40000:41000])
        
        new_data = wave_data[0]
        new_data1 = wave_data[1]
        
        if denoise:
            new_data = SpectralSub.handler(new_data, rate)
            new_data1 = SpectralSub.handler(new_data1, rate)
            
        new_data = invalid_killer(new_data)
        new_data1 = invalid_killer(new_data1)
        
        if handler_name != 'null':
            new_data = fft_handler(new_data, rate, t, fft_freqs, handler_name)  
            new_data1 = fft_handler(new_data1, rate, t, fft_freqs, handler_name)
        
        # new_data1 -= np.mean(new_data1)
        #vstack needs (()) , do not delete any of them
        new_data = np.vstack((new_data, new_data1))
        #print(new_data1[5*rate:5*rate+1000]==new_data[1][5*rate:5*rate+1000])
    #new_data = new_data.astype(int)
    #print(np.mean(new_data))
    # print(new_data1[:100])
    # plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
    # plt.rcParams['axes.unicode_minus'] = False
    # plt.subplot(111)
    # print(new_data1.shape==time.shape)
    # print(new_data1[:1000])
    # plt.plot(time,new_data1,'g')
    wavio.write(dest , new_data.T , rate , sampwidth=file_sampwidth)
    
    
if __name__ == '__main__':
    src = 'D:/Desktop/工地测试_01.wav'
    #src = 'D:/Desktop/0.wav'
    dest = 'D:/Desktop/water.wav'
    wave_reader(src, dest,'high',False)
    
