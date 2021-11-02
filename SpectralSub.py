import numpy as np

def enframe(x, win, inc=None):
    nx = len(x)
    if isinstance(win, list) or isinstance(win, np.ndarray):
        nwin = len(win)
        nlen = nwin  # 帧长=窗长
    elif isinstance(win, int):
        nwin = 1
        nlen = win  # 设置为帧长
    if inc is None:
        inc = nlen
    nf = (nx - nlen + inc) // inc
    frameout = np.zeros((nf, nlen))
    indf = np.multiply(inc, np.array([i for i in range(nf)]))
    for i in range(nf):
        frameout[i, :] = x[indf[i]:indf[i] + nlen]
    if isinstance(win, list) or isinstance(win, np.ndarray):
        frameout = np.multiply(frameout, np.array(win))#相同形状的矩阵，对应位置元素相乘
        #例如 1 2  multiply 1 2 等于 1 4
        #     3 4           3 4     9 16
    return frameout

def SpectralSub(signal, wlen, inc, NIS, a, b):
    """
    谱减法滤波
    :param signal:
    :param wlen:
    :param inc:
    :param NIS:
    :param a:
    :param b:
    :return:
    """
    wnd = np.hamming(wlen)#初始化汉明窗
    y = enframe(signal, wnd, inc)
    fn, flen = y.shape
    y_a = np.abs(np.fft.fft(y, axis=1))#计算复数的幅角
    y_a2 = np.power(y_a, 2)#y_a的平方
    y_angle = np.angle(np.fft.fft(y, axis=1))
    Nt = np.mean(y_a2[:NIS, ], axis=0)#平均值
    
    #相当于c语言里temp=a>b?c:d;并且对数组中每个元素都执行一遍
    y_a2 = np.where(y_a2 >= a * Nt, y_a2 - a * Nt, b * Nt)

    X = y_a2 * np.cos(y_angle) + 1j * y_a2 * np.sin(y_angle)
    hatx = np.real(np.fft.ifft(X, axis=1))#取实部

    sig = np.zeros(int((fn - 1) * inc + wlen))#创建指定长度的数组，其所有元素为0

    for i in range(fn):
        start = i * inc
        sig[start:start + flen] += hatx[i, :]
    return sig

def handler(data, rate, IS=0.05, wlen=400, inc=10):
    '''
    Parameters
    ----------
    data    : np.array原始数据
    
    rate    : fs, how many frames per second
    
    IS      : 前导无话段长度
    
    wlen    : 帧长（单位：帧）
    
    inc     : 帧移（单位：帧）
    '''
    datamax = np.max(np.abs(data))
    data = data - np.mean(data)
    #做标准化处理
    data /= np.max(np.abs(data))
    #参数初始化
    NIS = int((IS * rate - wlen) // inc + 1)
    a, b = 4, 0.001
    #进行谱减法处理
    output = SpectralSub(data, wlen, inc, NIS, a, b)
    #反标准化处理
    filted = output
    filted *= datamax/20
    filted = filted.astype(int)
    # print(filted[4000:5000])
    # print(len(filted))
    # print(filted.shape)
    # print(filted[40000:41000])
    return filted
    