import numpy as np
import matplotlib.pyplot as plt

def test1(a, *args):
    print("첫번째 인자:", a)
    for each in args:
        print("다른 인자", each)


def test2(**kwargs):
    for key, value in kwargs.items():
        print(key, ":", value)


def test3(amp, freq, sample_time, end_time, bias):
    time = np.arange(0, end_time, sample_time)
    result = amp * np.sin(2 * np.pi * freq * time) + bias

    plt.figure(figsize=(12, 6))
    plt.plot(time, result)
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel('Sin')
    plt.title(str(amp) + "*sin(2*pi*" + str(freq) + "*t )+" + str(bias))
    plt.show()


def test4(**kwargs):
    end_time, sample_time = kwargs.get('endTime', 1), kwargs.get('sampleTime', 0.01)
    amp, freq, bias = kwargs.get('amp', 2), kwargs.get('freq', 1), kwargs.get('bias', 0)
    figsize = kwargs.get('figsize', (12, 6))
    time = np.arange(0, end_time, sample_time)
    result = amp * np.sin(2 * np.pi * freq * time) + bias

    plt.figure(figsize=figsize)
    plt.plot(time, result)
    plt.grid(True)
    plt.xlabel('time')
    plt.ylabel('sin')
    plt.title(str(amp) + "*sin(2*pi*" + str(freq) + "*t )+" + str(bias))
    plt.show()


if __name__ == '__main__':
    test4(amp=2, freq=0.5, endTime=10)