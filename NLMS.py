import numpy as np

def LMS(xn, dn, M, mu, itr):
    """
    使用LMS自适应滤波
    :param xn:输入的信号序列
    :param dn:所期望的响应序列
    :param M:滤波器的阶数
    :param mu:收敛因子(步长)
    :param itr:迭代次数
    :return:
    """
    en = np.zeros(itr)  # 误差序列,en(k)表示第k次迭代时预期输出与实际输入的误差
    W = np.zeros((M, itr))  # 每一行代表一个加权参量,每一列代表-次迭代,初始为0
    # 迭代计算
    for k in range(M, itr):
        x = xn[k:k - M:-1]
        y = np.matmul(W[:, k - 1], x)
        en[k] = dn[k] - y
        W[:, k] = W[:, k - 1] + 2 * mu * en[k] * x
    # 求最优输出序列
    yn = np.inf * np.ones(len(xn))
    for k in range(M, len(xn)):
        x = xn[k:k - M:-1]
        yn[k] = np.matmul(W[:, -1], x)
    return yn


def NLMS(xn, dn, M, mu, itr):
    """
    使用Normal LMS自适应滤波
    :param xn:输入的信号序列
    :param dn:所期望的响应序列
    :param M:滤波器的阶数
    :param mu:收敛因子(步长)
    :param itr:迭代次数
    :return:
    """
    en = np.zeros(itr)  # 误差序列,en(k)表示第k次迭代时预期输出与实际输入的误差
    W = np.zeros((M, itr))  # 每一行代表一个加权参量,每一列代表-次迭代,初始为0
    # 迭代计算
    for k in range(M, itr):
        x = xn[k:k - M:-1]
        y = np.matmul(W[:, k - 1], x)
        en[k] = dn[k] - y
        W[:, k] = W[:, k - 1] + 2 * mu * en[k] * x / (np.sum(np.multiply(x, x)) + 1e-10)
    # 求最优输出序列
    yn = np.inf * np.ones(len(xn))
    for k in range(M, len(xn)):
        x = xn[k:k - M:-1]
        yn[k] = np.matmul(W[:, -1], x)
    return en



def handler(data, method='NLMS', M=64, mu=0.001, offset=10):
    '''
    :param method:方法LMS,NLMS
    :param M:滤波器的阶数
    :param mu:收敛因子(步长)
    :param offset:输入信号延迟帧数
    '''
    data = data - np.mean(data)
    data_max = np.max(np.abs(data))
    data /= data_max
    itr = len(data)
    
    #计算期望
    dn = np.zeros(itr)
    if offset > 0:
        dn[:-offset] += data[offset:]
    elif offset == 0:
        dn = data
    else:
        offset=abs(offset)
        dn[offset:] += data[:-offset]
    
    #选择方法
    if method == 'LMS':
        output = LMS(data, dn, M, mu, itr)
    else:
        output = NLMS(data, dn, M, mu, itr)
    output *= data_max
    # print(output[:100])
    return output