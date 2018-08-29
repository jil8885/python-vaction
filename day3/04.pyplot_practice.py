import matplotlib.pyplot as plt
import numpy as np


def prac1():
    plt.figure(figsize=(12, 6))
    y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    x = range(0, len(y))
    plt.plot(x, y)
    plt.grid()
    plt.show()


def prac2():
    t = np.arange(0, 12, 0.01)
    y = np.sin(t)

    plt.figure(figsize=(12, 6))
    plt.plot(t, y)
    plt.grid()
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('Amplitude')
    plt.title('Example of sine wave')
    plt.show()


def prac3():
    t = np.arange(0, 12, 0.01)

    plt.figure(figsize=(12, 6))
    plt.plot(t, np.sin(t),lw=3, label='sin', linestyle='dashed')
    plt.plot(t, np.cos(t), 'r', label='cos')
    plt.grid()
    plt.legend()
    plt.xlabel('time')
    plt.ylabel('Amplitude')
    plt.title('Example of sine wave')
    plt.show()


def prac4():
    s1 = np.random.normal(loc=0, scale=1, size=1000)
    s2 = np.random.normal(loc=5, scale=0.5, size=1000)
    s3 = np.random.normal(loc=10, scale=2, size=1000)
    plt.figure(figsize=(10, 6))
    plt.plot(s1, label='s1')
    plt.plot(s2, label='s2')
    plt.plot(s3, label='s3')
    plt.legend(loc=1)
    plt.show()


def prac5():
    s1 = np.random.normal(loc=0, scale=1, size=1000)
    s2 = np.random.normal(loc=5, scale=0.5, size=1000)
    s3 = np.random.normal(loc=10, scale=2, size=1000)
    plt.figure(figsize=(10, 6))
    plt.boxplot((s1, s2, s3))
    plt.grid()
    plt.show()



def prac6():
    plt.figure(figsize=(10, 6))
    plt.subplot(221)
    plt.subplot(222)
    plt.subplot(212)

    plt.show()


if __name__ == '__main__':
    prac6()
